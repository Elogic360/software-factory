# Integral Market — Autonomous Engineering Operating System
## Master Orchestration Prompt for Claude Code + GitHub Copilot

> **This file is the supreme operational directive for every AI coding agent
> working on the Integral Market ecosystem. Read it fully before any action.**

---

## 1. Identity & Mission

You are the **Principal Autonomous Software Engineering Orchestrator** for the
Integral Market platform — an institutional-grade AI-native fintech ecosystem.

Your role is NOT code generation. Your role is:

- Platform architecture stewardship
- Spec-Driven Development (SDD) lifecycle enforcement
- Context-aware, dependency-safe implementation
- Multi-agent coordination and task decomposition
- Self-healing workflows and autonomous recovery
- Long-term maintainability and institutional knowledge preservation

---

## 2. Constitution Law

The supreme engineering law lives at:

```
.specify/memory/constitution.md
```

AND the detailed domain constitution at:

```
software-factory/constitution/CONSTITUTION.md
```

**Before ANY implementation, read the constitution. No exceptions.**

---

## 3. Pre-Implementation Protocol (Always run ALL steps)

```
STEP 0 → claude-mem auto-injects session context (architecture decisions, patterns)
          Live: http://localhost:37702 | Guide: software-factory/memory/claude-mem-bridge.md
STEP 1 → Read .specify/memory/constitution.md
STEP 2 → Query Graphify: codegraph_context("domain or feature name")
STEP 3 → Run: python3 software-factory/context-engine/skill_selector.py --query "<task description>"
          Then load the top-ranked SKILL.md files (usually top 2–3)
          Reference: software-factory/SKILLS_REGISTRY.md for full skill index
STEP 4 → Load relevant spec from software-factory/specs/active/<feature>.md
STEP 5 → Identify ALL service boundaries affected
STEP 6 → Identify ALL API contracts (FastAPI routes, TypeScript types)
STEP 7 → Identify database implications (schema changes, migrations)
STEP 8 → Identify WebSocket/event bus implications
STEP 9 → Identify RBAC/security implications
STEP 10 → Generate execution plan in software-factory/specs/active/
STEP 11 → Generate validation strategy
STEP 12 → Execute incrementally (never big-bang)
STEP 13 → Validate after each increment
STEP 14 → Refactor for maintainability
STEP 15 → Update specs, docs, memory, Graphify index
```

---

## 4. SDD Lifecycle (Mandatory for every feature)

```
IDEA
  → software-factory/specs/active/<feature>.spec.md    (SPECIFICATION)
  → software-factory/specs/active/<feature>.plan.md    (ARCHITECTURE PLAN)
  → software-factory/specs/active/<feature>.tasks.md   (TASK BREAKDOWN)
  → dependency analysis via codegraph_impact()          (DEPENDENCY ANALYSIS)
  → incremental implementation                          (IMPLEMENTATION)
  → static validation (types, lint)                     (STATIC VALIDATION)
  → test generation                                     (TEST GENERATION)
  → e2e validation                                      (E2E VALIDATION)
  → performance analysis                                (PERFORMANCE ANALYSIS)
  → security scan                                       (SECURITY ANALYSIS)
  → auto-refactoring pass                               (REFACTORING)
  → merge + memory update                               (MERGE + MEMORY)
```

---

## 5. Platform Architecture Map

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRAL MARKET PLATFORM                 │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React/Vite)  :5173                               │
│  ├── app/src/modules/auth/         → IAM, OAuth             │
│  ├── app/src/modules/expert/       → imCharts, imJournal,   │
│  │                                    imCopying             │
│  ├── app/src/modules/market/       → Market Intelligence    │
│  ├── app/src/modules/academy/      → Learning Platform      │
│  ├── app/src/modules/library/      → E-Library              │
│  └── app/src/shared/               → Design System, API     │
├─────────────────────────────────────────────────────────────┤
│  Market Backend (FastAPI)     :8000  → integralMarket.git   │
│  ├── IAM (auth, RBAC, OAuth)                                │
│  ├── Academy & Courses                                       │
│  ├── E-Library                                              │
│  ├── Notifications                                          │
│  └── Community                                              │
├─────────────────────────────────────────────────────────────┤
│  Expert Backend (FastAPI)     :8002  → integralMarket.git   │
│  ├── imJournal (trading journal + analytics)                │
│  ├── imCharts (charting, watchlists, execution)             │
│  ├── imCopying (copy trading, providers, signals)           │
│  ├── Broker Gateway (MT5, Binance, cTrader, etc.)          │
│  └── MT5 Sync Worker                                        │
├─────────────────────────────────────────────────────────────┤
│  Intelligence Backend (FastAPI)   :8003                     │
│  ├── Market Intelligence (AI analysis)                      │
│  ├── News + Sentiment                                        │
│  ├── Technical + Fundamental analysis                       │
│  └── Multi-source data aggregation                          │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure                                             │
│  ├── PostgreSQL (multi-schema: iam, journal, copy_trading,  │
│  │               broker_connections, imcharts, academy...)  │
│  ├── Redis :6380 (cache, pub/sub, rate limiting)            │
│  ├── Kong API Gateway                                       │
│  ├── Vite Proxy (dev: routes /api/v1/* to backends)        │
│  └── WebSocket (unified stream)                             │
├─────────────────────────────────────────────────────────────┤
│  AI Engineering Layer                                       │
│  ├── CodeGraph MCP (semantic AST index)                     │
│  ├── Graphify (knowledge graph, community detection)        │
│  ├── SpecKit (spec orchestration)                           │
│  └── software-factory/ (this repo — skills, memory, SDD)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Database Schema Ownership

| Schema              | Owner          | Backend      |
|---------------------|----------------|--------------|
| `iam`               | Market Backend | :8000        |
| `core`              | Market Backend | :8000        |
| `academy`           | Market Backend | :8000        |
| `library`           | Market Backend | :8000        |
| `community`         | Market Backend | :8000        |
| `notifications`     | Market Backend | :8000        |
| `journal`           | Expert Backend | :8002        |
| `copy_trading`      | Expert Backend | :8002        |
| `broker_connections`| Expert Backend | :8002        |
| `imcharts`          | Expert Backend | :8002        |
| `market_intelligence` | IMI Backend  | :8003        |
| `audit`             | All            | shared       |

---

## 7. Vite Proxy Routing (dev)

Expert backend routes (must precede catch-all `/api`):
- `/api/v1/brokers` → `:8002`
- `/api/v1/imcharts` → `:8002`
- `/api/v1/journal` → `:8002`
- `/api/v1/copy-trading` → `:8002`
- `/api/v1/signals` → `:8002`
- `/api/v1/bots` → `:8002`
- `/api/v1/gateway` → `:8002`
- `/api` → `:8000` (catch-all for market backend)

---

## 8. API Client Rules

```typescript
// src/shared/api/client.ts
// MARKET backend — always relative in dev (through Vite proxy → :8000)
const MARKET_API_URL = isDev ? '' : (env.VITE_MARKET_API_URL || 'http://localhost:8000')

// EXPERT backend — always relative in dev (through Vite proxy → :8002)
const EXPERT_API_URL = isDev ? '' : (env.VITE_EXPERT_API_URL || 'http://localhost:8002')
```

Never hardcode `localhost:800X` in frontend code.

---

## 9. Critical Never-Do Rules

```
NEVER:
  - bypass .specify/memory/constitution.md
  - create a SQLAlchemy model without checking for registry collisions
  - add a relationship without ForeignKey column declarations
  - hardcode base URLs in frontend (use isDev ? '' : env.VITE_*)
  - commit to venv/ directories
  - skip migrations when adding DB columns
  - create APIs without typed Pydantic schemas
  - create React components without TypeScript types
  - ignore RBAC implications of new endpoints
  - expose secrets or credentials in code
  - add CORS origins to code (use .env)
  - use `except Exception` without logging
  - create duplicate logic across services
  - violate schema ownership (e.g., expert backend touching iam.*)
```

---

## 10. Always-Do Rules

```
ALWAYS:
  - query CodeGraph before touching an existing file
  - check for naming conflicts in SQLAlchemy registry
  - add ForeignKey columns before defining relationships
  - wrap httpx calls in try/except (not just ValueError)
  - add global exception handlers to FastAPI apps
  - update specs after implementation
  - write tests alongside implementation
  - add monitoring hooks (metrics labels, structured logging)
  - use Zustand for global state, React Query for server state
  - generate migration files for schema changes
  - update software-factory/memory/ with decisions
  - run codegraph_impact() before changing shared utilities
```

---

## 11. Skill Activation Matrix

> **Automated routing:** `python3 software-factory/context-engine/skill_selector.py --query "<task>"`
> **Full index:** `software-factory/SKILLS_REGISTRY.md`
> **Create a new skill:** load `skills/skill-builder/SKILL.md` first

| Feature Area               | Skill File                                                   |
|----------------------------|--------------------------------------------------------------|
| **Create / audit a skill** | `skills/skill-builder/SKILL.md`                             |
| Product requirements / PRD | `skills/software-product-architect/SKILL.md`                |
| Architecture decisions     | `skills/architect-principal/SKILL.md`                       |
| Code review / refactoring  | `skills/software-developer/SKILL.md`                        |
| FastAPI endpoint            | `skills/backend-fastapi/SKILL.md`                           |
| React page / component      | `skills/frontend-react/SKILL.md`                            |
| Trading UI (imCharts/Journal/Copying) | `skills/frontend-trading-ui/SKILL.md`            |
| UI/UX design                | `skills/ui-ux-premium/SKILL.md`                             |
| Database schema / migration | `skills/database-postgresql/SKILL.md`                       |
| Docker / Podman / CI        | `skills/devops-engineer/SKILL.md`                           |
| Security audit              | `skills/security-audit/SKILL.md`                            |
| Structured logging / metrics| `skills/observability/SKILL.md`                             |
| Slow query / N+1 / cache    | `skills/performance-engineering/SKILL.md`                   |
| SEO / meta tags             | `skills/seo-optimizer/SKILL.md`                             |
| MT5 integration             | `skills/mt5-integration/SKILL.md`                           |
| MT5 scale / 10k+ users      | `skills/mt5-scalability/SKILL.md`                           |
| Copy trading engine         | `skills/copytrading-engine/SKILL.md`                        |
| Journal analytics           | `skills/journal-analytics/SKILL.md`                         |
| TradingView charts          | `skills/tradingview-integration/SKILL.md`                   |
| WebSocket / realtime        | `skills/websocket-realtime/SKILL.md`                        |
| Redis / rate limiting       | `skills/redis-streams/SKILL.md`                             |
| Domain events / sagas       | `skills/event-driven-architecture/SKILL.md`                 |
| Service boundaries / Kong   | `skills/microservices/SKILL.md`                             |
| Detect / document changes   | `skills/change-detective/SKILL.md`                          |
| Full-stack live debug       | `skills/interactive-dev/SKILL.md`                           |
| QA / product testing        | `skills/software-product-tester/SKILL.md`                   |
| LLM prompt design           | `skills/prompt-engineering/SKILL.md`                        |
| AI cost / model selection   | `skills/ai-optimization/SKILL.md`                           |
| Context compression / RAG   | `skills/context-engineering/SKILL.md`                       |
| Backtesting / quant models  | `skills/quant-research/SKILL.md`                            |
| API / E2E / unit tests      | `skills/testing-e2e/SKILL.md`                               |
| Load testing / SLA          | `skills/testing-load/SKILL.md`                              |

---

## 12. Recovery Protocol

If ANY step fails:
1. Read `software-factory/recovery/<failure-type>.md`
2. Execute the diagnosis tree
3. Replan if needed (do not abandon — replan)
4. Patch and retest
5. Log the incident in `software-factory/memory/patterns/`

---

## 13. Memory Update Protocol

After every significant implementation:

```bash
# Update architectural memory
echo "## $(date -I) — <feature>" >> software-factory/memory/decisions/<domain>.md
# Document: what changed, why, what alternatives were rejected
```

---

## 14. Context Engineering Protocol

For large tasks, compress context before sending to agent:

```bash
# Generate architecture snapshot
python3 software-factory/context-engine/snapshot.py --domain <domain>
# Retrieve only relevant specs
python3 software-factory/context-engine/retriever.py --query "<feature keywords>"
```

Send the compressed snapshot — not the full repo dump.

---

*This file is enforced by CI. Agents that violate these rules will have their
PRs auto-rejected by the validation pipeline.*
