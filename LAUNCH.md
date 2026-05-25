# Integral Market — Complete Launch Guide
## Starting All Services: Frontend + 3 Backends + Infrastructure

> **Always start infrastructure first (PostgreSQL + Redis), then backends,
> then frontend. The order matters.**

---

## Prerequisites

```bash
# Verify all tools are installed
python3 --version      # must be 3.12.13
node --version         # must be ≥ 20.0.0
pnpm --version         # must be ≥ 8.0.0

# Check infrastructure
pg_isready -h localhost -p 5432    # PostgreSQL running?
redis-cli -p 6380 ping             # Redis running? → should print PONG

# Check container runtime (expert-backend only)
podman --version    # OR: docker --version
```

---

## Quick Launch (all services at once)

```bash
# One-command launch — all 4 services
ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"
bash "$ROOT/software-factory/scripts/dev-start-all.sh"

# Monitor all logs together
tail -f /tmp/market-backend.log /tmp/imi-backend.log /tmp/frontend.log \
  | grep -v "^$"

# Expert backend logs (Docker/Podman)
podman logs -f integral-expert-backend
# OR:
docker logs -f integral-expert-backend
```

---

## 1. Infrastructure (PostgreSQL + Redis)

PostgreSQL and Redis must be running before any backend starts.

```bash
# Check if already running
pg_isready -h localhost -p 5432
redis-cli -p 6380 ping

# Start if not running (systemd)
sudo systemctl start postgresql
sudo systemctl start redis

# Start if using Docker/Podman
podman run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=integral_market \
  -p 5432:5432 \
  timescale/timescaledb:latest-pg15

podman run -d \
  --name redis \
  -p 6380:6379 \
  redis:7 redis-server --requirepass your_redis_password

# Verify
pg_isready -h localhost -p 5432   # → "accepting connections"
redis-cli -p 6380 -a your_redis_password ping   # → PONG
```

---

## 2. Market Backend — `integral-market-backend/`

```
Runtime:  Python 3.12.13  in  venv   (NEVER Docker)
Port:     8000
Purpose:  IAM, auth, OAuth, academy, library, community
```

### First-Time Setup

```bash
ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"
cd "$ROOT/integral-market-backend"

# Install Python 3.12.13 (via pyenv if not system default)
pyenv install 3.12.13
pyenv local 3.12.13

# Create venv with exact Python version
python3.12 -m venv venv
source venv/bin/activate
python3 --version    # verify: Python 3.12.13

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env from example
cp .env.example .env
# Edit .env — fill in:
#   DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/integral_market
#   DATABASE_URL_SYNC=postgresql://user:pass@localhost:5432/integral_market
#   REDIS_URL=redis://:password@localhost:6380/0
#   SECRET_KEY=<openssl rand -hex 32>
#   ENCRYPTION_KEY=<python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">
#   GOOGLE_CLIENT_ID=<from Google Cloud Console>
#   GOOGLE_CLIENT_SECRET=<from Google Cloud Console>
#   GOOGLE_REDIRECT_URI=http://localhost:5173/auth/oauth/callback
#   BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Run migrations
alembic upgrade head
alembic check    # verify DB matches models

# Seed required data (roles, permissions, initial admin)
python3 seed_data.py   # if exists
# OR manually seed the 'user' role:
python3 -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
import os
from dotenv import load_dotenv
load_dotenv()
async def seed():
    engine = create_async_engine(os.environ['DATABASE_URL'])
    async with AsyncSession(engine) as db:
        await db.execute(text(\"\"\"
            INSERT INTO iam.roles (name, hierarchy_level, is_active)
            VALUES ('user', 1, true),
                   ('premium', 2, true),
                   ('expert', 3, true),
                   ('admin', 10, true)
            ON CONFLICT (name) DO NOTHING
        \"\"\"))
        await db.commit()
    print('Roles seeded')
asyncio.run(seed())
"
```

### Daily Start

```bash
ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"
cd "$ROOT/integral-market-backend"
source venv/bin/activate

# Run in foreground (dev):
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run in background (nohup):
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload \
  > /tmp/market-backend.log 2>&1 &
echo "Market backend PID: $!"

# Health check
curl http://localhost:8000/health | python3 -m json.tool
```

---

## 3. Expert Backend — `integral-expert-backend/`

```
Runtime:  Python 3.12.13  in  Docker (Linux) or Podman (macOS / ppc Linux)
Port:     8002
Purpose:  Trading journal, copy trading, broker connections, imCharts
Scale:    10,000+ concurrent MT5 users
```

### Dockerfile

```dockerfile
# integral-expert-backend/Dockerfile
FROM python:3.12.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Run with multiple workers for 10k+ users
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8002", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--loop", "uvloop", \
     "--timeout-keep-alive", "30"]
```

### docker-compose.yml (expert-backend section)

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
    env_file:
      - .env
    environment:
      - PYTHONUNBUFFERED=1
      - WORKERS=4
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    volumes:
      - ./:/app  # dev only — remove for production
```

### Launch with Podman (ppc / macOS)

```bash
ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"
cd "$ROOT/integral-expert-backend"

# First-time build
podman build -t integral-expert-backend:latest .

# Run
podman run -d \
  --name integral-expert-backend \
  --env-file .env \
  -p 8002:8002 \
  -v "$(pwd)":/app \
  integral-expert-backend:latest

# OR with compose
podman compose up -d expert-backend

# View logs
podman logs -f integral-expert-backend

# Health check
curl http://localhost:8002/health | python3 -m json.tool

# Restart after code change
podman compose build expert-backend && podman compose up -d expert-backend
```

### Launch with Docker (Linux standard)

```bash
cd "$ROOT/integral-expert-backend"
docker compose up -d expert-backend
docker logs -f integral-expert-backend
curl http://localhost:8002/health
```

---

## 4. IMI Backend — `integral-market-intelligence/`

```
Runtime:  Python 3.12.13  in  venv   (NEVER Docker for dev)
Port:     8003
Purpose:  AI market analysis, sentiment, news, signals
```

```bash
ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"
cd "$ROOT/integral-market-intelligence"   # or integral-imi-backend/

# First-time setup
python3.12 -m venv venv
source venv/bin/activate
python3 --version    # verify: Python 3.12.13
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Required:
#   ANTHROPIC_API_KEY=sk-ant-...   (for Claude AI features)
#   DATABASE_URL=...
#   REDIS_URL=...
#   MARKET_BACKEND_URL=http://localhost:8000

# Start
nohup uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload \
  > /tmp/imi-backend.log 2>&1 &
curl http://localhost:8003/health
```

---

## 5. Frontend — `app/`

```
Runtime:  Node.js 20+, pnpm
Port:     5173 (dev)
```

```bash
ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"
cd "$ROOT/app"

# First-time setup
pnpm install

# Create .env.local (Vite reads this)
cat > .env.local << 'EOF'
VITE_APP_ENV=development
# Leave these EMPTY in dev — Vite proxy routes to correct backends
VITE_MARKET_API_URL=
VITE_EXPERT_API_URL=
VITE_IMI_API_URL=
EOF
# Note: DO NOT set localhost URLs — leave blank so Vite proxy works!

# Start dev server
pnpm dev

# Verify all proxy routes work
curl http://localhost:5173/api/v1/auth/me    # → market backend
curl http://localhost:5173/api/v1/brokers/accounts  # → expert backend
curl http://localhost:5173/api/v1/intelligence/   # → IMI backend

# Type check
pnpm type-check

# Build for production
pnpm build
```

---

## 6. Full Health Check

After all services start, run this to verify everything is healthy:

```bash
python3 software-factory/context-engine/dev_runner.py --health
```

Or manually:

```bash
echo "=== INFRASTRUCTURE ===" && \
pg_isready -h localhost -p 5432 && \
redis-cli -p 6380 ping && \
echo "=== BACKENDS ===" && \
curl -s http://localhost:8000/health | python3 -m json.tool && \
curl -s http://localhost:8002/health | python3 -m json.tool && \
curl -s http://localhost:8003/health | python3 -m json.tool && \
echo "=== FRONTEND ===" && \
curl -s -o /dev/null -w "Frontend: HTTP %{http_code}\n" http://localhost:5173
```

---

## 7. Common Startup Errors

| Error | Service | Fix |
|-------|---------|-----|
| `connection refused :5432` | All backends | `sudo systemctl start postgresql` |
| `connection refused :6380` | All backends | `sudo systemctl start redis` |
| `No 'free'/'user' role found` | Market | Run role seed script |
| `Module not found` | Python | `pip install -r requirements.txt` |
| `Cannot find module X` | Frontend | `pnpm install` |
| `Address already in use :8002` | Expert | `lsof -ti:8002 \| xargs kill -9` |
| `CORS error in browser` | Frontend | Restart Vite (config may have changed) |
| `TS errors on pnpm dev` | Frontend | `pnpm type-check` to see full list |
| `alembic heads diverged` | Backends | `alembic merge heads && alembic upgrade head` |
| `container not found` | Expert | `podman compose up -d` to rebuild |

---

## 8. Log Locations

| Service | Log Path | Live Tail |
|---------|----------|-----------|
| Market Backend | `/tmp/market-backend.log` | `tail -f /tmp/market-backend.log` |
| Expert Backend | Podman/Docker | `podman logs -f integral-expert-backend` |
| IMI Backend | `/tmp/imi-backend.log` | `tail -f /tmp/imi-backend.log` |
| Frontend | `/tmp/frontend.log` | `tail -f /tmp/frontend.log` |
| PostgreSQL | `/var/log/postgresql/` | `sudo tail -f /var/log/postgresql/postgresql-*.log` |

---

## 9. Stopping All Services

```bash
# Kill venv backends
lsof -ti:8000,8003 | xargs kill -9 2>/dev/null || true

# Stop expert backend
podman compose down    # OR: docker compose down

# Stop frontend
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

echo "All services stopped."
```
