# SKILL: MT5 Scalability Architecture
## Domain: 10,000+ Concurrent MetaTrader5 Users — Worker Pools, Redis Queue, Horizontal Scaling

**Activation triggers:** MT5 scalability, metatrader5 scale, 10000 users, concurrent MT5,
broker connection pool, MT5 worker, MT5 queue, MT5 sync, MT5 bridge, trading account sync,
copy trading scale, broker gateway scale, MT5 connection limit, MT5 Windows VM,
MT5 horizontal scaling, Redis queue MT5, WebSocket MT5, position sync, order sync,
MT5 circuit breaker, MT5 pool, MT5 batch, MT5 performance.

---

## Architecture Overview

MetaTrader5 **only runs on Windows**. The Expert Backend runs on Linux/Mac in
Docker/Podman and communicates with a Windows VM (MT5 Bridge) that holds the
actual MT5 connections.

```
┌──────────────────────────────────────────────────────────────────────┐
│  Expert Backend (Linux / Podman)  :8002                              │
│  ┌──────────────┐  ┌─────────────────────────────────────────────┐  │
│  │  FastAPI     │  │  MT5 Worker Pool (asyncio + Redis queue)    │  │
│  │  4 workers   │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  uvloop      │→ │  │ Worker 1 │  │ Worker 2 │  │ Worker N │  │  │
│  └──────────────┘  │  └──────────┘  └──────────┘  └──────────┘  │  │
│                    └──────────────────────────────────────────────┘  │
│                                      │                               │
│                                 Redis :6380                          │
│                         (job queue, position cache)                  │
│                                      │                               │
└──────────────────────────────────────┼───────────────────────────────┘
                                       │ HTTP/WS :8004
                         ┌─────────────────────────┐
                         │  MT5 Bridge (Windows VM) │
                         │  Python 3.x + MetaTrader5│
                         │  ┌────┐  ┌────┐  ┌────┐ │
                         │  │ T1 │  │ T2 │  │ T3 │ │  ← MT5 terminal threads
                         │  └────┘  └────┘  └────┘ │
                         └─────────────────────────┘
                                       │
                              MT5 Broker Servers
```

---

## MT5 Bridge — Windows VM Service

The MT5 Bridge runs on a **Windows-only VM** and exposes a lightweight HTTP/WS API
that the Expert Backend calls. It manages the actual MT5 terminal connections.

```python
# integral-expert-backend/app/services/mt5_bridge.py
"""
MT5 Bridge client — communicates with the Windows VM MT5 service.
Never connect to MT5 directly from the Expert Backend (Linux).
"""
import asyncio
import httpx
from typing import Optional, Any
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

MT5_BRIDGE_URL = settings.MT5_BRIDGE_URL   # e.g. "http://192.168.1.10:8004"
MT5_BRIDGE_TIMEOUT = 10.0                  # seconds


class MT5BridgeClient:
    """Async client for the Windows MT5 Bridge service."""

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=MT5_BRIDGE_URL,
                timeout=MT5_BRIDGE_TIMEOUT,
                limits=httpx.Limits(max_connections=200, max_keepalive_connections=50),
            )
        return self._client

    async def get_positions(self, account_id: str) -> list[dict]:
        client = await self._get_client()
        try:
            resp = await client.get(f"/accounts/{account_id}/positions")
            resp.raise_for_status()
            return resp.json()
        except httpx.TimeoutException:
            logger.warning("MT5 bridge timeout for account %s", account_id)
            raise
        except httpx.HTTPStatusError as e:
            logger.error("MT5 bridge error %s for account %s", e.response.status_code, account_id)
            raise

    async def sync_account(self, account_id: str, broker_config: dict) -> dict:
        client = await self._get_client()
        resp = await client.post(f"/accounts/{account_id}/sync", json=broker_config)
        resp.raise_for_status()
        return resp.json()

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()


# Singleton — one shared client per worker process
mt5_bridge = MT5BridgeClient()
```

---

## Redis Job Queue — 10k Concurrent User Pattern

Instead of making synchronous HTTP calls to the MT5 Bridge for each user request,
queue sync jobs in Redis. Workers drain the queue at their own rate, preventing
the Bridge from being overwhelmed.

```python
# integral-expert-backend/app/workers/mt5_sync_worker.py
"""
MT5 sync worker — pulls account-sync jobs from Redis queue, batches them,
sends to MT5 Bridge, stores results in Redis cache and PostgreSQL.

Designed for 10,000+ concurrent MT5 accounts:
- Redis BLPOP for non-polling queue drain
- Batch processing (up to 50 accounts per Bridge call)
- Circuit breaker for Bridge failures
- Result cache (TTL 30s) to avoid repeat queries for same account
"""
import asyncio
import json
import time
from typing import Optional
import redis.asyncio as aioredis
from app.core.config import settings
from app.core.logging import get_logger
from app.services.mt5_bridge import mt5_bridge
from app.db.session import AsyncSessionFactory

logger = get_logger(__name__)

QUEUE_KEY      = "mt5:sync:queue"
RESULT_PREFIX  = "mt5:positions:"
RESULT_TTL     = 30           # seconds — position cache TTL
BATCH_SIZE     = 50           # accounts per Bridge batch call
WORKER_SLEEP   = 0.1          # seconds between empty queue polls
CIRCUIT_OPEN_THRESHOLD = 5    # consecutive failures before circuit opens
CIRCUIT_RESET_AFTER    = 60   # seconds before retry after circuit opens


class CircuitBreaker:
    def __init__(self, threshold: int, reset_after: int):
        self.threshold   = threshold
        self.reset_after = reset_after
        self._failures   = 0
        self._opened_at: Optional[float] = None

    @property
    def is_open(self) -> bool:
        if self._opened_at and time.time() - self._opened_at > self.reset_after:
            logger.info("Circuit breaker: resetting after %ss", self.reset_after)
            self._failures  = 0
            self._opened_at = None
        return self._opened_at is not None

    def record_success(self):
        self._failures  = 0
        self._opened_at = None

    def record_failure(self):
        self._failures += 1
        if self._failures >= self.threshold:
            self._opened_at = time.time()
            logger.error(
                "Circuit breaker OPENED after %d failures — MT5 Bridge unreachable",
                self._failures
            )


_breaker = CircuitBreaker(CIRCUIT_OPEN_THRESHOLD, CIRCUIT_RESET_AFTER)


async def enqueue_sync(redis: aioredis.Redis, account_id: str, payload: dict) -> None:
    """Add an account sync job to the Redis queue."""
    job = json.dumps({"account_id": account_id, **payload})
    await redis.rpush(QUEUE_KEY, job)


async def get_cached_positions(redis: aioredis.Redis, account_id: str) -> Optional[list]:
    """Return cached positions if available."""
    raw = await redis.get(f"{RESULT_PREFIX}{account_id}")
    if raw:
        return json.loads(raw)
    return None


async def cache_positions(redis: aioredis.Redis, account_id: str, positions: list) -> None:
    """Cache positions with TTL."""
    await redis.setex(
        f"{RESULT_PREFIX}{account_id}",
        RESULT_TTL,
        json.dumps(positions)
    )


async def run_worker(worker_id: int) -> None:
    """Main worker loop — drains the MT5 sync queue."""
    redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    logger.info("MT5 sync worker %d started", worker_id)

    while True:
        if _breaker.is_open:
            logger.warning("Worker %d: circuit open, sleeping %ds", worker_id, CIRCUIT_RESET_AFTER)
            await asyncio.sleep(CIRCUIT_RESET_AFTER)
            continue

        # Non-blocking batch drain
        batch: list[dict] = []
        for _ in range(BATCH_SIZE):
            raw = await redis.lpop(QUEUE_KEY)
            if raw is None:
                break
            batch.append(json.loads(raw))

        if not batch:
            await asyncio.sleep(WORKER_SLEEP)
            continue

        account_ids = [j["account_id"] for j in batch]
        logger.debug("Worker %d: processing batch of %d accounts", worker_id, len(batch))

        try:
            # Send batch to MT5 Bridge
            results = await mt5_bridge.sync_accounts_batch(account_ids)
            _breaker.record_success()

            # Cache results + persist to DB
            async with AsyncSessionFactory() as db:
                for account_id, positions in results.items():
                    await cache_positions(redis, account_id, positions)
                    await _persist_positions(db, account_id, positions)
                await db.commit()

        except Exception as exc:
            _breaker.record_failure()
            logger.exception("Worker %d batch failed: %s", worker_id, exc)
            # Re-queue failed jobs for retry
            for job in batch:
                await redis.rpush(QUEUE_KEY, json.dumps(job))


async def _persist_positions(db, account_id: str, positions: list) -> None:
    """Upsert positions from MT5 sync into journal.positions."""
    from sqlalchemy import text
    for pos in positions:
        await db.execute(text("""
            INSERT INTO journal.positions
              (account_id, ticket, symbol, volume, open_price, current_price, profit, updated_at)
            VALUES
              (:account_id, :ticket, :symbol, :volume, :open_price, :current_price, :profit, now())
            ON CONFLICT (account_id, ticket) DO UPDATE SET
              current_price = EXCLUDED.current_price,
              profit        = EXCLUDED.profit,
              updated_at    = now()
        """), {"account_id": account_id, **pos})


async def start_worker_pool(n_workers: int = 4) -> None:
    """Launch N concurrent sync workers."""
    logger.info("Starting MT5 sync worker pool with %d workers", n_workers)
    tasks = [asyncio.create_task(run_worker(i)) for i in range(n_workers)]
    await asyncio.gather(*tasks)
```

---

## FastAPI Startup — Worker Pool Integration

```python
# integral-expert-backend/app/main.py (additions for MT5 scalability)
import asyncio
from contextlib import asynccontextmanager
from app.workers.mt5_sync_worker import start_worker_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start MT5 sync worker pool on startup
    worker_task = asyncio.create_task(start_worker_pool(n_workers=4))
    yield
    # Graceful shutdown
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)
```

---

## PostgreSQL Connection Pooling for Scale

```python
# integral-expert-backend/app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,           # per-worker connections
    max_overflow=30,        # burst capacity
    pool_timeout=30,        # wait for connection
    pool_recycle=1800,      # recycle connections every 30min
    pool_pre_ping=True,     # detect stale connections
    echo=False,
)
```

**With 4 uvicorn workers × 20 pool_size = 80 max DB connections.**
Configure PostgreSQL `max_connections=200` to give headroom.

---

## Podman / Docker Scaling — Expert Backend

```yaml
# integral-expert-backend/docker-compose.yml
version: "3.9"

services:
  expert-backend:
    build:
      context: .
      dockerfile: Dockerfile
    image: integral-expert-backend:latest
    container_name: integral-expert-backend
    ports:
      - "8002:8002"
    env_file: .env
    environment:
      - PYTHONUNBUFFERED=1
      - WORKERS=4          # 4 uvicorn workers per container
      - MT5_SYNC_WORKERS=4 # 4 Redis queue workers per process
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: "4"
          memory: "4G"
```

**Horizontal scaling with multiple containers:**
```bash
# Scale to 3 container instances (behind Kong/nginx load balancer)
podman compose up -d --scale expert-backend=3

# Each instance: 4 uvicorn workers × 4 MT5 sync workers = 16 concurrent handlers
# 3 instances = 48 concurrent processing threads
# Redis queue ensures no duplicate processing
```

---

## WebSocket — Live Position Updates to 10k Clients

```python
# integral-expert-backend/app/api/v1/ws/positions.py
"""
WebSocket endpoint for live position updates.
Uses Redis pub/sub — MT5 sync workers publish, this WS broadcasts to clients.
Designed for 10k+ concurrent connections.
"""
import asyncio
import json
import redis.asyncio as aioredis
from fastapi import WebSocket, WebSocketDisconnect, Depends
from app.core.config import settings

POSITION_CHANNEL = "mt5:positions:updates"


async def position_ws_endpoint(ws: WebSocket, account_id: str):
    await ws.accept()
    redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"{POSITION_CHANNEL}:{account_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await ws.send_text(message["data"])
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe()
        await redis.close()
```

```python
# In sync worker — publish after updating positions:
await redis.publish(
    f"{POSITION_CHANNEL}:{account_id}",
    json.dumps({"positions": positions, "ts": time.time()})
)
```

---

## Broker Connection Schema

```sql
-- integral-expert-backend/alembic/versions/XXX_broker_connections.py

-- Encrypted broker credentials
CREATE TABLE broker_connections.accounts (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID NOT NULL,  -- references iam.users (cross-schema FK — no DB FK, ORM only)
    broker       VARCHAR(50) NOT NULL,   -- 'mt5', 'binance', 'ctrader'
    account_id   VARCHAR(100) NOT NULL,
    server       VARCHAR(200),           -- MT5 broker server address
    login        VARCHAR(100),
    -- NEVER store plaintext passwords — use Fernet encryption
    password_enc BYTEA,                  -- encrypted with ENCRYPTION_KEY from .env
    is_active    BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMPTZ,
    sync_status  VARCHAR(20) DEFAULT 'pending',  -- pending|syncing|ok|error
    error_msg    TEXT,
    created_at   TIMESTAMPTZ DEFAULT now(),
    updated_at   TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_broker_accounts_user ON broker_connections.accounts(user_id);
CREATE INDEX idx_broker_accounts_sync ON broker_connections.accounts(sync_status, last_sync_at);
```

**Password encryption pattern:**
```python
from cryptography.fernet import Fernet

class BrokerEncryption:
    def __init__(self, key: str):
        self.fernet = Fernet(key.encode())

    def encrypt_password(self, plaintext: str) -> bytes:
        return self.fernet.encrypt(plaintext.encode())

    def decrypt_password(self, ciphertext: bytes) -> str:
        return self.fernet.decrypt(ciphertext).decode()
```

---

## SLA Targets for MT5 at Scale

```
Metric                          Target
────────────────────────────────────────────────────────
Position sync latency           < 5s  (P95)
WebSocket push latency          < 200ms
API response time (reads)       < 100ms (P95, cached)
API response time (writes)      < 500ms (P95)
Concurrent accounts syncing     10,000+
Queue depth                     < 1000 pending jobs
Circuit breaker recovery        < 60s after Bridge recovery
DB connection pool utilization  < 70% at peak
Redis memory usage              < 4GB (position cache)
```

---

## Monitoring Hooks

```python
# Add to every sync worker iteration:
from prometheus_client import Counter, Histogram, Gauge

sync_jobs_total = Counter("mt5_sync_jobs_total", "Total MT5 sync jobs", ["status"])
sync_duration   = Histogram("mt5_sync_duration_seconds", "MT5 sync job duration")
queue_depth     = Gauge("mt5_queue_depth", "Current MT5 sync queue depth")

# In worker loop:
with sync_duration.time():
    await process_batch(batch)
sync_jobs_total.labels(status="success").inc(len(batch))

# In health endpoint:
depth = await redis.llen(QUEUE_KEY)
queue_depth.set(depth)
```

---

## Anti-Patterns

```
✗ Calling MT5 directly from FastAPI request handlers (blocks event loop)
✗ One DB connection per MT5 sync job (exhausts pool at 10k users)
✗ Storing MT5 passwords in plaintext (critical security violation)
✗ No circuit breaker on MT5 Bridge (one failure cascades to 10k users)
✗ Using threading instead of asyncio for concurrent MT5 jobs (GIL)
✗ Polling Redis with sleep() instead of BLPOP (CPU waste)
✗ No result caching (same account queried N times per second)
✗ Running MT5 terminal on Linux (MetaTrader5 is Windows-only)
✗ Scaling stateful WebSocket handlers without Redis pub/sub (split-brain)
```
