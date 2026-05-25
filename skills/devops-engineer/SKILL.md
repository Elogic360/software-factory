# SKILL: DevOps Engineer
## Domain: Docker, CI/CD, Kubernetes, Infrastructure as Code

**Activation triggers:** Dockerfile, docker-compose, CI pipeline, deployment,
environment config, service startup, health checks, scaling.

---

## Service Startup Order

```yaml
# docker-compose.yml dependency order
services:
  postgres:     # Start first — all others depend on it
  redis:        # Start second — backends depend on it
  market-backend:    depends_on: [postgres, redis]
  expert-backend:    depends_on: [postgres, redis]
  imi-backend:       depends_on: [postgres, redis]
  frontend:          depends_on: [market-backend]
  kong:              depends_on: [market-backend, expert-backend]
```

---

## Dev Start Script

```bash
#!/bin/bash
# dev-start.sh — start all services for local development
set -e

ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"
MARKET="$ROOT/integral-market-backend"
EXPERT="$ROOT/integral-expert-backend"

# Kill existing processes on our ports
lsof -ti:8000,8002,8003,5173 2>/dev/null | xargs kill -9 2>/dev/null || true
sleep 1

# Market backend
cd "$MARKET" && source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/market-backend.log 2>&1 &
echo "Market backend starting on :8000"

# Expert backend
cd "$EXPERT" && source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload > /tmp/expert-backend.log 2>&1 &
echo "Expert backend starting on :8002"

# Frontend
cd "$ROOT/app"
nohup pnpm dev > /tmp/frontend.log 2>&1 &
echo "Frontend starting on :5173"

echo "All services started. Check /tmp/*.log for output."
```

---

## Health Check Pattern

```python
# Every FastAPI service must expose /health
@app.get("/health")
async def health_check():
    checks = {}
    # Database
    try:
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))
        checks["database"] = {"status": "healthy"}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}

    # Redis
    try:
        await cache.redis.ping()
        checks["redis"] = {"status": "healthy"}
    except Exception as e:
        checks["redis"] = {"status": "unhealthy", "error": str(e)}

    overall = "healthy" if all(c["status"] == "healthy" for c in checks.values()) else "degraded"
    return {"status": overall, "version": settings.APP_VERSION, "checks": checks}
```

---

## Environment Variable Standards

```bash
# .env.example — document ALL variables (no secrets, just keys with descriptions)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname
DATABASE_URL_SYNC=postgresql://user:pass@localhost:5432/dbname
REDIS_URL=redis://:password@localhost:6380/0
SECRET_KEY=<generate with: openssl rand -hex 32>
ENCRYPTION_KEY=<generate with: python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">
GOOGLE_CLIENT_ID=<from Google Cloud Console>
GOOGLE_CLIENT_SECRET=<from Google Cloud Console>
GOOGLE_REDIRECT_URI=http://localhost:5173/auth/oauth/callback
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

---

## CI Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: timescale/timescaledb:latest-pg15
        env:
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
      redis:
        image: redis:7
        ports: ["6379:6379"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r integral-expert-backend/requirements.txt
      - run: cd integral-expert-backend && pytest --tb=short -q

  frontend-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd app && pnpm install --frozen-lockfile
      - run: cd app && pnpm type-check
      - run: cd app && pnpm lint
      - run: cd app && pnpm build

  constitution-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify constitution exists
        run: test -f software-factory/constitution/CONSTITUTION.md
      - name: Verify no venv committed
        run: '! git diff --name-only origin/main | grep "venv/"'
```

---

## Anti-Patterns

```
✗ Committing venv/, node_modules/, __pycache__/ to git
✗ Hardcoded secrets in docker-compose.yml or Dockerfiles
✗ Services starting without health checks
✗ Missing CORS configuration for production domains
✗ Running backends as root in containers
✗ No graceful shutdown handling (SIGTERM)
✗ Missing resource limits on containers
```
