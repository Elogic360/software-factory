# INTEGRAL MARKET — ENGINEERING CONSTITUTION
## Supreme Engineering Law · Version 1.0

> This document is the non-negotiable governance layer for all engineering
> decisions. Every AI agent, every human engineer, every CI pipeline must
> comply. Constitution changes require explicit human approval.

---

## ARTICLE I — SERVICE BOUNDARIES

### I.1 Backend Ownership

Each backend owns exactly one set of database schemas. Cross-schema reads via
JOIN are permitted only through shared DB functions. Cross-schema writes are
FORBIDDEN — use events or API calls.

```
Market Backend (:8000)   → iam, core, academy, library, community, notifications
Expert Backend (:8002)   → journal, copy_trading, broker_connections, imcharts
IMI Backend    (:8003)   → market_intelligence
Shared                   → audit, public
```

### I.2 API Versioning

All routes MUST be versioned under `/api/v1/`. New incompatible changes
introduce `/api/v2/`. Never break v1 without a deprecation window.

### I.3 Frontend Module Boundaries

Each module in `app/src/modules/<domain>/` owns its:
- pages, components, hooks, store, api, types, utils

Shared utilities go in `app/src/shared/`. Never import from another module's
internals — use `index.ts` exports only.

---

## ARTICLE II — NAMING CONVENTIONS

### II.1 Python (Backends)

```python
# Files: snake_case
auth_service.py
copy_trading_router.py

# Classes: PascalCase
class CopySubscription(Base): ...     # NOT "Subscription" — check registry!
class BrokerRegistry: ...

# Functions: snake_case
async def get_current_user() -> User: ...

# Constants: SCREAMING_SNAKE
MAX_FAILED_LOGIN_ATTEMPTS = 5

# SQLAlchemy models: ALWAYS unique names across ALL models in the registry
# Prefix domain if collision risk: CopySubscription, UserSubscription
```

### II.2 TypeScript (Frontend)

```typescript
// Files: camelCase for hooks/utils, PascalCase for components
useAuthStore.ts
BrokerSettingsModal.tsx
imcharts.api.ts

// Components: PascalCase
function AccountPill() {}

// Hooks: usePascalCase
function useBrokerAccounts() {}

// Types/Interfaces: PascalCase
interface BrokerAccount { id: string; display_name: string; }

// Zustand stores: useDomainStore
const useBrokerAccountStore = create<BrokerAccountState>()(...)

// API clients: domainApiClient
export const expertApiClient = new ApiClient(EXPERT_API_URL)
```

### II.3 Database

```sql
-- Tables: schema.snake_case_plural
journal.trades
copy_trading.subscriptions
broker_connections.accounts

-- Columns: snake_case
user_id, created_at, is_active, broker_type_id

-- Functions: schema.verb_noun_noun
iam.get_user_permissions(uid)
iam.is_admin(uid)

-- Indexes: idx_table_column(s)
idx_trades_user_id_created_at

-- Foreign keys: fk_table_ref_table
fk_subscriptions_provider_id
```

---

## ARTICLE III — CODING STANDARDS

### III.1 Python

```python
# Always use type hints
async def create_token_pair(self, user: User, ip_address: Optional[str] = None) -> Tuple[str, str, int]:

# Always use structured logging
import logging
logger = logging.getLogger(__name__)
logger.info("Token created", extra={"user_id": str(user.id)})

# Catch specific exceptions — never bare except
try:
    result = await httpx_client.post(url, data=payload)
except httpx.TimeoutException:
    raise HTTPException(503, "Upstream timeout")
except httpx.ConnectError:
    raise HTTPException(503, "Upstream unavailable")
except ValueError as e:
    raise HTTPException(400, str(e))

# Always await DB commits after mutations
await db.commit()
await db.refresh(entity)

# SQLAlchemy: always declare ForeignKey columns before relationships
provider_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("copy_trading.providers.id", ondelete="CASCADE"),
    nullable=False,
)
provider: Mapped["Provider"] = relationship("Provider", back_populates="snapshots")
```

### III.2 TypeScript / React

```typescript
// All API calls through typed client — never raw fetch()
const accounts = await expertApiClient.get<BrokerAccount[]>('/api/v1/brokers/accounts')

// Server state: React Query
const { data, isLoading, error } = useQuery({
  queryKey: ['brokers', 'accounts'],
  queryFn: () => expertApiClient.get('/api/v1/brokers/accounts'),
  gcTime: 600_000,
})

// Global UI state: Zustand with persist
const useBrokerAccountStore = create<BrokerAccountState>()(
  devtools(persist((set) => ({ ... }), { name: 'im-active-broker', version: 1 }))
)

// Components: always typed props
interface Props { accountId: string | null; onConnect: () => void; }
function AccountPill({ accountId, onConnect }: Props) {}

// Never use `any` — use `unknown` then narrow
function handleError(err: unknown) {
  const msg = err instanceof ApiClientError ? err.message : String(err)
}
```

---

## ARTICLE IV — SECURITY REQUIREMENTS

### IV.1 Authentication & Authorization

- All protected endpoints MUST use `Depends(get_current_active_user)`
- All admin endpoints MUST additionally check `Depends(require_role("admin"))`
- JWT tokens expire in 30 minutes; refresh tokens rotate on every use
- Passwords hashed with bcrypt (cost factor ≥ 12)
- OAuth codes are single-use; exchange immediately
- Rate limiting on all auth endpoints: 20 req/5min

### IV.2 Data Protection

- Broker credentials encrypted with Fernet (AES-256) before storage
- Never log credentials, tokens, or PII
- All DB connections use parameterized queries — no string formatting
- Environment variables for all secrets — never hardcode
- CORS origins in .env only — never in source code

### IV.3 API Security

- Input validation via Pydantic schemas (no raw dict access)
- File uploads: validate MIME type and size server-side
- SQL: use SQLAlchemy text() with bound parameters only
- All foreign key relationships verified before cross-user data access

---

## ARTICLE V — PERFORMANCE BUDGETS

| Metric                      | Budget          |
|-----------------------------|-----------------|
| API p99 latency (market)    | < 200ms         |
| API p99 latency (expert)    | < 500ms         |
| WebSocket message delivery  | < 50ms          |
| React initial load (LCP)    | < 2.5s          |
| React bundle (gzipped)      | < 500KB initial |
| DB query (single entity)    | < 10ms          |
| DB query (list, indexed)    | < 50ms          |
| Redis cache hit rate        | > 80%           |
| MT5 sync latency            | < 2s            |

### V.1 Query Rules

- Never load a relationship with `lazy="select"` in a list endpoint — use `selectinload()`
- Always paginate list endpoints (default 50, max 200)
- Index all FK columns and all query predicate columns
- Cache hot reads in Redis with appropriate TTL

---

## ARTICLE VI — OBSERVABILITY STANDARDS

### VI.1 Logging

Every service must emit structured JSON logs:

```python
logger.info("Order executed", extra={
    "service": "expert-backend",
    "domain": "copy_trading",
    "user_id": str(user.id),
    "order_id": str(order.id),
    "duration_ms": elapsed,
})
```

### VI.2 Metrics

All endpoints must record:
- `http_requests_total{path, status}`
- `http_request_duration_seconds{path}`
- Domain-specific counters (trades_executed_total, signals_delivered_total, etc.)

### VI.3 Health Checks

Every service exposes `/health` returning:
```json
{ "status": "healthy|degraded|unhealthy", "checks": { ... }, "version": "x.y.z" }
```

---

## ARTICLE VII — TESTING REQUIREMENTS

| Layer              | Minimum Coverage | Tool           |
|--------------------|------------------|----------------|
| Unit tests         | 80%              | pytest/vitest  |
| Integration tests  | Critical paths   | pytest + httpx |
| E2E tests          | Core user flows  | Playwright     |
| Load tests         | Before release   | k6             |

### VII.1 Test Rules

- Every new API endpoint needs an integration test
- Every new React page needs at least a smoke test
- Tests run in CI — failing tests block merge
- Mock external services (Google OAuth, MT5, broker APIs) in tests
- Use fixtures for DB setup/teardown — never test against production

---

## ARTICLE VIII — MIGRATION RULES

### VIII.1 Database Changes

```
MANDATORY PROCESS:
1. Write migration SQL in schema_files/<NN>_<description>.sql
2. Generate Alembic version: alembic revision --autogenerate -m "<desc>"
3. Review generated migration — never auto-apply without review
4. Test migration on dev DB first
5. Ensure rollback SQL exists
6. Never DROP columns — soft-delete with is_active/deleted_at
7. Always add indexes for new FK columns
```

### VIII.2 API Changes

- Breaking changes require new version (`/api/v2/`)
- Non-breaking additions are backward compatible
- Deprecate with `X-Deprecated: true` response header
- Give 30-day deprecation notice before removal

---

## ARTICLE IX — BRANCHING STRATEGY

```
main          → production-ready, protected
develop       → integration branch
feature/<id>-<slug>   → feature branches (from develop)
fix/<id>-<slug>       → bug fixes (from develop or main)
hotfix/<slug>         → critical production fixes (from main)
```

All PRs require:
- [ ] Constitution compliance check
- [ ] Tests passing
- [ ] TypeScript compile clean
- [ ] No new `any` types
- [ ] Memory/specs updated
- [ ] Reviewed by at least 1 human

---

## ARTICLE X — AI AGENT BEHAVIOR

### X.1 Agent Obligations

Every AI agent MUST:
1. Read this constitution before any implementation
2. Query CodeGraph for structural context
3. Load the relevant skill file
4. Propose a plan before implementing (for changes > 50 lines)
5. Implement incrementally with validation gates
6. Never violate service boundaries
7. Never commit to venv/, __pycache__, node_modules/
8. Log architectural decisions in software-factory/memory/

### X.2 Agent Prohibitions

Every AI agent MUST NOT:
- Invent database schemas without schema_files SQL
- Create SQLAlchemy models with duplicate registry names
- Add relationships without ForeignKey columns
- Hardcode localhost URLs in frontend code
- Use `except Exception: pass` silently
- Create files outside their domain ownership
- Make breaking API changes without versioning
- Touch .env files (read config.py patterns only)

### X.3 Escalation Triggers

Stop and ask a human when:
- Schema change would delete/rename existing columns
- Security model change (new permission types, RBAC restructure)
- New external service integration (billing, payment)
- Architecture change affecting multiple service boundaries
- Performance degradation > 20% detected in benchmarks

---

*Constitution ratified: 2026-05-25 | Owner: Elogic360 | Review cycle: quarterly*
