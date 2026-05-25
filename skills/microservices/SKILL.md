# SKILL: Microservices Architect
## Domain: Service Design, Inter-Service Communication, API Gateway, Service Mesh

**Activation triggers:** new service, service boundary, inter-service call,
API gateway, Kong, service discovery, microservice design, service contract,
service decomposition.

---

## Service Inventory

```
Service               Port   Schema Owner      Responsibility
──────────────────────────────────────────────────────────────
market-backend         8000  iam, academy       IAM, auth, academy, library
expert-backend         8002  journal, copy_*    Trading journal, copy trading
imi-backend            8003  market_intelligence AI analysis, news, sentiment
mt5-bridge             8004  (no DB)            MT5 Windows bridge (REST)
kong-gateway           8080  (config)           API gateway, routing, auth
```

---

## Service Boundary Rules

```python
# Rule 1: Services own their schemas — NEVER cross schema ownership
# expert-backend CANNOT directly query iam.users — call market-backend API instead

# WRONG:
async def get_user_name(user_id: str, db: AsyncSession) -> str:
    result = await db.execute(text("SELECT email FROM iam.users WHERE id = :id"), {"id": user_id})
    return result.scalar()

# CORRECT: Call market-backend via internal API
async def get_user_name(user_id: str, http: httpx.AsyncClient) -> str:
    resp = await http.get(
        f"{settings.MARKET_BACKEND_URL}/internal/users/{user_id}",
        headers={"X-Service-Key": settings.INTERNAL_SERVICE_KEY},
    )
    resp.raise_for_status()
    return resp.json()["email"]
```

---

## Internal Service Communication

```python
# app/core/service_client.py
# HTTP client for internal service-to-service calls

import httpx
from app.core.config import settings

class ServiceClient:
    """Authenticated internal service client with retry and timeout."""

    def __init__(self, base_url: str, service_name: str):
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(10.0),
            headers={
                "X-Service-Name": service_name,
                "X-Service-Key": settings.INTERNAL_SERVICE_KEY,
            },
        )

    async def get(self, path: str, **kwargs) -> dict:
        try:
            resp = await self.client.get(path, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except httpx.TimeoutException:
            raise ServiceUnavailableError(f"Service timeout: {path}")
        except httpx.HTTPStatusError as e:
            raise ServiceError(f"Service error {e.response.status_code}: {path}")

# Usage in expert-backend:
market_client = ServiceClient(settings.MARKET_BACKEND_URL, "expert-backend")
user_data = await market_client.get(f"/internal/users/{user_id}")
```

---

## Kong API Gateway Configuration

```yaml
# kong/declarative/kong.yml
_format_version: "3.0"

services:
  - name: market-backend
    url: http://market-backend:8000
    routes:
      - name: market-api
        paths: [/api/v1/auth, /api/v1/academy, /api/v1/library, /api/v1/community]
        plugins:
          - name: jwt
          - name: rate-limiting
            config: { minute: 100, policy: local }

  - name: expert-backend
    url: http://expert-backend:8002
    routes:
      - name: expert-api
        paths: [/api/v1/brokers, /api/v1/journal, /api/v1/copy-trading, /api/v1/imcharts]
        plugins:
          - name: jwt
          - name: rate-limiting
            config: { minute: 200, policy: local }

  - name: imi-backend
    url: http://imi-backend:8003
    routes:
      - name: intelligence-api
        paths: [/api/v1/intelligence, /api/v1/sentiment, /api/v1/signals]
        plugins:
          - name: jwt
          - name: rate-limiting
            config: { minute: 60, policy: local }
```

---

## Health Check Aggregation

```python
# app/api/internal/health.py — expose health check for service mesh
# Each service exposes /health AND /internal/health (for other services to ping)

@router.get("/internal/health")
async def internal_health():
    """Used by Kong and other services to verify this service is up."""
    return {"service": "expert-backend", "status": "ok", "version": settings.APP_VERSION}
```

---

## Service Decomposition Decision Framework

```
SPLIT a service when:
  - Teams are stepping on each other's code
  - Different scaling requirements (analytics needs more RAM, auth needs more replicas)
  - Different deployment cadences
  - Clear bounded context with its own data ownership

KEEP together when:
  - Less than 3 engineers on the whole platform
  - Same team owns both features
  - Features share data ownership (same DB schema)
  - Splitting would require cross-service transactions

Current recommendation for Integral Market:
  3-service architecture (market, expert, imi) is correct at this stage.
  Don't split further until team grows beyond 8 engineers.
```

---

## Anti-Patterns

```
✗ Services directly reading other services' DB schemas
✗ Synchronous chains > 3 hops (latency compounds: 100ms × 3 = 300ms minimum)
✗ No circuit breaker on inter-service calls (cascading failures)
✗ Sharing DB between services (defeats isolation)
✗ Hardcoding service URLs (use environment variables + service discovery)
✗ Missing internal health check endpoint (Kong can't health-check the service)
✗ Different JWT secrets per service (use shared secret via env var)
✗ Cross-service transactions without saga pattern (distributed transactions fail)
```
