# Universal Project Scaffold System

**Version:** 1.0  
**Purpose:** Build ANY project from zero using AI agents, with auto-discovery and scaling capability

---

## Core Concept

Instead of discovering existing architecture, **this system lets you BUILD new projects** with proper architecture from day 1.

```
Choose Project Type
    ↓
Select Scale (solo, team, enterprise)
    ↓
Choose Tech Stack
    ↓
Auto-generate Scaffold
    ↓
Initialize with Agent
    ↓
Get Live Architecture Documentation
```

---

## Project Types Supported

### Type 1: REST API Service
```
scaffold/rest-api/
├── src/
│   ├── domain/           # Business logic
│   ├── application/      # Use cases
│   ├── infrastructure/   # Database, external APIs
│   └── presentation/     # Controllers
├── tests/
├── deployments/
└── docs/
```

### Type 2: Full-Stack Web Application
```
scaffold/fullstack-web/
├── backend/
│   ├── src/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── presentation/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── hooks/
│   └── tests/
├── shared/
└── deployments/
```

### Type 3: Microservices System
```
scaffold/microservices/
├── services/
│   ├── api-gateway/
│   ├── service-1/
│   ├── service-2/
│   └── service-3/
├── shared/
├── infrastructure/
├── deployments/
└── docs/
```

### Type 4: Real-Time System (Trading, Gaming, Chat)
```
scaffold/realtime/
├── backend/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   │   └── websocket/
│   │   └── message-queue/
│   └── presentation/
├── frontend/
├── shared/
├── deployments/
└── docs/
```

### Type 5: Data Pipeline / Analytics
```
scaffold/data-pipeline/
├── src/
│   ├── extractors/       # Data sources
│   ├── transformers/     # ETL logic
│   ├── loaders/          # Data sinks
│   ├── validators/       # Quality checks
│   └── orchestrators/    # DAGs, workflows
├── dags/                 # Airflow DAGs
├── tests/
├── deployments/
└── docs/
```

### Type 6: Machine Learning System
```
scaffold/ml-system/
├── src/
│   ├── data/             # Data pipelines
│   ├── features/         # Feature engineering
│   ├── models/           # ML models
│   ├── training/         # Training loops
│   ├── inference/        # Prediction service
│   └── evaluation/       # Metrics, tests
├── notebooks/            # Exploratory notebooks
├── experiments/          # Experiment tracking
├── tests/
├── deployments/
└── docs/
```

### Type 7: Multi-Tenant SaaS Platform
```
scaffold/saas-platform/
├── backend/
│   ├── domain/
│   │   ├── tenant/       # Multi-tenancy logic
│   │   ├── billing/      # Subscription
│   │   └── ...
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
├── frontend/
├── admin-dashboard/
├── deployments/
└── docs/
```

### Type 8: Mobile App (Backend)
```
scaffold/mobile-backend/
├── src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── presentation/
│   │   └── mobile/       # Mobile-specific endpoints
│   └── auth/             # Push notifications
├── tests/
├── deployments/
└── docs/
```

---

## Scale Levels

### Level 1: Solo Developer (1 Person)
**Use When:** MVP, prototype, personal project

```
memory/
├── decisions.md          # 3-5 decisions
├── patterns.md           # Single architecture pattern
└── violations.md         # Minor issues (optional)

docs/
└── architecture/
    ├── REPOSITORY_MAP.md
    └── ARCHITECTURE_ANALYSIS.md
```

**Discovery Phases Used:** 1, 2, 4 (quick C4)  
**Cadence:** Monthly  
**Memory Size:** < 100KB

---

### Level 2: Small Team (2-5 Developers)
**Use When:** Early startup, small product team

```
memory/
├── architecture/
│   ├── discovered-patterns.md
│   ├── bounded-contexts.md
│   ├── decisions.md         # 10-20 ADRs
│   └── violations.md
├── agent-logs/
│   ├── team-member-1.md
│   └── team-member-2.md
└── cache/
    └── ...
```

**Discovery Phases Used:** All 13 phases  
**Cadence:** Weekly (watch mode)  
**Memory Size:** 1-5MB  
**Tools:** Git + shared .specify/memory/

---

### Level 3: Growth Team (6-20 Developers)
**Use When:** Scaling startup, multiple product areas

```
memory/
├── architecture/
│   ├── contexts/
│   │   ├── context-1.md     # Per bounded context
│   │   ├── context-2.md
│   │   └── ...
│   ├── patterns.md
│   ├── decisions/            # Per-ADR files
│   ├── violations/
│   └── compliance/           # Security, performance
├── agent-logs/
│   ├── YYYY-MM.md            # Monthly summaries
│   └── team-sync.md
├── cache/
└── metrics/
    └── discovery-stats.json
```

**Discovery Phases Used:** All 13, with focus on DDD + security  
**Cadence:** Daily (CI/CD integration)  
**Memory Size:** 10-50MB  
**Tools:** Git + shared storage + CI/CD automation  
**Agents:** Claude + Copilot (parallel discovery)

---

### Level 4: Enterprise (20+ Developers)
**Use When:** Large org, multiple teams, strict governance

```
memory/
├── architecture/
│   ├── platform/
│   │   ├── contexts/        # All bounded contexts
│   │   ├── contracts/       # Service contracts
│   │   ├── patterns.md
│   │   ├── standards.md     # Org-wide rules
│   │   └── violations/
│   ├── products/
│   │   ├── product-1/
│   │   │   ├── architecture/
│   │   │   ├── decisions/
│   │   │   └── team/
│   │   └── product-2/
│   ├── decisions/
│   │   ├── 2026-Q1/         # Quarterly grouping
│   │   ├── 2026-Q2/
│   │   └── ...
│   ├── compliance/
│   │   ├── security/
│   │   ├── performance/
│   │   └── regulations/
│   └── metrics/
│       ├── discovery-stats.json
│       ├── team-velocity.json
│       └── health-scorecard.md
├── agent-logs/
│   ├── 2026-06-03/
│   │   ├── claude-main.md
│   │   ├── copilot-feature.md
│   │   ├── gemini-security.md
│   │   └── merged.md
│   └── ...
├── governance/
│   ├── architecture-rules.yaml
│   ├── compliance-rules.yaml
│   └── audit-log.md
├── cache/
│   ├── dependency-graph.json
│   └── c4-cache/
└── webhooks/
    └── integrations.yaml     # Slack, Jira, etc.
```

**Discovery Phases Used:** All 13 + governance + compliance  
**Cadence:** Continuous (every commit)  
**Memory Size:** 100MB-1GB  
**Tools:** Git + cloud storage + governance platform  
**Agents:** Claude + Copilot + Gemini + Cursor (parallel, async)  
**Governance:** Automated compliance checks, violation tracking

---

## Initialization Workflow

### Step 1: Choose Project Type

```bash
claude /scaffold --type <type>
```

**Types:**
- `rest-api` - Single service REST API
- `fullstack-web` - React/Vue + backend
- `microservices` - Multiple services
- `realtime` - WebSocket, real-time
- `data-pipeline` - ETL, batch, streaming
- `ml-system` - Training + inference
- `saas-platform` - Multi-tenant SaaS
- `mobile-backend` - Mobile API

---

### Step 2: Choose Scale

```bash
claude /scaffold --type rest-api --scale <scale>
```

**Scales:**
- `solo` - 1 developer, minimal tooling
- `team` - 2-5 developers, shared memory
- `growth` - 6-20 developers, DDD focused
- `enterprise` - 20+ developers, governance

---

### Step 3: Choose Tech Stack

```bash
claude /scaffold \
  --type rest-api \
  --scale team \
  --backend python-fastapi \
  --database postgresql \
  --cache redis \
  --queue rabbitmq
```

**Supported:**
- **Languages:** Python, Go, Node.js, Rust, Java, C#
- **Frameworks:** FastAPI, Django, Express, Gin, Spring, .NET
- **Databases:** PostgreSQL, MongoDB, DynamoDB, Firestore
- **Cache:** Redis, Memcached, DynamoDB
- **Queues:** RabbitMQ, Kafka, SQS, GCP Pub/Sub

---

### Step 4: Auto-Generate Scaffold

```bash
claude /scaffold \
  --type rest-api \
  --scale team \
  --backend python-fastapi \
  --generate
```

**Generated:**
```
project-root/
├── .github/workflows/
├── src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
├── tests/
├── deployments/
├── docs/
├── CLAUDE.md              # Project instructions
├── .specify/
│   └── memory/            # Already initialized!
├── software-factory/
│   └── symlink to factory
├── docker-compose.yml
├── README.md
├── pyproject.toml
└── .gitignore
```

---

### Step 5: Initialize with Agents

```bash
# Single agent
claude /scaffold --init --project-path ./my-api

# Multiple agents (parallel)
claude /scaffold --init --parallel
copilot /scaffold --validate
gemini /scaffold --security-review
```

**Agents Will:**
1. Create initial files (models, services, controllers)
2. Set up database migrations
3. Configure CI/CD
4. Generate initial documentation
5. Create memory system with empty contexts

---

### Step 6: Auto-Discovery Enabled

```bash
# Documentation auto-generated
ls docs/architecture/
REPOSITORY_MAP.md          # ← Project structure
ARCHITECTURE_ANALYSIS.md   # ← Clean architecture detected
C4_CONTEXT.md              # ← System context
C4_CONTAINER.md            # ← Service boundaries
DDD_MODEL.md               # ← Bounded contexts (pre-populated)
```

**Memory Auto-Initialized:**
```
.specify/memory/architecture/
├── discovered-patterns.md
│   └─ Primary: Clean Architecture (100% - we just built it!)
├── bounded-contexts.md
│   └─ Pre-filled with your domain model
├── decisions.md
│   ├─ ADR-001: Why this architecture
│   ├─ ADR-002: Why this tech stack
│   └─ ADR-003: Why this scale level
└── violations.md
    └─ Empty (clean slate!)
```

---

## Building Your Project

After initialization, you have a complete scaffold with:

✅ **Proper folder structure** (DDD + Clean Architecture)  
✅ **Database migrations** (initial schema)  
✅ **Sample domain models** (Order, User, etc.)  
✅ **Sample services** (OrderService, UserService)  
✅ **Sample repositories** (OrderRepository, UserRepository)  
✅ **Sample controllers** (REST endpoints)  
✅ **Test templates** (unit, integration, e2e)  
✅ **Docker setup** (Dockerfile, docker-compose.yml)  
✅ **CI/CD pipeline** (GitHub Actions, GitLab CI)  
✅ **Documentation** (Architecture, API docs)  
✅ **Memory system** (Pre-initialized contexts)  

---

## Scaling Up

### From Solo to Team

```bash
# When you hire the 2nd developer:
claude /scaffold --scale-up solo→team

# This will:
# 1. Create shared memory structure
# 2. Add team collaboration docs
# 3. Set up code review process
# 4. Enable agent coordination
```

### From Team to Growth

```bash
# When you hire the 6th developer:
claude /scaffold --scale-up team→growth

# This will:
# 1. Split monolith into bounded contexts
# 2. Create per-team memory areas
# 3. Add governance & compliance
# 4. Enable parallel agent discovery
```

### From Growth to Enterprise

```bash
# When you hire the 20th developer:
claude /scaffold --scale-up growth→enterprise

# This will:
# 1. Create platform architecture
# 2. Set up governance system
# 3. Enable multi-product support
# 4. Add compliance tracking
# 5. Enable audit logging
```

---

## Project Types Deep Dive

### REST API (Most Common)

**When:** Building a single service, microservice in a larger system

```bash
claude /scaffold \
  --type rest-api \
  --scale team \
  --backend python-fastapi
```

**Structure:**
```
src/
├── domain/              # Pure business logic
│   ├── models/          # Order, User, etc.
│   ├── services/        # OrderService
│   ├── repositories/    # OrderRepository (interface)
│   └── events/          # OrderCreated event
├── application/         # Use cases
│   ├── commands/        # PlaceOrderCommand
│   ├── queries/         # GetOrderQuery
│   └── handlers/        # PlaceOrderHandler
├── infrastructure/      # Adapters
│   ├── persistence/     # SQLAlchemy, MongoDB
│   ├── messaging/       # RabbitMQ, Kafka
│   └── external/        # Stripe, AWS, etc.
└── presentation/        # Controllers
    ├── routes/          # FastAPI routes
    ├── dto/             # Request/response models
    └── middleware/      # Auth, logging, etc.
```

**Tests:**
```
tests/
├── unit/
│   └── domain/          # Pure logic, no DB
├── integration/
│   ├── infrastructure/  # DB, messaging
│   └── application/     # End-to-end handlers
└── e2e/
    └── api/             # HTTP requests
```

---

### Microservices

**When:** Multiple teams, multiple product areas, independent scaling

```bash
claude /scaffold \
  --type microservices \
  --scale enterprise \
  --services trading,portfolio,risk,auth \
  --communication event-driven
```

**Structure:**
```
services/
├── api-gateway/
│   ├── src/
│   ├── tests/
│   └── Dockerfile
├── trading-service/
│   ├── src/
│   │   ├── domain/     # Trading business logic
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── presentation/
│   └── tests/
├── portfolio-service/
│   └── ...
└── risk-service/
    └── ...

shared/
├── proto/              # Protocol buffers or OpenAPI
├── events/             # Event definitions
└── libraries/          # Shared code

infrastructure/
├── docker-compose.yml
├── k8s/
│   ├── api-gateway.yaml
│   ├── trading-service.yaml
│   └── ...
└── terraform/
    └── main.tf
```

**Memory Structure:**
```
.specify/memory/
├── architecture/
│   ├── services/
│   │   ├── trading/
│   │   ├── portfolio/
│   │   └── risk/
│   ├── contracts/       # Service contracts
│   ├── events/          # Domain events
│   └── dependencies.json
└── agent-logs/
    └── team-a.md       # Trading team discovery
```

---

### Real-Time System

**When:** Multiplayer games, live trading, collaborative tools, chat

```bash
claude /scaffold \
  --type realtime \
  --scale growth \
  --websocket native \
  --messaging redis-streams
```

**Special Considerations:**
- WebSocket handlers
- Message queue for broadcasting
- Real-time state synchronization
- Conflict resolution
- Offline-first support

---

### Data Pipeline

**When:** ETL, analytics, batch processing, ML training

```bash
claude /scaffold \
  --type data-pipeline \
  --scale growth \
  --orchestrator airflow \
  --sources postgres,s3,api \
  --sinks postgres,s3,warehouse
```

**Structure:**
```
src/
├── extractors/         # Read from sources
├── transformers/       # Business logic
├── loaders/            # Write to sinks
├── validators/         # Quality gates
└── orchestrators/      # DAG definitions

dags/
├── daily_etl.py
├── weekly_analytics.py
└── ...

tests/
├── unit/
│   └── transformers/   # Pure logic tests
└── integration/
    └── pipelines/      # End-to-end tests
```

---

### ML System

**When:** Model training, inference, MLOps

```bash
claude /scaffold \
  --type ml-system \
  --scale enterprise \
  --framework pytorch \
  --platform mlflow
```

**Structure:**
```
src/
├── data/               # Data loading & processing
├── features/           # Feature engineering
├── models/             # Model definitions
├── training/           # Training loops
├── inference/          # Prediction service
└── evaluation/         # Metrics & tests

notebooks/              # Exploration
experiments/            # Experiment tracking
models/                 # Saved model artifacts
deployments/            # Model serving
```

---

## Agent Roles During Scaffold & Build

### Claude Code (Primary Developer)
- Creates initial scaffold
- Implements models, services, controllers
- Writes tests
- Updates documentation

### Copilot (Code Review / Quality)
- Reviews generated code
- Suggests improvements
- Validates against patterns
- Checks architecture compliance

### Gemini (Analysis & Optimization)
- Analyzes emerging patterns
- Suggests optimizations
- Identifies potential issues
- Creates reports

### Cursor (Refactoring)
- Refactors as project grows
- Applies design patterns
- Optimizes performance
- Maintains architecture

---

## Command Reference

```bash
# Initialize new project
claude /scaffold --type rest-api --scale team --generate

# Scale existing project
claude /scaffold --scale-up team→growth

# Add new service (microservices only)
claude /scaffold --add-service trading-bot

# Discover current state
claude /architect-discovery --full

# Watch for violations
claude /architect-discovery --watch .

# Generate ADR
claude /scaffold --create-adr "Migrate to microservices"

# Validate against rules
claude /scaffold --validate --rules .specify/architecture-rules.yaml
```

---

## What Gets Created

### Day 1 (After Init)
- ✅ Project structure
- ✅ Sample code (models, services)
- ✅ Database migrations
- ✅ Tests
- ✅ Docker setup
- ✅ CI/CD pipeline
- ✅ Architecture documentation
- ✅ Memory system (initialized)

### Week 1
- ✅ Real business models
- ✅ Core services
- ✅ Real database schema
- ✅ Initial API endpoints
- ✅ Tests (growing)
- ✅ ADRs (3-5 decisions documented)

### Month 1
- ✅ Complete core features
- ✅ Comprehensive tests
- ✅ Performance baseline
- ✅ Security review
- ✅ Architecture validated
- ✅ Team onboarding docs

---

## Memory Persistence at Scale

The memory system grows WITH your project:

| Scale | Memory Size | Structure | Storage |
|-------|-----------|-----------|---------|
| Solo | < 100KB | Simple | Git |
| Team | 1-5MB | Shared | Git + Cloud |
| Growth | 10-50MB | Hierarchical | Git + Cloud |
| Enterprise | 100MB-1GB | Governance | Enterprise DB |

**Auto-archiving:**
```
.specify/memory/
├── current/           # Active, frequently accessed
├── archive/
│   ├── 2026-Q1/       # Quarterly snapshots
│   └── 2026-Q2/
└── cache/             # Performance optimization
```

---

## Integration Points

This scaffold system integrates seamlessly with:

✅ **ARCHITECTURE_DISCOVERY.md** - Understand existing projects  
✅ **AGENT_INTEGRATION.md** - Multiple AI agents  
✅ **MEMORY_ARCHITECTURE.md** - Cross-session state  
✅ **SDD Pipeline** - Spec-driven development  
✅ **Software Factory** - Governance & standards  

---

## Success Criteria

✅ Project starts with proper architecture  
✅ Memory system ready for team growth  
✅ Scales from solo → enterprise seamlessly  
✅ AI agents coordinate seamlessly  
✅ Documentation auto-generated & live  
✅ Compliance & governance built-in  

