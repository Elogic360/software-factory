# Memory Architecture for Architecture Discovery

**Purpose:** Enable cross-session, cross-agent awareness of discovered architecture  
**Scope:** Bounded contexts, patterns, decisions, violations, change history

---

## Memory System Structure

```
.specify/memory/
├── architecture/                 # Core architecture artifacts
│   ├── discovered-patterns.md    # Detected architecture style
│   ├── bounded-contexts.md       # DDD model (contexts, aggregates)
│   ├── data-flows.md             # Request sequences, domain events
│   ├── decisions.md              # Architectural decisions (ADRs)
│   ├── violations.md             # Known architecture breaches
│   ├── c4-definitions.json       # Cache: C4 level definitions
│   └── dependency-graph.json     # Cache: Dependency matrix
│
├── agent-logs/                   # Per-agent discovery records
│   ├── claude-2026-06.md         # What Claude discovered
│   ├── copilot-2026-06.md        # What Copilot found
│   ├── gemini-2026-06.md         # What Gemini added
│   └── summary.md                # Merged discovery results
│
└── cache/                        # Performance optimization
    ├── file-hashes.json          # Skip unchanged files
    ├── diagram-renders.json      # Pre-rendered SVG
    └── discovery-timestamp.txt   # Last run date
```

---

## Core Memory Files

### 1. `discovered-patterns.md`

**Updated:** Every discovery run  
**Purpose:** Detect new/changed architecture patterns

```markdown
---
agent: claude
timestamp: 2026-06-03T14:25:00Z
confidence: 0.92
---

# Discovered Patterns

## Primary: Microservices + DDD

**Confidence:** 92%

**Evidence:**
- 7 independent services (api-gateway, trading, portfolio, risk, auth, reporting, admin)
- Separate databases (trading_db, portfolio_db, auth_db)
- Message queue: RabbitMQ, async event handling
- Domain-driven structure: domain/, application/, infrastructure/ in each service

## Secondary: Event-Driven

**Confidence:** 88%

**Evidence:**
- Event handlers found (OrderCreatedHandler, TradeExecutedHandler)
- Message topics: orders, trades, positions, risk_alerts
- Event sourcing pattern in trading service

## Supporting: CQRS

**Confidence:** 75%

**Evidence:**
- Separate read/write paths in portfolio service
- ReadModel classes found
- Query and Command handlers (PlaceOrderCommand, GetPortfolioQuery)

## Architectural Violators

- ❌ Domain classes have database imports (should be persistence-agnostic)
- ❌ Circular dependency: OrderService ↔ PaymentService
- ⚠️ Shared database table accessed by 3 services (needs separate views)
```

---

### 2. `bounded-contexts.md`

**Updated:** When domain changes detected  
**Purpose:** Track DDD contexts, aggregates, repositories

```markdown
---
contexts_count: 5
aggregates_count: 12
last_verified: 2026-06-03
---

# DDD Bounded Contexts

## Context 1: Trading Engine
**Path:** `src/trading-service`  
**Responsibility:** Order execution, trade settlement, position tracking  
**Owner:** Trading Team

### Aggregates
- **Order (Root)**
  - Entities: OrderLine, ExecutionHistory
  - Value Objects: OrderId, Symbol, Quantity, Price
  - Repository: OrderRepository
  - Events: OrderCreated, OrderExecuted, OrderCancelled

- **Trade (Root)**
  - Entities: Execution
  - Value Objects: TradeId, Pair, Volume
  - Repository: TradeRepository
  - Events: TradeSettled, TradeRejected

### Repositories
- `OrderRepository`: Find by OrderId, by Symbol, by Status
- `TradeRepository`: Find by TradeId, by Symbol

### Domain Services
- `OrderExecutionService`: Matches and executes orders
- `SettlementService`: Coordinates trade settlement
- `PositionCalculator`: Computes live positions

### External Dependencies
- Broker API (FIX protocol)
- Market Data Feed (WebSocket)

---

## Context 2: Portfolio Management
**Path:** `src/portfolio-service`  
**Responsibility:** Portfolio composition, rebalancing, analytics  
**Owner:** Portfolio Team

### Aggregates
- **Portfolio (Root)**
  - Value Objects: PortfolioId, Currency
  - Entities: Holding (per asset)
  - Repository: PortfolioRepository

- **AllocationStrategy (Root)**
  - Value Objects: Target weights, rebalance thresholds
  - Repository: StrategyRepository

### Domain Services
- `RebalancingService`: Implements rebalancing logic
- `PerformanceCalculator`: P&L, Sharpe ratio, etc.

### External Dependencies
- Trading Engine (events: OrderExecuted, TradeSettled)
- Market Data (price feeds)

---

## Context 3: Risk Management
**Path:** `src/risk-service`  
**Responsibility:** Compliance, risk limits, alert generation

### Aggregates
- **RiskProfile (Root)**
  - Rules, limits, thresholds
  - Repository: RiskProfileRepository

### Domain Services
- `RiskEvaluator`: Check order against limits
- `AlertGenerator`: Create compliance alerts

### External Dependencies
- Trading Engine (events: OrderCreated)

---

## Context Interactions

```
Trading Engine
  ├─→ emits: OrderCreated, OrderExecuted, TradeSettled
  └─ receives: None

Portfolio Service
  ├─ listens: OrderCreated, OrderExecuted, TradeSettled
  ├─→ updates: Holdings, Performance
  └─ receives: None

Risk Service
  ├─ listens: OrderCreated
  ├─→ publishes: RiskViolation, ComplianceAlert
  └─ receives: None
```

---

## Coupling Analysis

| Interaction | Type | Async | Status |
|---|---|---|---|
| Trading → Portfolio | Event | Yes | ✓ Good |
| Trading → Risk | Event | Yes | ✓ Good |
| Portfolio → Trading | API Call | No | ⚠️ Tight coupling |
| Auth → Others | JWT | Implicit | ✓ Good |
```

---

### 3. `data-flows.md`

**Updated:** When flows change  
**Purpose:** Document key request/response paths

```markdown
---
last_updated: 2026-06-03
flows_documented: 8
---

# Data Flows & Sequences

## Flow 1: Place Trade Order

**Sequence:**
```
1. User → WebUI: "Buy 100 BTC at $45,000"
2. WebUI → API Gateway: POST /orders {symbol, qty, price}
3. API Gateway → Trading Service: PlaceOrderCommand
4. Trading Service → Risk Service: CheckRisk(order)
5. Risk Service → Trading Service: OK
6. Trading Service → Order Repository: Save Order (PENDING)
7. Trading Service → Broker API: Send Order (FIX)
8. Broker API → Trading Service: Order Confirmed
9. Trading Service → Event Bus: OrderCreated event
10. Portfolio Service: Listen → Update holdings
11. Trading Service → API Gateway: Order Created (200)
12. API Gateway → WebUI: Show confirmation
13. WebUI → User: "Order placed"
```

**Data Model:**
```
PlaceOrderCommand
├── symbol: "BTC-USD"
├── quantity: 100
├── price: 45000
└── userId: UUID

Order (created)
├── orderId: UUID
├── userId: UUID
├── symbol: "BTC-USD"
├── quantity: 100
├── price: 45000
├── status: "PENDING"
└── createdAt: ISO8601

OrderCreatedEvent
├── orderId: UUID
├── symbol: "BTC-USD"
└── quantity: 100
```

---

## Flow 2: Update Portfolio on Trade

**Trigger:** TradeSettledEvent from Trading Service

```
Event Bus receives: TradeSettledEvent
  ├─ Portfolio Service subscribes
  ├─ UpdateHoldingHandler triggered
  ├─ Query: SELECT * FROM holdings WHERE userId = ?
  ├─ Update quantity, cost basis
  ├─ Publish: HoldingUpdatedEvent
  └─ WebUI subscribes → real-time update

Caching:
  ├─ Holdings cached in Redis (5min TTL)
  ├─ On update: invalidate cache
  └─ Query hits database only on cache miss
```

---

## Flow 3: Risk Check on Order

**Trigger:** OrderCreatedEvent

```
Risk Service subscribes
  ├─ Load RiskProfile for user
  ├─ Evaluate: orderQty + openQty vs position_limit
  ├─ Evaluate: orderValue vs account_balance
  ├─ Evaluate: orderSymbol in restricted_list?
  ├─ If violation:
  │   └─ Publish: RiskViolationEvent
  ├─ Else:
  │   └─ Publish: RiskApprovedEvent
  └─ Trading Service may auto-cancel if violated
```
```

---

### 4. `decisions.md`

**Updated:** When architectural decisions made  
**Purpose:** Record ADRs, rationale, consequences

```markdown
---
adr_count: 7
last_decision: 2026-05-28
---

# Architecture Decisions (ADRs)

## ADR-001: Microservices Architecture

**Date:** 2026-05-15  
**Status:** Accepted  
**Author:** Architecture Team

### Context
Monolith reached 100K LOC. Deployment took 45 min. Team > 20 engineers, 3 product teams.

### Decision
Split into 7 independent microservices:
- Trading Engine (Python/FastAPI)
- Portfolio Service (Python/FastAPI)
- Risk Service (Go)
- Auth Service (Node.js)
- Market Data (Rust)
- Reporting (Python/Spark)
- Admin Panel (Node.js)

### Consequences

✓ **Positive:**
- Independent scaling per service
- 10 min deployment per service vs 45 min
- Clear team ownership (1-2 teams per service)
- Technology flexibility (Go for perf, Python for ML)

✗ **Negative:**
- Distributed transaction complexity
- Service-to-service latency (p99: 50-100ms)
- Operational overhead (7 services to monitor)
- Network partition risks

### Alternatives

**1. Modular Monolith**
- Rejected: Coupling issues remained in practice

**2. Serverless (AWS Lambda)**
- Rejected: Cold start (5-10s) unacceptable for trading

**3. Event Sourcing Everywhere**
- Rejected: Too complex, not all services need it

---

## ADR-002: Event-Driven Communication

**Date:** 2026-05-20  
**Status:** Accepted

### Context
Microservices need coordination without synchronous API calls.

### Decision
RabbitMQ with async event handlers.
- Orders → events: OrderCreated, OrderExecuted, OrderCancelled
- Trades → events: TradeSettled, TradeRejected
- Holdings → events: HoldingUpdated

### Consequences
✓ Loose coupling between services
✓ Natural audit trail (events immutable)
✗ Eventual consistency (challenging in trading)

---

## ADR-003: Separate Databases per Service

**Date:** 2026-05-25  
**Status:** Accepted

### Context
Monolith shared one DB. Scaling bottleneck.

### Decision
- Trading Service: PostgreSQL (ACID needed for orders)
- Portfolio Service: PostgreSQL
- Market Data: TimescaleDB (time-series)
- Cache: Redis (for fast queries)

### Consequences
✓ Independent scaling per service
✗ Distributed transactions impossible
✗ Harder to answer cross-context queries
✗ Schema sync challenges

### Mitigation
- Using read replicas and caching
- Event-driven sync for critical data
```

---

### 5. `violations.md`

**Updated:** Continuously (by living mode)  
**Purpose:** Track architecture breaches, TODOs

```markdown
---
critical: 2
warnings: 5
low: 3
last_scan: 2026-06-03T08:15:00Z
---

# Architecture Violations

## CRITICAL

### 1. Cyclic Dependency: OrderService ↔ PaymentService
**Severity:** CRITICAL  
**File:** `src/trading-service/src/domain/order.py`  
**Issue:** OrderService imports PaymentService; PaymentService imports OrderService  
**Impact:** Impossible to test independently  
**Owner:** Trading Team  
**Status:** In Progress (Refactor to use event)  
**Deadline:** 2026-06-15

### 2. Domain Layer Depends on Persistence
**Severity:** CRITICAL  
**File:** `src/trading-service/src/domain/order.py:45`  
**Issue:** `from src.infrastructure.persistence import pg`  
**Impact:** Domain not testable without database  
**Owner:** Trading Team  
**Status:** Needs Planning  
**Fix:** Apply repository pattern, inject interface

---

## WARNING

### 3. Shared Database Table (holdings)
**Severity:** WARNING  
**Issue:** `holdings` table accessed by Portfolio AND Trading service  
**Location:** `migrations/0045_shared_holdings.sql`  
**Impact:** Distributed transaction risk  
**Fix:** Create separate views per service, sync via events

### 4. WebSocket Missing Encryption
**Severity:** WARNING  
**Issue:** Real-time updates use plain WebSocket  
**File:** `src/websocket-realtime/src/ws_server.py`  
**Impact:** Trade data exposed on network  
**Fix:** Upgrade to WSS (WebSocket Secure), add mTLS

### 5. No Rate Limiting on API Gateway
**Severity:** WARNING  
**Issue:** DOS vulnerability  
**File:** `src/api-gateway/src/main.py`  
**Impact:** Service can be overwhelmed  
**Fix:** Add rate limiter middleware

---

## LOW

### 6. Test Coverage < 50% in Risk Service
### 7. Missing ADR for Redis Caching Strategy
### 8. Outdated Sequence Diagram (2 months old)
```

---

### 6. Cache: `c4-definitions.json`

```json
{
  "last_generated": "2026-06-03T08:15:00Z",
  "contexts": {
    "level1": {
      "name": "Trading System Context",
      "actors": ["Trader", "Risk Manager"],
      "systems": ["Trading Platform", "Broker API", "Market Data Feed"],
      "hash": "abc123def456"
    },
    "level2": {
      "containers": [
        {
          "name": "API Gateway",
          "technology": "FastAPI + Uvicorn",
          "port": 8000,
          "replicas": 3
        }
      ]
    }
  }
}
```

---

### 7. Cache: `dependency-graph.json`

```json
{
  "nodes": [
    {"id": "trading-service", "type": "service"},
    {"id": "portfolio-service", "type": "service"},
    {"id": "postgres", "type": "database"},
    {"id": "rabbitmq", "type": "infrastructure"}
  ],
  "edges": [
    {
      "from": "trading-service",
      "to": "postgres",
      "type": "persistent",
      "async": false
    },
    {
      "from": "trading-service",
      "to": "rabbitmq",
      "type": "event",
      "async": true
    }
  ],
  "violations": [
    {
      "type": "cyclic",
      "nodes": ["OrderService", "PaymentService"]
    }
  ]
}
```

---

## Memory Update Protocol

### When Agent Discovers Something New

1. **Read** existing memory files
2. **Merge** new findings with old
3. **Update** appropriate memory file(s)
4. **Commit** to git if significant
5. **Cache** for performance

### Example: Adding New ADR

```
Agent runs discovery → Detects new pattern
  ↓
Write to .specify/memory/architecture/decisions.md
  ↓
Add entry: "ADR-N: [Title]"
  ↓
Commit to software-factory/memory/decisions/ADR-N.md
  ↓
Update summary in decisions.md
  ↓
Next agent session has full history ✓
```

---

## Memory Lifecycle

| Age | Action |
|-----|--------|
| < 1 week | Use directly |
| 1-4 weeks | Validate with code scan |
| > 1 month | Re-run discovery to refresh |
| > 3 months | Full discovery recommended |

---

## Access Across Sessions

```
Session 1 (Claude):
  └─ discovers patterns
  └─ writes to .specify/memory/

Session 2 (Copilot):
  ├─ reads existing memory
  ├─ validates against code
  └─ updates with new findings

Session 3 (Gemini):
  ├─ reads both previous sessions
  ├─ identifies conflicts
  └─ merges intelligently
```

---

## Integration with SDD Pipeline

```
Feature spec created
  ↓
Call: /architect-discovery --check-impact
  ↓
Load: .specify/memory/architecture/
  ↓
Identify affected contexts & aggregates
  ↓
Flag violations that would result
  ↓
Recommend architecture changes
  ↓
Record in decisions.md if approved
```

---

## Maintenance

### Weekly
- Verify memory files still valid
- Check for stale ADRs

### Monthly
- Re-run discovery to catch changes
- Update violations list
- Archive old agent-logs

### Quarterly
- Full architecture re-assessment
- Update all C4 diagrams
- Review and update ADRs

