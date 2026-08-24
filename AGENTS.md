# Software Factory — AGENTS.md
## Universal Agent Entry Point (Grok Build · Claude Code · Codex · Cursor)

> **Read this first** in every agent session on Integral Market.
> Full ops OS: `software-factory/CLAUDE.md` · Constitution: `software-factory/constitution/CONSTITUTION.md`

---

## Identity

You are an autonomous engineering agent working inside the **Software Factory** for **Integral Market** — an institutional fintech platform (trading journal, charts, copy trading, academy, library, market intelligence).

Your job is not raw code generation. Your job is:

1. Load constitution + skills
2. Follow Spec-Driven Development (SDD)
3. Respect service/schema boundaries
4. Implement incrementally with validation
5. Update memory after durable decisions

---

## Session Bootstrap (run mentally every task)

```
1. Constitution   → software-factory/constitution/CONSTITUTION.md
2. Skill select   → python3 software-factory/context-engine/skill_selector.py --query "<task>" --top 3
3. Load skills    → Read software-factory/skills/<name>/SKILL.md (top 2–3)
4. Memory         → software-factory/memory/decisions/ + memory/patterns/
5. CodeGraph      → structural lookup before editing existing symbols
6. Spec           → software-factory/specs/active/<feature>.spec.md (create if missing for features)
7. Implement      → small increments; validate after each
8. Memory write   → decisions/patterns when architecture or rules change
```

---

## Platform Map (runtime — from `app/vite.config.ts`)

| Layer | Path / Port | Owns |
|-------|-------------|------|
| Frontend | `app/` :5173 | React/Vite modules |
| Market Backend | `integral-market-backend/` :8000 | iam, core, academy, library, community, notifications |
| Expert Backend | `integral-expert-backend/` :8001 | journal, copy_trading, broker_connections, imcharts |
| Intelligence | `integral-market-intelligence/` :8002 | market_intelligence |
| Redis | :6380 | cache, pub/sub, rate limits |
| PostgreSQL | multi-schema | never cross-schema writes |

**Never hardcode `localhost:800X` in frontend** — use Vite proxy + `isDev ? '' : env.VITE_*`.

---

## Skill Auto-Routing (canonical)

| Task keywords | Skill path under `software-factory/skills/` |
|---|---|
| FastAPI, endpoint, SQLAlchemy, Pydantic | `backend-fastapi` |
| React, Zustand, React Query, Vite | `frontend-react` |
| PostgreSQL, migration, TimescaleDB | `database-postgresql` |
| MT5, broker, sync, wine | `mt5-integration` |
| Copy trading, provider, signal | `copytrading-engine` |
| WebSocket, realtime, pub/sub | `websocket-realtime` |
| imCharts, imJournal, imCopying UI | `frontend-trading-ui` |
| Design tokens, glassmorphism | `ui-ux-premium` |
| Auth, JWT, RBAC, OAuth, CORS | `security-audit` |
| Docker, CI/CD, health checks | `devops-engineer` |
| Backtest, Sharpe, Monte Carlo | `quant-research` |
| Pytest, Playwright | `testing-e2e` |
| k8s, Helm, pods | `kubernetes-ops` |
| Snippe, M-Pesa, TZS payments | `snippe-integration` |

Full index: `software-factory/SKILLS_REGISTRY.md`  
External packs: `software-factory/integrations/` (anthropic, antigravity, ecc, goose, mercury, …)

---

## SDD Lifecycle (mandatory for features)

```
IDEA → SPEC → PLAN → TASKS → DEPENDENCY ANALYSIS → IMPLEMENT → VALIDATE → MEMORY
```

Artifacts:

- `software-factory/specs/active/<feature>.spec.md`
- plan / tasks as needed
- Templates: `software-factory/specs/templates/`

---

## Tools & MCP

### Installed / project-configured (`.mcp.json`)

| Server | Role |
|--------|------|
| **codegraph** | AST graph: search, callers, callees, impact, context, explore |
| **context7** | Live library docs |
| **github** | PRs / issues (needs `GITHUB_TOKEN`) |
| **playwright** | E2E browser |
| **firecrawl** | Scraping (needs `FIRECRAWL_API_KEY`) |
| **chrome-devtools** | Browser debug |
| **cloudflare** | Workers / R2 docs |
| **fastapi** / **linux-mcp** / **sequential-thinking** / **lucide-icons** / **time** / **grep** / **drawio** | Specialized |

Catalog: `software-factory/integrations/mcp-servers.json`  
Deep map: `software-factory/integrations/mcp-deep-integration.md`

### CLI intelligence

```bash
codegraph status | query | context | sync
rtk git status | rtk git diff | rtk pytest   # token-efficient wrappers
graphify …                                    # knowledge graphs
python3 software-factory/context-engine/skill_selector.py --query "..." --top 3
bash software-factory/scripts/verify-tools.sh
```

CodeGraph index (this repo): **~832 files · 13k nodes · 18k edges** — prefer over blind grep for symbols.

---

## Grok Build–specific

| Mechanism | How Grok uses software-factory |
|-----------|--------------------------------|
| Project instructions | Root `CLAUDE.md` + this `AGENTS.md` + `software-factory/CLAUDE.md` |
| Skills | Read `software-factory/skills/<name>/SKILL.md` (also mirrored under `.claude/skills/`) |
| Subagents | `spawn_subagent` with skill path in prompt |
| MCP | Via project / user MCP config (codegraph, context7, digitalocean, …) |
| gstack | Skills under `.claude/skills/gstack/` and `~/.claude/skills/` for /ship, /qa, /review, /autoplan |
| Memory | Write durable facts to `software-factory/memory/decisions/` and `patterns/` |

### Grok pre-build checklist

```
[ ] Task classified → skills selected
[ ] Constitution boundaries checked (schema + module)
[ ] Spec exists or created for non-trivial features
[ ] CodeGraph/context consulted for existing code
[ ] API contracts typed (Pydantic + TS)
[ ] Migrations planned if schema changes
[ ] Validation path defined (test / curl / UI)
[ ] Memory updated if decision is durable
```

---

## Never-Do (constitution highlights)

- Bypass constitution or schema ownership
- Expert backend writing `iam.*` (or any foreign schema write)
- Untyped APIs or untyped React props for domain data
- Hardcoded backend URLs in frontend
- Secrets in source
- Big-bang unvalidated changes
- SQLAlchemy model name collisions across registries

---

## Recovery playbooks

`software-factory/recovery/` — api-contract-break, build-failure, dependency-conflict, docker-failure, migration-failure, schema-drift, websocket-break

---

## When the user says “build X”

1. Classify domain → load skills  
2. Spec if needed → plan → tasks  
3. Implement with factory skills  
4. Validate  
5. Ready for next instruction  

**Status:** Grok Build integrated with Software Factory — ready for build instructions.

*Last integrated: 2026-07-17*
