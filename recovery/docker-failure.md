# Recovery Playbook: Docker / Service Failure

## Diagnosis Tree

```
Service won't start?
  │
  ├── Port already in use
  │     → lsof -ti:8000,8002,8003,5173 | xargs kill -9
  │     → OR: kill the specific process using the port
  │
  ├── "cannot connect to Docker daemon"
  │     → sudo systemctl start docker
  │     → OR: sudo service docker start
  │
  ├── Container exits immediately
  │     → docker logs <container-name> | tail -50
  │     → Usually: missing env var, DB not ready, port conflict
  │
  ├── Backend starts but returns 500 on every request
  │     → Check service log: tail -f /tmp/expert-backend.log
  │     → Usually: DB connection failed, Redis unreachable, import error
  │
  ├── PostgreSQL connection refused
  │     → pg_isready -h localhost -p 5432
  │     → sudo systemctl start postgresql
  │     → Check pg_hba.conf allows local connections
  │
  └── Redis connection refused
        → redis-cli ping
        → sudo systemctl start redis
        → Check REDIS_URL in .env matches running Redis port/password
```

---

## Quick Service Reset

```bash
#!/bin/bash
# Reset all services to clean state

ROOT="/home/elogic360/Desktop/little QUANTUM/Integral Market"

# Kill everything on our ports
echo "Stopping services..."
lsof -ti:8000,8002,8003,5173 2>/dev/null | xargs kill -9 2>/dev/null || true
sleep 1

# Verify infrastructure is running
pg_isready -h localhost -p 5432 || echo "WARNING: PostgreSQL not running"
redis-cli ping || echo "WARNING: Redis not running"

# Start market backend
cd "$ROOT/integral-market-backend" && source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/market-backend.log 2>&1 &
echo "Market backend starting on :8000"

# Start expert backend
cd "$ROOT/integral-expert-backend" && source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload > /tmp/expert-backend.log 2>&1 &
echo "Expert backend starting on :8002"

# Wait for backends to be ready
sleep 3
curl -s http://localhost:8000/health | python3 -m json.tool || echo "Market backend: not healthy"
curl -s http://localhost:8002/health | python3 -m json.tool || echo "Expert backend: not healthy"

# Start frontend
cd "$ROOT/app"
nohup pnpm dev > /tmp/frontend.log 2>&1 &
echo "Frontend starting on :5173"

echo ""
echo "Logs:"
echo "  Market:  tail -f /tmp/market-backend.log"
echo "  Expert:  tail -f /tmp/expert-backend.log"
echo "  Frontend: tail -f /tmp/frontend.log"
```

---

## Health Check All Services

```bash
# Check all service health endpoints
for service in "8000:Market" "8002:Expert" "8003:IMI"; do
  port="${service%%:*}"
  name="${service##*:}"
  response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/health")
  if [ "$response" = "200" ]; then
    echo "✅ $name backend (:$port) — healthy"
  else
    echo "❌ $name backend (:$port) — HTTP $response"
    echo "   Check: tail -f /tmp/$(echo $name | tr '[:upper:]' '[:lower:]')-backend.log"
  fi
done

# Frontend
response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:5173")
[ "$response" = "200" ] && echo "✅ Frontend (:5173) — running" || echo "❌ Frontend (:5173) — not responding"
```

---

## Docker Compose (Production-like)

```bash
# Start all services via docker-compose
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f market-backend
docker compose logs -f expert-backend

# Restart a single service
docker compose restart expert-backend

# Full rebuild after code change
docker compose build expert-backend
docker compose up -d expert-backend
```
