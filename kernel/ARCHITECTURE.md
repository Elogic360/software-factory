# Integral Market — Architecture Kernel
## The Stable System Core: Service Topology, Schema Ownership, Agent Orientation

> **This file is the immutable reference for the platform's physical layout.**
> Every agent reads this before touching any code. It changes only when the
> architecture itself changes — not for features.

---

## 1. Service Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        INTEGRAL MARKET PLATFORM                             │
│                                                                             │
│   Browser / Mobile                                                          │
│       │                                                                     │
│       ▼                                                                     │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Frontend — React + Vite                    :5173 (dev)             │  │
│   │  app/                                       :80   (prod, nginx)     │  │
│   │  ├── /auth/*              → Market Backend  :8000                   │  │
│   │  ├── /academy/*           → Market Backend  :8000                   │  │
│   │  ├── /expert/* (charts)   → Expert Backend  :8002                   │  │
│   │  ├── /expert/* (copying)  → Expert Backend  :8002                   │  │
│   │  └── /intelligence/*      → IMI Backend     :8003                   │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│       │                │                │                                   │
│       ▼                ▼                ▼                                   │
│   ┌────────┐    ┌────────────┐   ┌─────────────┐                           │
│   │Market  │    │Expert      │   │Intelligence │                           │
│   │Backend │    │Backend     │   │Backend (IMI)│                           │
│   │:8000   │    │:8002       │   │:8003        │                           │
│   │Python  │    │Python      │   │Python       │                           │
│   │3.12.13 │    │3.12.13     │   │3.12.13      │                           │
│   │venv    │    │Docker/     │   │venv         │                           │
│   │        │    │Podman      │   │             │                           │
│   └────────┘    └────────────┘   └─────────────┘                           │
│       │                │                │                                   │
│       └────────────────┴────────────────┘                                  │
│                        │                                                    │
│               ┌─────────────────┐                                          │
│               │   PostgreSQL    │ :5432                                     │
│               │   (TimescaleDB) │                                          │
│               └─────────────────┘                                          │
│                        │                                                    │
│               ┌─────────────────┐                                          │
│               │     Redis       │ :6380                                     │
│               └─────────────────┘                                          │
│                                                                             │
│   MT5 Bridge   :8004  (Windows VM — MetaTrader5 only runs on Windows)      │
│   Kong Gateway :8080  (API gateway — prod only)                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Service Definitions

### Market Backend — `integral-market-backend/`
```
Runtime:    Python 3.12.13  in  venv  (NEVER Docker for this service)
Port:       8000
Config:     integral-market-backend/.env
Start:      cd integral-market-backend && source venv/bin/activate
            uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Log:        /tmp/market-backend.log
Health:     GET http://localhost:8000/health
Owns:       iam, core, academy, library, community, notifications schemas
```

### Expert Backend — `integral-expert-backend/`
```
Runtime:    Python 3.12.13  in  Docker (dev) or Podman (macOS/Linux ppc)
Port:       8002
Config:     integral-expert-backend/.env
Start:      podman compose up expert-backend   (Podman)
            docker compose up expert-backend   (Docker)
Log:        podman logs -f integral-expert-backend
            /tmp/expert-backend.log  (if run directly)
Health:     GET http://localhost:8002/health
Owns:       journal, copy_trading, broker_connections, imcharts schemas
Scale:      Horizontal — 10k+ concurrent MT5 users via worker pool + Redis queue
```

### IMI Backend — `integral-market-intelligence/` (or `integral-imi-backend/`)
```
Runtime:    Python 3.12.13  in  venv  (NEVER Docker for this service in dev)
Port:       8003
Config:     integral-market-intelligence/.env
Start:      cd integral-market-intelligence && source venv/bin/activate
            uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
Log:        /tmp/imi-backend.log
Health:     GET http://localhost:8003/health
Owns:       market_intelligence schema
```

### Frontend — `app/`
```
Runtime:    Node.js 20+, pnpm
Port:       5173 (dev)
Config:     app/.env.local
Start:      cd app && pnpm dev
Log:        /tmp/frontend.log  or  terminal stdout
Build:      cd app && pnpm build   → dist/
Proxy:      Vite routes /api/v1/brokers|journal|copy-trading|imcharts → :8002
            /api/* → :8000 (catch-all)
```

---

## 3. Database Schema Ownership Map

```sql
-- NEVER cross schema ownership boundaries
-- Market Backend owns:
CREATE SCHEMA iam;          -- users, roles, permissions, OAuth
CREATE SCHEMA core;         -- platform config, feature flags
CREATE SCHEMA academy;      -- courses, enrollments, progress
CREATE SCHEMA library;      -- e-library, documents
CREATE SCHEMA community;    -- forums, posts
CREATE SCHEMA notifications;-- push, email notification queue
CREATE SCHEMA audit;        -- shared audit log (all services write)

-- Expert Backend owns:
CREATE SCHEMA journal;        -- trades, journal entries, equity snapshots
CREATE SCHEMA copy_trading;   -- providers, subscriptions, signals, execution_logs
CREATE SCHEMA broker_connections; -- encrypted broker accounts
CREATE SCHEMA imcharts;       -- watchlists, chart layouts, alerts

-- IMI Backend owns:
CREATE SCHEMA market_intelligence; -- analyses, sentiment, news
```

---

## 4. Port Reference

| Service           | Dev Port | Protocol | Notes                        |
|-------------------|----------|----------|------------------------------|
| Frontend (Vite)   | 5173     | HTTP/WS  | Vite proxy routes to backends|
| Market Backend    | 8000     | HTTP/WS  | Python venv                  |
| Expert Backend    | 8002     | HTTP/WS  | Docker / Podman              |
| IMI Backend       | 8003     | HTTP/WS  | Python venv                  |
| MT5 Bridge        | 8004     | HTTP     | Windows VM only              |
| PostgreSQL        | 5432     | TCP      | TimescaleDB                  |
| Redis             | 6380     | TCP      | Custom port (not default 6379)|
| Kong Gateway      | 8080     | HTTP     | Prod only                    |

---

## 5. CodeGraph Integration Protocol

CodeGraph (`codegraph_*` tools) gives sub-millisecond structural queries over
the entire AST-parsed codebase. **Always use CodeGraph for structural questions.**

```python
# Before touching any shared utility or model:
codegraph_impact("function_name_or_class")
# → shows every file that would break if this symbol changes

# Before adding a new model:
codegraph_search("ClassName")
# → find if the name is already used (prevent registry collisions)

# When starting work on a domain:
codegraph_context("copy_trading")
# → returns relevant files, types, relationships in one shot

# When unsure where something is defined:
codegraph_search("FunctionName")
# → returns kind + location + signature

# NEVER grep first for structural questions — CodeGraph is faster and complete
```

**CodeGraph initialization** (run once per repo, or when `.codegraph/` missing):
```bash
cd "/home/elogic360/Desktop/little QUANTUM/Integral Market"
codegraph init -i
```

---

## 6. Graphify Integration Protocol

Graphify builds a **semantic knowledge graph** of the codebase with community
detection — it surfaces emergent clusters that CodeGraph's AST view misses.

```bash
# Run Graphify to update the knowledge graph after large changes:
/graphify   # (invokes the graphify Claude skill)

# Graphify output lives in: software-factory/graphify/
# Key artifacts:
#   graph.json          — full semantic graph
#   communities.json    — detected code communities
#   architecture-map.md — auto-generated architecture narrative
```

**When to re-run Graphify:**
- After adding a new service or major feature
- After a large refactoring session
- Before writing an ADR that affects multiple services
- Monthly, as part of the architecture review

---

## 7. Environment Files

```
Root project:
  .env                  ← NEVER commit — symlink to .env.local for dev

Market Backend:
  integral-market-backend/.env          ← dev secrets
  integral-market-backend/.env.example  ← template (commit this)

Expert Backend:
  integral-expert-backend/.env          ← dev secrets
  integral-expert-backend/.env.example  ← template (commit this)
  integral-expert-backend/docker-compose.yml

IMI Backend:
  integral-market-intelligence/.env          ← dev secrets
  integral-market-intelligence/.env.example  ← template

Frontend:
  app/.env.local        ← Vite env (VITE_* prefix for client-side)
  app/.env.example      ← template (commit this)
```

---

## 8. Vite Proxy Rules (Critical — order matters)

```typescript
// app/vite.config.ts — Expert routes MUST precede catch-all /api
proxy: {
  '/api/v1/brokers':      { target: 'http://localhost:8002', changeOrigin: true },
  '/api/v1/imcharts':     { target: 'http://localhost:8002', changeOrigin: true },
  '/api/v1/journal':      { target: 'http://localhost:8002', changeOrigin: true },
  '/api/v1/copy-trading': { target: 'http://localhost:8002', changeOrigin: true },
  '/api/v1/signals':      { target: 'http://localhost:8002', changeOrigin: true },
  '/api/v1/bots':         { target: 'http://localhost:8002', changeOrigin: true },
  '/api/v1/gateway':      { target: 'http://localhost:8002', changeOrigin: true },
  '/api/v1/intelligence': { target: 'http://localhost:8003', changeOrigin: true },
  '/api/v1/sentiment':    { target: 'http://localhost:8003', changeOrigin: true },
  '/ws/expert':           { target: 'ws://localhost:8002', ws: true, changeOrigin: true },
  '/ws':                  { target: 'ws://localhost:8000', ws: true, changeOrigin: true },
  '/api':                 { target: 'http://localhost:8000', changeOrigin: true },
}
```

---

## 9. Python Version Enforcement

```bash
# ALL services MUST use Python 3.12.13
# Verify before running:
python3 --version  # must print Python 3.12.13

# Install pyenv if needed:
pyenv install 3.12.13
pyenv local 3.12.13

# Create venv with exact version:
python3.12 -m venv venv
source venv/bin/activate
python3 --version   # verify: 3.12.13

# For Docker/Podman (expert-backend):
# FROM python:3.12.13-slim  ← exact version in Dockerfile
```

---

## 10. Architecture Change Protocol

When this kernel must change:
1. Write an ADR in `software-factory/memory/decisions/adr-NNNN-<title>.md`
2. Update this file (`kernel/ARCHITECTURE.md`)
3. Update `software-factory/CLAUDE.md` section 5 (Platform Architecture Map)
4. Update `SKILLS_REGISTRY.md` if new service boundaries affect skill domains
5. Re-run `codegraph init -i` and `/graphify` to re-index
6. Commit with message: `arch: <title of change>`
