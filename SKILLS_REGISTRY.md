# Integral Market — Skills Registry
## Canonical Index of All Agentic Skills

> **This file is the single source of truth for the software-factory skill
> library.** Every agent session should reference this before loading any skill.
> Use `context-engine/skill_selector.py --query "<task>"` to auto-select skills.

---

## Quick Navigation

| # | Skill | Layer | Primary Use Case |
|---|-------|-------|-----------------|
| 1 | [skill-builder](#1-skill-builder) | Meta | Create / audit skills |
| 2 | [software-product-architect](#2-software-product-architect) | Product | PRDs, user stories, roadmap |
| 3 | [architect-principal](#3-architect-principal) | Architecture | ADRs, system design, service boundaries |
| 4 | [software-developer](#4-software-developer) | General | Code quality, debugging, refactoring |
| 5 | [backend-fastapi](#5-backend-fastapi) | Backend | FastAPI endpoints, SQLAlchemy, Pydantic |
| 6 | [database-postgresql](#6-database-postgresql) | Database | Schema, migrations, TimescaleDB, RBAC |
| 7 | [frontend-react](#7-frontend-react) | Frontend | React, TypeScript, Zustand, React Query |
| 8 | [frontend-trading-ui](#8-frontend-trading-ui) | Frontend | imCharts, imJournal, imCopying UI |
| 9 | [ui-ux-premium](#9-ui-ux-premium) | Design | Design tokens, glassmorphism, animations |
| 10 | [security-audit](#10-security-audit) | Security | Auth, CORS, JWT, RBAC, credential storage |
| 11 | [devops-engineer](#11-devops-engineer) | Infra | Docker, CI/CD, env vars, health checks |
| 12 | [observability](#12-observability) | Infra | Logging, Prometheus, Grafana, tracing |
| 13 | [performance-engineering](#13-performance-engineering) | Perf | Query optimization, caching, pagination |
| 14 | [seo-optimizer](#14-seo-optimizer) | Frontend | Meta tags, sitemap, Core Web Vitals |
| 15 | [mt5-integration](#15-mt5-integration) | Trading | MT5 bridge, broker adapters, sync worker |
| 16 | [copytrading-engine](#16-copytrading-engine) | Trading | Provider/subscriber, signal routing, risk |
| 17 | [journal-analytics](#17-journal-analytics) | Trading | Trade analytics, win rate, drawdown, Sharpe |
| 18 | [tradingview-integration](#18-tradingview-integration) | Trading | Lightweight Charts, OHLCV feed, markers |
| 19 | [websocket-realtime](#19-websocket-realtime) | Realtime | WS endpoints, ConnectionManager, pub/sub |
| 20 | [redis-streams](#20-redis-streams) | Infra | Consumer groups, rate limiting, cache patterns |
| 21 | [event-driven-architecture](#21-event-driven-architecture) | Arch | Domain events, event bus, saga pattern |
| 22 | [microservices](#22-microservices) | Arch | Service boundaries, Kong, inter-service comms |
| 23 | [prompt-engineering](#23-prompt-engineering) | AI | LLM prompts, structured output, model selection |
| 24 | [ai-optimization](#24-ai-optimization) | AI | Cost, latency, caching, streaming, evaluation |
| 25 | [context-engineering](#25-context-engineering) | AI | Context compression, retrieval, agent memory |
| 26 | [quant-research](#26-quant-research) | Quant | Backtesting, Sharpe, Monte Carlo, walk-forward |
| 27 | [testing-e2e](#27-testing-e2e) | Testing | Pytest, Playwright, factories, fixtures |
| 28 | [testing-load](#28-testing-load) | Testing | Locust, k6, SLA validation, bottlenecks |
| 29 | [change-detective](#29-change-detective) | DevProcess | Autonomous git diff analysis, auto-documentation |
| 30 | [interactive-dev](#30-interactive-dev) | DevProcess | Full-stack live debug — browser, backends, DB |
| 31 | [software-product-tester](#31-software-product-tester) | Testing | QA, accessibility, regression, bug reports |
| 32 | [mt5-scalability](#32-mt5-scalability) | Trading | 10k+ concurrent MT5 users, worker pools, Redis queue |

---

## Full Skill Profiles

---

### 1. skill-builder
**Path:** `skills/skill-builder/SKILL.md`
**Layer:** Meta
**Activation triggers:** create new skill, add skill, skill template, skill quality review, knowledge codification, agent knowledge base, extend software-factory, skill audit
**Depends on:** *(none — this is the root meta-skill)*
**Used by:** All skills (template source)
**Platform layers touched:** software-factory itself
**Example task:** "We need a skill for handling Stripe payments — create it."

---

### 2. software-product-architect
**Path:** `skills/software-product-architect/SKILL.md`
**Layer:** Product
**Activation triggers:** new feature request, product requirements, user story, acceptance criteria, feature scope, PRD, roadmap, MVP definition, feature prioritization, RICE score, persona, stakeholder alignment
**Depends on:** architect-principal
**Used by:** All implementation skills (provides spec before build)
**Platform layers touched:** specs/, memory/
**Example task:** "We want to add Telegram notifications — write the PRD."

---

### 3. architect-principal
**Path:** `skills/architect-principal/SKILL.md`
**Layer:** Architecture
**Activation triggers:** architecture decision, ADR, service design, system design, service boundary, scalability, schema ownership, dependency analysis, technical trade-off, monolith vs microservices
**Depends on:** software-product-architect
**Used by:** backend-fastapi, database-postgresql, microservices, event-driven-architecture
**Platform layers touched:** All services, software-factory/specs/
**Example task:** "Should the signal routing engine live in expert-backend or a separate service?"

---

### 4. software-developer
**Path:** `skills/software-developer/SKILL.md`
**Layer:** General
**Activation triggers:** code review, refactoring, debugging, code quality, naming convention, code smell, technical debt, guard clauses, extract function, git workflow, commit message
**Depends on:** *(none — general skill)*
**Used by:** All implementation skills
**Platform layers touched:** All source files
**Example task:** "Review this auth service for code smells before merging."

---

### 5. backend-fastapi
**Path:** `skills/backend-fastapi/SKILL.md`
**Layer:** Backend
**Activation triggers:** FastAPI endpoint, SQLAlchemy model, Pydantic schema, async route, dependency injection, exception handler, global handler, middleware, ORM relationship, registry collision, selectinload, mapped_column
**Depends on:** security-audit, database-postgresql
**Used by:** copytrading-engine, mt5-integration, journal-analytics, websocket-realtime
**Platform layers touched:** integral-expert-backend/, integral-market-backend/
**Example task:** "Add a POST endpoint for creating a watchlist in imCharts."

---

### 6. database-postgresql
**Path:** `skills/database-postgresql/SKILL.md`
**Layer:** Database
**Activation triggers:** alembic migration, schema design, TimescaleDB, hypertable, continuous aggregate, RBAC function, is_admin, index, ForeignKey, multi-schema, data migration, pg_dump
**Depends on:** architect-principal
**Used by:** backend-fastapi, journal-analytics, copytrading-engine
**Platform layers touched:** alembic/versions/, PostgreSQL schemas (iam, journal, copy_trading, imcharts, broker_connections)
**Example task:** "Add a daily_stats continuous aggregate for the journal schema."

---

### 7. frontend-react
**Path:** `skills/frontend-react/SKILL.md`
**Layer:** Frontend
**Activation triggers:** React component, TypeScript type, Zustand store, React Query, useQuery, useMutation, TanStack Query, custom hook, lazy loading, code splitting, module structure, barrel export
**Depends on:** ui-ux-premium
**Used by:** frontend-trading-ui, seo-optimizer
**Platform layers touched:** app/src/modules/, app/src/shared/
**Example task:** "Create the useProviders hook for the imCopying module."

---

### 8. frontend-trading-ui
**Path:** `skills/frontend-trading-ui/SKILL.md`
**Layer:** Frontend
**Activation triggers:** trading interface, chart panel, watchlist, journal entry, copy trading UI, provider card, trade history table, PnL display, broker account connection panel, positions table, order panel, signal feed
**Depends on:** frontend-react, ui-ux-premium, websocket-realtime
**Used by:** tradingview-integration
**Platform layers touched:** app/src/modules/expert/ (imCharts, imJournal, imCopying)
**Example task:** "Build the ProviderCard component with stats grid and subscribe button."

---

### 9. ui-ux-premium
**Path:** `skills/ui-ux-premium/SKILL.md`
**Layer:** Design
**Activation triggers:** new page design, component styling, design token, glassmorphism, dark mode, responsive layout, animation, accessibility, color system, GlassCard, gradient border, Tailwind, Framer Motion
**Depends on:** *(none — design is the foundation)*
**Used by:** frontend-react, frontend-trading-ui, seo-optimizer
**Platform layers touched:** app/src/shared/tokens/, app/src/shared/components/
**Example task:** "Design the account status badge component with connection state colors."

---

### 10. security-audit
**Path:** `skills/security-audit/SKILL.md`
**Layer:** Security
**Activation triggers:** JWT access token, refresh token rotation, bcrypt, account lockout, OAuth implementation, CORS configuration, rate limiting, SQL injection, security headers, credential storage, Fernet encryption, RBAC permission check
**Depends on:** *(none — security is cross-cutting)*
**Used by:** backend-fastapi, mt5-integration, devops-engineer
**Platform layers touched:** All backends, .env files
**Example task:** "Review the new OAuth flow for security — is redirect_uri safe?"

---

### 11. devops-engineer
**Path:** `skills/devops-engineer/SKILL.md`
**Layer:** Infra
**Activation triggers:** Dockerfile, docker-compose, CI pipeline, deployment, environment config, service startup, health check, scaling, GitHub Actions, env var, dev-start script
**Depends on:** security-audit
**Used by:** microservices, observability
**Platform layers touched:** docker-compose.yml, .github/workflows/, .env files
**Example task:** "Set up a GitHub Actions CI pipeline that runs pytest and pnpm build."

---

### 12. observability
**Path:** `skills/observability/SKILL.md`
**Layer:** Infra
**Activation triggers:** structured logging, metrics endpoint, Prometheus, Grafana, OpenTelemetry, distributed tracing, JSON logs, alert rule, Loki, health dashboard, performance monitoring
**Depends on:** devops-engineer
**Used by:** backend-fastapi, performance-engineering
**Platform layers touched:** Both backends (/metrics endpoint), monitoring/ directory
**Example task:** "Add Prometheus metrics to the copy trading signal routing endpoint."

---

### 13. performance-engineering
**Path:** `skills/performance-engineering/SKILL.md`
**Layer:** Perf
**Activation triggers:** slow query, N+1 problem, cache strategy, pagination, response time budget, database index, Redis cache, query explain, profiling, lazy loading, connection pool, selectinload, cursor pagination
**Depends on:** database-postgresql, redis-streams, observability
**Used by:** journal-analytics, frontend-react
**Platform layers touched:** All backends, PostgreSQL indexes, Redis cache layer
**Example task:** "The /journal/performance endpoint is taking 3s — optimize it."

---

### 14. seo-optimizer
**Path:** `skills/seo-optimizer/SKILL.md`
**Layer:** Frontend
**Activation triggers:** meta tags, Open Graph, sitemap, robots.txt, structured data, page title, canonical URL, Core Web Vitals, SSR, landing page SEO, search ranking, social sharing, SEOHead
**Depends on:** frontend-react, ui-ux-premium
**Used by:** *(none — leaf skill)*
**Platform layers touched:** app/src/, integral-market-backend/app/api/ (sitemap endpoint)
**Example task:** "Add SEO meta tags and structured data to the Academy course pages."

---

### 15. mt5-integration
**Path:** `skills/mt5-integration/SKILL.md`
**Layer:** Trading
**Activation triggers:** MT5 connection, trade sync, broker adapter, execution gateway, position management, order placement, BrokerRegistry, MT5 Windows bridge, sync worker, APScheduler, Fernet encrypted credentials
**Depends on:** backend-fastapi, security-audit
**Used by:** copytrading-engine, journal-analytics, frontend-trading-ui
**Platform layers touched:** integral-expert-backend/app/services/integrations/, integral-expert-backend/app/workers/
**Example task:** "The MT5 sync worker is failing silently — add proper retry and logging."

---

### 16. copytrading-engine
**Path:** `skills/copytrading-engine/SKILL.md`
**Layer:** Trading
**Activation triggers:** copy trading, provider registration, subscription, signal routing, risk limits, performance tracking, execution log, CopySubscription, ProviderSignal, copy_ratio, drawdown check, lot size
**Depends on:** backend-fastapi, mt5-integration, event-driven-architecture
**Used by:** frontend-trading-ui, journal-analytics
**Platform layers touched:** integral-expert-backend/app/models/copy_trading/, copy_trading schema
**Example task:** "Add a symbol filter to the risk engine so subscribers can block XAUUSD."

---

### 17. journal-analytics
**Path:** `skills/journal-analytics/SKILL.md`
**Layer:** Trading
**Activation triggers:** trading journal, trade analytics, performance metrics, win rate, profit factor, Sharpe ratio, drawdown calculation, equity curve, calendar heatmap, trade annotation, journal entry, TimescaleDB continuous aggregate
**Depends on:** database-postgresql, performance-engineering
**Used by:** frontend-trading-ui, tradingview-integration, quant-research
**Platform layers touched:** integral-expert-backend/app/services/journal/, journal schema
**Example task:** "Add a calendar heatmap data endpoint showing daily PnL by date."

---

### 18. tradingview-integration
**Path:** `skills/tradingview-integration/SKILL.md`
**Layer:** Trading
**Activation triggers:** TradingView chart, custom data feed, OHLCV bars, chart widget, symbol search, order markers, Lightweight Charts, charting configuration, candlestick, equity curve chart
**Depends on:** frontend-react, journal-analytics
**Used by:** frontend-trading-ui
**Platform layers touched:** app/src/modules/expert/imCharts/, integral-expert-backend/app/api/v1/endpoints/imcharts.py
**Example task:** "Add buy/sell markers on the equity curve chart for each closed trade."

---

### 19. websocket-realtime
**Path:** `skills/websocket-realtime/SKILL.md`
**Layer:** Realtime
**Activation triggers:** WebSocket endpoint, live price feed, real-time positions, signal streaming, notification push, pub/sub channel, Redis streams, connection management, reconnection logic, ConnectionManager, useExpertWS
**Depends on:** backend-fastapi, redis-streams, security-audit
**Used by:** frontend-trading-ui, copytrading-engine
**Platform layers touched:** integral-expert-backend/app/api/v1/ws/, app/src/shared/ws/
**Example task:** "Stream live position updates to the frontend without polling."

---

### 20. redis-streams
**Path:** `skills/redis-streams/SKILL.md`
**Layer:** Infra
**Activation triggers:** Redis streams, consumer groups, rate limiting, session cache, Redis pub/sub, message queue, job queue, leaky bucket, token bucket, Redis data structures, xadd, xreadgroup, xack
**Depends on:** devops-engineer
**Used by:** websocket-realtime, event-driven-architecture, performance-engineering
**Platform layers touched:** app/core/redis.py, app/core/rate_limiter.py (both backends)
**Example task:** "Implement sliding window rate limiting for the broker connect endpoint."

---

### 21. event-driven-architecture
**Path:** `skills/event-driven-architecture/SKILL.md`
**Layer:** Architecture
**Activation triggers:** domain event, event bus, pub/sub architecture, CQRS, saga pattern, event sourcing, async workflow, decoupled service communication, DomainEvent, fan-out, at-least-once delivery
**Depends on:** redis-streams, architect-principal
**Used by:** copytrading-engine, websocket-realtime
**Platform layers touched:** integral-expert-backend/app/core/events.py, app/sagas/
**Example task:** "Decouple signal routing from the HTTP request path using domain events."

---

### 22. microservices
**Path:** `skills/microservices/SKILL.md`
**Layer:** Architecture
**Activation triggers:** new service, service boundary, inter-service call, API gateway, Kong, service discovery, microservice design, service contract, service decomposition, internal API, ServiceClient
**Depends on:** architect-principal, devops-engineer, security-audit
**Used by:** *(applies to all services)*
**Platform layers touched:** kong/, docker-compose.yml, all backend services
**Example task:** "Should IMI backend call the expert backend directly, or use an event?"

---

### 23. prompt-engineering
**Path:** `skills/prompt-engineering/SKILL.md`
**Layer:** AI
**Activation triggers:** LLM integration, AI feature, prompt template, agent design, context window, few-shot examples, chain-of-thought, structured output, function calling, market intelligence AI, tool use, system prompt
**Depends on:** context-engineering, ai-optimization
**Used by:** ai-optimization, context-engineering
**Platform layers touched:** integral-imi-backend/app/services/ai/, software-factory/prompts/
**Example task:** "Design the system prompt for the journal AI coach feature."

---

### 24. ai-optimization
**Path:** `skills/ai-optimization/SKILL.md`
**Layer:** AI
**Activation triggers:** AI pipeline, LLM inference cost, model selection, caching AI responses, streaming, batching, quality evaluation, A/B testing prompts, AI feature scaling, claude-haiku, claude-opus, claude-sonnet, SSE stream
**Depends on:** prompt-engineering, redis-streams
**Used by:** *(leaf AI skill)*
**Platform layers touched:** integral-imi-backend/app/services/ai/, Redis cache layer
**Example task:** "The market analysis AI is costing $800/month — optimize model selection."

---

### 25. context-engineering
**Path:** `skills/context-engineering/SKILL.md`
**Layer:** AI
**Activation triggers:** context window, token budget, agent memory, information retrieval, context snapshot, session compression, RAG, semantic search, long conversation, context overflow, snapshot.py, retriever.py
**Depends on:** prompt-engineering
**Used by:** skill-builder (when loading context for a session)
**Platform layers touched:** software-factory/context-engine/
**Example task:** "Generate a compressed architecture snapshot of the copy_trading domain."

---

### 26. quant-research
**Path:** `skills/quant-research/SKILL.md`
**Layer:** Quant
**Activation triggers:** trading strategy, backtest, alpha signal, statistical analysis, risk-adjusted return, Monte Carlo, walk-forward analysis, strategy optimization, quant model, Sharpe ratio, profit factor, drawdown simulation
**Depends on:** journal-analytics, performance-engineering
**Used by:** *(leaf quant skill)*
**Platform layers touched:** integral-imi-backend/app/services/quant/
**Example task:** "Backtest the RSI mean-reversion strategy on EURUSD daily data."

---

### 27. testing-e2e
**Path:** `skills/testing-e2e/SKILL.md`
**Layer:** Testing
**Activation triggers:** test writing, API test, end-to-end test, Playwright, pytest, test fixture, mock, factory pattern, coverage report, CI test pipeline, pytest-asyncio, AsyncClient, factory_boy
**Depends on:** backend-fastapi, frontend-react
**Used by:** *(leaf testing skill)*
**Platform layers touched:** tests/, e2e/
**Example task:** "Write integration tests for the new copy trading subscription endpoint."

---

### 28. testing-load
**Path:** `skills/testing-load/SKILL.md`
**Layer:** Testing
**Activation triggers:** load test, performance benchmark, concurrent users, throughput, Locust, k6, capacity planning, stress test, spike test, bottleneck, latency under load, SLA validation, P99
**Depends on:** performance-engineering, observability
**Used by:** *(leaf testing skill)*
**Platform layers touched:** tests/load/
**Example task:** "Load test the broker positions endpoint at 100 concurrent users."

---

### 29. change-detective
**Path:** `skills/change-detective/SKILL.md`
**Layer:** DevProcess
**Activation triggers:** change detection, detect changes, what changed, diff analysis, auto-document, schema drift, API drift, type drift, undocumented change, changelog, audit trail, memory update, codebase drift, breaking change, regression risk
**Depends on:** *(none — observes git history)*
**Used by:** software-developer, testing-e2e, devops-engineer
**Platform layers touched:** software-factory/memory/, git history
**Example task:** "Detect and document all changes since the last merge to main."

---

### 30. interactive-dev
**Path:** `skills/interactive-dev/SKILL.md`
**Layer:** DevProcess
**Activation triggers:** interactive dev, live debugging, full-stack debug, run all services, capture logs, browser logs, backend logs, postgres logs, reproduce bug, end-to-end debug, dev runner, watch mode, hot reload, inspect network, inspect error, dev session, stack trace, frontend error, backend error
**Depends on:** devops-engineer, software-product-tester
**Used by:** All implementation skills (debugging support)
**Platform layers touched:** All running services, browser, PostgreSQL logs
**Example task:** "Run the full stack and capture the error logs when the broker connect fails."

---

### 31. software-product-tester
**Path:** `skills/software-product-tester/SKILL.md`
**Layer:** Testing
**Activation triggers:** product testing, software testing, QA, test plan, regression test, bug report, bug reproduction, acceptance test, UAT, UI test, browser test, API test, integration test, smoke test, accessibility, a11y, WCAG, cross-browser, visual regression, test coverage, playwright, pytest, locust, write tests, verify this works
**Depends on:** testing-e2e, testing-load, interactive-dev
**Used by:** *(quality gate across all layers)*
**Platform layers touched:** tests/, e2e/, all service endpoints
**Example task:** "Write the full QA test plan for the Google OAuth login flow."

---

### 32. mt5-scalability
**Path:** `skills/mt5-scalability/SKILL.md`
**Layer:** Trading
**Activation triggers:** MT5 scalability, metatrader5 scale, 10000 users, concurrent MT5, broker connection pool, MT5 worker, MT5 queue, MT5 sync, MT5 bridge, trading account sync, copy trading scale, broker gateway scale, MT5 connection limit, MT5 horizontal scaling, Redis queue MT5, WebSocket MT5, position sync, order sync, MT5 circuit breaker
**Depends on:** mt5-integration, redis-streams, websocket-realtime, devops-engineer
**Used by:** copytrading-engine, frontend-trading-ui
**Platform layers touched:** integral-expert-backend/app/workers/, broker_connections schema, Redis queue
**Example task:** "Scale the MT5 sync worker to handle 10,000 concurrent broker accounts."

---

## Skill Dependency Graph

```
                    [skill-builder] ← meta, creates all others
                          │
              ┌───────────┼───────────────┐
              ▼           ▼               ▼
    [software-product]  [architect]  [software-developer]
         │                 │
         └────────┬────────┘
                  ▼
        ┌─────────────────────────────────────────────┐
        │          PLATFORM LAYER                      │
        │  [backend-fastapi]  [database-postgresql]    │
        │  [frontend-react]   [security-audit]         │
        │  [devops-engineer]  [ui-ux-premium]          │
        └─────────────────────────────────────────────┘
                  │
        ┌─────────┼──────────────────────────────────────┐
        ▼         ▼              ▼               ▼        ▼
  [observability] [redis-streams] [perf-eng] [seo] [frontend-trading-ui]
        │               │
        └───────────────┼──────────────────────────────────┐
                        ▼                                  ▼
              [event-driven-arch]               [websocket-realtime]
                        │                                  │
              ┌─────────┘                     ┌────────────┘
              ▼                               ▼
  [microservices]                  [copytrading-engine]
                                             │
                          ┌──────────────────┼─────────────────────┐
                          ▼                  ▼                     ▼
               [mt5-integration]   [journal-analytics]   [tradingview-integration]
                                             │
                                   [quant-research]
                          ┌──────────────────────────┐
                          ▼                          ▼
               [testing-e2e]              [testing-load]
                          │                          │
               [software-product-tester]─────────────┘
                          │
                [interactive-dev] ←→ [change-detective]
                          ┌──────────────────────────┐
                          ▼                          ▼
               [prompt-engineering]       [ai-optimization]
                          │
                [context-engineering]

              [mt5-scalability]
                  (depends on: mt5-integration, redis-streams,
                   websocket-realtime, devops-engineer)
```

---

## Using This Registry

```bash
# Find the right skill for a task (automated)
python3 software-factory/context-engine/skill_selector.py \
  --query "add WebSocket live position updates to imCharts"
# Output: [websocket-realtime ★★★★★] [frontend-trading-ui ★★★☆☆] [redis-streams ★★☆☆☆]

# Load a skill's full content for an agent session
cat software-factory/skills/websocket-realtime/SKILL.md

# Load multiple skills
for skill in websocket-realtime redis-streams frontend-trading-ui; do
  echo "=== $skill ===" && cat software-factory/skills/$skill/SKILL.md
done
```

---

## Registry Maintenance

This file must be updated whenever:
- A new skill is added to `skills/`
- A skill's domain or activation triggers change
- A skill is deprecated or merged

**Owner:** The engineer who modifies `skills/` is responsible for updating this registry in the same commit.

**Automation:** The AUTO-SYNC block below is regenerated after every commit by the
`post-commit` git hook (`scripts/update_skills.py`). It auto-maps changed code
domains to the skills that own them and flags new domains that need a new skill —
so the library grows and self-modifies as the project grows. Install the hook with
`bash software-factory/scripts/install_hooks.sh`.

<!-- AUTO-SYNC:START -->
## Auto-Sync Status

> This block is regenerated by `scripts/update_skills.py` (wired to the git
> post-commit hook). It tracks how the skill library is auto-scaling with the
> codebase. Do not edit by hand — changes here are overwritten.

- **Last sync:** 2026-05-31 05:35 UTC
- **Commit range:** `66c5599b2a6c3f3e29b7dd77e45f56bce3d3768e..c72ae0e0`
- **Files changed:** 216
- **Breaking changes:** 9
- **Graph:** skipped

### Skills to review (auto-mapped from changed domains)

| Skill | Files touched | Examples |
|-------|---------------|----------|
| `backend-fastapi` | 87 | integral-expert-backend/.env, integral-expert-backend/.env.example, integral-expert-backend/README.md … |
| `copytrading-engine` | 60 | integral-expert-backend/.env, integral-expert-backend/.env.example, integral-expert-backend/README.md … |
| `mt5-integration` | 60 | integral-expert-backend/.env, integral-expert-backend/.env.example, integral-expert-backend/README.md … |
| `frontend-react` | 36 | app/src/core/router/AppRouter.tsx, app/src/core/services/gateway/UnifiedWebSocket.ts, app/src/modules/academy/AcademyRouter.tsx … |
| `ui-ux-premium` | 34 | app/src/modules/academy/AcademyRouter.tsx, app/src/modules/academy/pages/AcademyPage.tsx, app/src/modules/academy/pages/CoursesPage.tsx … |
| `security-audit` | 27 | integral-market-backend/.env, integral-market-backend/README.md, integral-market-backend/app/__pycache__/main.cpython-312.pyc … |
| `frontend-trading-ui` | 24 | app/src/modules/expert/ExpertRouter.tsx, app/src/modules/expert/api/imcharts.api.ts, app/src/modules/expert/api/journal.api.ts … |
| `journal-analytics` | 24 | app/src/modules/expert/ExpertRouter.tsx, app/src/modules/expert/api/imcharts.api.ts, app/src/modules/expert/api/journal.api.ts … |
| `tradingview-integration` | 24 | app/src/modules/expert/ExpertRouter.tsx, app/src/modules/expert/api/imcharts.api.ts, app/src/modules/expert/api/journal.api.ts … |
| `change-detective` | 3 | schema_files/05_journal.sql, schema_files/10_broker_connections.sql, schema_files/12_journal_enhancements.sql |
| `database-postgresql` | 3 | schema_files/05_journal.sql, schema_files/10_broker_connections.sql, schema_files/12_journal_enhancements.sql |
| `architect-principal` | 2 | app/src/core/router/AppRouter.tsx, app/src/core/services/gateway/UnifiedWebSocket.ts |
| `devops-engineer` | 2 | docker-compose.prod.yml, docker-compose.yml |
| `microservices` | 2 | docker-compose.prod.yml, docker-compose.yml |

*New domains with no owning skill are candidates for `skill-builder` to codify
into a new SKILL.md — keeping the library growing as the project grows.*
<!-- AUTO-SYNC:END -->
