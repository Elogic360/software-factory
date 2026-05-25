# Recovery Playbook: Build Failure

## Diagnosis Tree

```
Build fails?
  │
  ├── Python / FastAPI backend
  │     ├── ImportError / ModuleNotFoundError
  │     │     → pip install -r requirements.txt
  │     │     → check venv is activated: which python
  │     │
  │     ├── SQLAlchemy "Multiple classes found for path X"
  │     │     → REGISTRY COLLISION — two models with same class name
  │     │     → grep -r "class Subscription" integral-expert-backend/
  │     │     → rename the conflicting class (add domain prefix)
  │     │     → See: skills/copytrading-engine/SKILL.md → SQLAlchemy Registry Rules
  │     │
  │     ├── Pydantic ValidationError on startup
  │     │     → Missing required .env variable
  │     │     → check .env.example for required keys
  │     │     → python3 -c "from app.core.config import settings; print('ok')"
  │     │
  │     └── alembic.util.CommandError: Can't locate revision
  │           → alembic heads — check for multiple heads
  │           → alembic merge heads -m "merge"
  │           → alembic upgrade head
  │
  ├── TypeScript / Vite frontend
  │     ├── TypeScript error (TS2xxx)
  │     │     → pnpm type-check for full error list
  │     │     → Check import path is correct
  │     │     → Check type definition matches API response schema
  │     │
  │     ├── Module not found
  │     │     → pnpm install
  │     │     → check tsconfig.json paths aliases
  │     │
  │     ├── Vite build fails with chunk size warning
  │     │     → check skills/performance-engineering/SKILL.md → code splitting
  │     │     → add manualChunks to vite.config.ts
  │     │
  │     └── pnpm type-check passes but build fails
  │           → usually a dynamic import or CSS issue
  │           → run: pnpm build 2>&1 | head -50
  │
  └── Docker / CI
        ├── docker build fails with COPY error
        │     → file path in Dockerfile wrong
        │     → .dockerignore excluding needed file
        │
        └── CI fails with "no module named X"
              → requirements.txt not committed / out of date
              → run: pip freeze > requirements.txt && git add
```

---

## Quick Fixes

```bash
# Backend: reset venv from scratch
cd integral-expert-backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend: reset node_modules
cd app
rm -rf node_modules .pnpm-store
pnpm install

# Check all services start correctly
bash software-factory/skills/devops-engineer/dev-start.sh

# Verify backend imports work
cd integral-expert-backend && source venv/bin/activate
python3 -c "from app.main import app; print('Expert backend OK')"

cd integral-market-backend && source venv/bin/activate
python3 -c "from app.main import app; print('Market backend OK')"
```

---

## When to Escalate

If the build has been broken for > 30 minutes:
1. Check git log — did a recent commit introduce the break?
2. `git bisect start HEAD <last-known-good-commit>` to isolate
3. Document the root cause in `software-factory/memory/patterns/anti-patterns.md`
