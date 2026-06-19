# Scalable Memory Framework

**Version:** 1.0  
**Purpose:** Enable architecture memory system to scale from solo dev to enterprise (1→10,000+ engineers)

---

## Core Principle

Memory grows intelligently WITH your team:

```
Solo (1 person)
    ↓ memory ≈ 100KB
    ├── decisions.md (3-5)
    ├── patterns.md
    └── violations.md

Team (2-5)
    ↓ memory ≈ 1-5MB
    ├── architecture/
    ├── agent-logs/
    └── cache/

Growth (6-20)
    ↓ memory ≈ 10-50MB
    ├── contexts/ (per bounded context)
    ├── decisions/ (per-ADR files)
    ├── agent-logs/ (monthly summaries)
    └── metrics/

Enterprise (20+)
    ↓ memory ≈ 100MB-1GB
    ├── platform/ (company architecture)
    ├── products/ (per-product areas)
    ├── governance/ (rules, compliance)
    ├── agent-logs/ (daily, per-agent)
    └── audit/ (immutable log)
```

---

## Tier 1: Solo Developer

**Size:** 1 person  
**Memory:** < 100KB  
**Update Cadence:** Monthly  
**Storage:** Git only

### Structure
```
.specify/memory/architecture/
├── discovered-patterns.md      # What architecture you use
├── decisions.md                # 3-5 key decisions
├── violations.md               # Minor issues (optional)
└── README.md                   # Quick reference
```

### File: `discovered-patterns.md`
```yaml
---
timestamp: 2026-06-03
patterns: 1
---

# Discovered Patterns

## Primary: Monolithic REST API

- Tech Stack: Python/FastAPI, PostgreSQL, Redis
- Structure: Single database, single codebase
- Deployment: Docker container
- Scale: 1 developer, 1000 DAU

## Current Limitations
- No message queue
- Synchronous API calls
- Single-threaded processing

## Future: Event-Driven Microservices
- Timeline: When team grows to 3+
```

### File: `decisions.md`
```yaml
---
adr_count: 3
---

# Architecture Decisions

## ADR-001: Python + FastAPI
Status: Accepted
Rationale: Fast to develop, great async support
Date: 2026-01-15

## ADR-002: PostgreSQL
Status: Accepted
Rationale: Reliable, ACID transactions
Date: 2026-01-15

## ADR-003: Docker for Deployment
Status: Accepted
Rationale: Reproducible environments
Date: 2026-02-01
```

### Agents Used
- **Claude Code:** Primary developer

### Update Process
```
Monthly:
  1. Run: claude /architect-discovery --quick
  2. Review: docs/architecture/ARCHITECTURE_ANALYSIS.md
  3. Update: .specify/memory/discovered-patterns.md
  4. Commit: git push
```

---

## Tier 2: Small Team

**Size:** 2-5 people  
**Memory:** 1-5MB  
**Update Cadence:** Weekly (watch mode)  
**Storage:** Git + shared .specify/

### Structure
```
.specify/memory/
├── architecture/
│   ├── discovered-patterns.md
│   ├── bounded-contexts.md     # NEW: Multiple domains
│   ├── data-flows.md           # NEW: Sequences
│   ├── decisions.md            # 10-20 ADRs
│   ├── violations.md
│   ├── c4-definitions.json     # Cache
│   └── dependency-graph.json   # Cache
├── agent-logs/
│   ├── claude-2026-06.md       # Who discovered what
│   ├── copilot-2026-06.md
│   └── summary.md              # Merged results
└── README.md
```

### File: `bounded-contexts.md`
```yaml
---
contexts_count: 2
last_update: 2026-06-03
---

# Bounded Contexts

## Context 1: User Management
- Domain: Authentication, profiles, roles
- Aggregates: User, Role, Permission
- Repositories: UserRepository, RoleRepository
- Services: AuthService, UserService

## Context 2: Product Catalog
- Domain: Products, inventory, categories
- Aggregates: Product, Category, Inventory
- Repositories: ProductRepository, InventoryRepository
- Services: CatalogService, InventoryService

## Communication
- User Context → Product Context: Events via queue
```

### Agents Used
- **Claude Code:** Primary implementation
- **Copilot:** Code review, quality checks

### Update Process
```
Watch Mode (Continuous):
  claude /architect-discovery --watch . --interval 60

Results:
  - Detects changes every minute
  - Updates affected diagrams
  - Flags new violations
  - Updates .specify/memory/ automatically
```

---

## Tier 3: Growth Stage

**Size:** 6-20 people  
**Memory:** 10-50MB  
**Update Cadence:** Daily (CI/CD)  
**Storage:** Git + cloud storage + cache

### Structure
```
.specify/memory/
├── architecture/
│   ├── contexts/
│   │   ├── trading/            # Per bounded context
│   │   │   ├── model.md
│   │   │   ├── aggregates.md
│   │   │   ├── external-deps.md
│   │   │   └── decisions.md
│   │   ├── portfolio/
│   │   ├── risk/
│   │   └── ...
│   ├── contracts/               # Service contracts
│   │   ├── order-api.yaml
│   │   └── position-feed.yaml
│   ├── patterns.md              # Org-wide patterns
│   ├── standards.md             # Coding standards
│   ├── decisions/               # One file per ADR
│   │   ├── ADR-001-*.md
│   │   ├── ADR-002-*.md
│   │   └── ...
│   ├── violations/
│   │   ├── critical/
│   │   ├── warnings/
│   │   └── low/
│   ├── compliance/              # NEW: Security, perf
│   │   ├── security-review.md
│   │   └── performance.md
│   └── cache/                   # Performance
│       ├── dependency-graph.json
│       ├── c4-cache/
│       └── file-hashes.json
├── agent-logs/
│   ├── 2026-06/
│   │   ├── 2026-06-01.md       # Daily summaries
│   │   ├── 2026-06-02.md
│   │   └── ...
│   └── summaries/
│       ├── team-trading.md     # Per-team
│       ├── team-portfolio.md
│       └── ...
├── team/
│   ├── ownership.md             # Who owns what
│   ├── contact.md               # How to reach teams
│   └── onboarding/
│       └── new-member.md
├── governance/                  # NEW: Rules
│   └── architecture-rules.yaml
└── metrics/                     # NEW: Health
    ├── discovery-stats.json
    └── health-scorecard.md
```

### File: `team/ownership.md`
```yaml
# Team Ownership

## Trading Team
- Services: trading-service, order-service
- Databases: trading_db
- Owner: alice@company.com

## Portfolio Team
- Services: portfolio-service, analytics
- Owner: bob@company.com

## Risk Team
- Services: risk-service
- Owner: charlie@company.com
```

### File: `governance/architecture-rules.yaml`
```yaml
rules:
  - name: "No cyclic dependencies"
    severity: CRITICAL
    action: BLOCK_MERGE

  - name: "Domain layer must not import infrastructure"
    severity: CRITICAL
    action: BLOCK_MERGE

  - name: "Services must communicate async"
    severity: HIGH
    action: WARN_REVIEW

  - name: "80% test coverage minimum"
    severity: MEDIUM
    action: WARN_REVIEW

  - name: "ADR required for architecture changes"
    severity: HIGH
    action: BLOCK_MERGE
```

### Agents Used
- **Claude Code:** Implement features, create services
- **Copilot:** Code review, enforce rules
- **Gemini:** Analyze patterns, optimize
- **Cursor:** Refactor, maintain architecture

### Update Process
```
CI/CD Automation:
  - On every push:
    1. Run: claude /architect-discovery --quick
    2. Check: governance/architecture-rules.yaml
    3. Update: .specify/memory/
    4. Report: Violations in PR comment
    5. Block: If CRITICAL violations
    6. Merge: If all checks pass
```

---

## Tier 4: Enterprise

**Size:** 20+ people (multiple teams, multiple products)  
**Memory:** 100MB-1GB  
**Update Cadence:** Continuous (every commit)  
**Storage:** Enterprise database + Git + CDN

### Structure
```
.specify/memory/
├── platform/                    # Company-wide
│   ├── architecture/
│   │   ├── contexts/            # ALL company contexts
│   │   │   ├── trading/
│   │   │   ├── portfolio/
│   │   │   ├── risk/
│   │   │   ├── auth/
│   │   │   ├── reporting/
│   │   │   └── ...
│   │   ├── contracts/           # Service contracts
│   │   ├── standards.md         # Org coding standards
│   │   ├── patterns.md          # Approved patterns
│   │   ├── rules/               # Architecture rules
│   │   │   ├── layer-rules.yaml
│   │   │   ├── naming-rules.yaml
│   │   │   └── security-rules.yaml
│   │   └── violations/
│   │       ├── critical/
│   │       ├── warnings/
│   │       └── audit-log.md
│   ├── decisions/               # Company decisions
│   │   ├── 2026-Q1/
│   │   ├── 2026-Q2/
│   │   └── active.md            # Current decisions
│   ├── compliance/
│   │   ├── security/
│   │   │   ├── auth-standard.md
│   │   │   ├── encryption.md
│   │   │   └── audit-log.md
│   │   ├── performance/
│   │   │   ├── benchmarks.md
│   │   │   └── slo.md
│   │   └── regulations/
│   │       ├── gdpr.md
│   │       ├── soc2.md
│   │       └── compliance-log.md
│   └── metrics/
│       ├── health-scorecard.md
│       ├── team-velocity.json
│       ├── discovery-stats.json
│       └── violations-trend.json
│
├── products/                    # Per-product teams
│   ├── product-trading/
│   │   ├── architecture/
│   │   │   ├── contexts/
│   │   │   ├── decisions/
│   │   │   └── violations/
│   │   ├── team/
│   │   │   ├── members.yaml
│   │   │   ├── standups.md
│   │   │   └── roadmap.md
│   │   └── metrics/
│   ├── product-analytics/
│   │   └── ...
│   └── product-mobile/
│       └── ...
│
├── agent-logs/
│   ├── 2026-06-03/
│   │   ├── claude-main-stream.md
│   │   ├── copilot-feature-review.md
│   │   ├── gemini-security-scan.md
│   │   ├── cursor-refactor.md
│   │   └── merged.md            # Consolidated
│   ├── summaries/
│   │   ├── daily/
│   │   ├── weekly/
│   │   └── monthly/
│   └── trends/
│       └── violations-trend.md
│
├── governance/
│   ├── rules/
│   │   ├── architecture-rules.yaml
│   │   ├── security-rules.yaml
│   │   ├── performance-rules.yaml
│   │   └── compliance-rules.yaml
│   ├── policies/
│   │   ├── review-policy.md
│   │   ├── escalation-policy.md
│   │   └── change-policy.md
│   └── audit/
│       ├── 2026-Q1-audit.md
│       └── 2026-Q2-audit.md
│
├── cache/
│   ├── dependency-graph.json
│   ├── c4-cache/
│   │   ├── context.svg
│   │   ├── container.svg
│   │   └── component.svg
│   └── file-hashes.json         # For fast diffs
│
├── webhooks/
│   ├── slack-integration.yaml   # Notify team
│   ├── jira-integration.yaml    # Create tickets
│   ├── datadog-integration.yaml # Send metrics
│   └── pagerduty-integration.yaml # Alert on critical
│
└── README.md                    # Navigation guide
```

### File: `platform/architecture/rules/architecture-rules.yaml`
```yaml
---
version: 1.0
organization: "Integral Market"
enforced_at: "2026-06-03"
---

rules:
  critical_rules:
    - name: "No cyclic dependencies"
      severity: CRITICAL
      action: BLOCK_MERGE
      exempt: []

    - name: "Domain layer must not import infrastructure"
      severity: CRITICAL
      action: BLOCK_MERGE
      exempt: []

    - name: "Service contracts must be documented"
      severity: CRITICAL
      action: BLOCK_MERGE
      file_pattern: "src/presentation/controllers/*.py"

  high_rules:
    - name: "Async communication for cross-service calls"
      severity: HIGH
      action: REQUIRE_REVIEW
      exception: "Small utility services"

    - name: "ADR required for architecture changes"
      severity: HIGH
      action: BLOCK_MERGE
      exempt: ["docs/", "tests/"]

    - name: "Security: All APIs must use mTLS"
      severity: HIGH
      action: BLOCK_DEPLOY
      deadline: "2026-07-01"

  medium_rules:
    - name: "80% unit test coverage"
      severity: MEDIUM
      action: REQUIRE_REVIEW
      threshold: 0.80

    - name: "Database migrations must be backwards compatible"
      severity: MEDIUM
      action: REQUIRE_REVIEW

    - name: "Performance: P99 latency < 500ms"
      severity: MEDIUM
      action: WARN_REVIEW
      metric: "p99_latency"
```

### File: `platform/metrics/health-scorecard.md`
```yaml
---
date: 2026-06-03
last_updated: "2026-06-03T14:30:00Z"
---

# Architecture Health Scorecard

| Metric | Target | Current | Status | Trend |
|--------|--------|---------|--------|-------|
| Cyclic Dependencies | 0 | 0 | ✓ Good | ↓ |
| Critical Violations | 0 | 2 | ✗ Alert | ↑ |
| Test Coverage | 80% | 76% | ⚠️ Warning | → |
| Documentation Complete | 100% | 92% | ⚠️ Warning | ↓ |
| Services Documented | 100% | 100% | ✓ Good | → |
| ADRs Current | 100% | 95% | ⚠️ Warning | ↓ |

## Critical Issues Requiring Action
1. Cyclic dependency in trading-service (estimated 8 hours to fix)
2. mTLS migration deadline: 2026-07-01 (3 weeks remaining)

## Weekly Trend
- Down: Violations reduced by 3 this week ✓
- Up: Test coverage steady at 76%
- New: 2 new ADRs created

## Team Health
- Velocity: 35 story points (avg 40)
- Onboarding time: 2 days (target: 1 day)
- Architecture review time: 2 hours per PR (acceptable)
```

### Agents Used
- **Claude Code (Stream 1):** Main development
- **Claude Code (Stream 2):** Feature development
- **Copilot (Team A):** Code review (trading team)
- **Copilot (Team B):** Code review (portfolio team)
- **Gemini:** Continuous analysis & optimization
- **Cursor:** Large refactors & migrations

### Update Process
```
Continuous (Every Commit):
  1. Trigger: Push to repo
  2. CI Pipeline:
     a. All 7 phases run (< 5 min)
     b. Check governance rules
     c. Compare to previous state
     d. Generate violations report
  3. Store:
     a. Results in .specify/memory/
     b. Metrics in metrics/
     c. Audit log in audit/
  4. Notify:
     a. Slack: New violations
     b. Jira: Create tickets
     c. DataDog: Send metrics
     d. PagerDuty: Alert on critical

Daily Summary:
  - Aggregate daily changes
  - Send team report
  - Update trend metrics

Weekly Sync:
  - Review health scorecard
  - Discuss ADRs
  - Plan architecture work

Monthly Audit:
  - Full discovery re-run
  - Compliance review
  - Metrics analysis
```

---

## Memory Migration Path

### From Tier 1 → Tier 2 (Hiring 1st team member)

```bash
claude /memory --migrate solo→team

This will:
  1. Reorganize .specify/memory/ structure
  2. Create agent-logs/ for multi-person tracking
  3. Add bounded-contexts.md
  4. Initialize shared memory in Git
  5. Setup watch mode
```

### From Tier 2 → Tier 3 (Hiring 6th person)

```bash
claude /memory --migrate team→growth

This will:
  1. Create contexts/ folder (per bounded context)
  2. Split decisions/ into per-ADR files
  3. Add governance/ folder
  4. Add metrics/ folder
  5. Enable CI/CD integration
  6. Setup automated daily summaries
```

### From Tier 3 → Tier 4 (Hiring 20th person)

```bash
claude /memory --migrate growth→enterprise

This will:
  1. Create platform/ (company-wide)
  2. Create products/ (per-team)
  3. Add compliance/ & audit/
  4. Setup webhook integrations
  5. Configure enterprise DB
  6. Enable multi-stream agent coordination
  7. Setup governance enforcement
  8. Enable audit logging
```

---

## Smart Archiving

Memory grows but stays performant:

```
Current Working Memory:
  .specify/memory/architecture/
  └─ < 10MB (active decisions, violations)

Recent Archive (This Quarter):
  .specify/memory/archive/2026-Q2/
  └─ Full snapshots, searchable

Historical Archive (Cloud):
  s3://company/architecture-memory/
  └─ Long-term retention, compliance
```

---

## Cross-Agent Coordination

With multiple agents running simultaneously:

```
Agent 1 (Claude - Main):      Agent 2 (Copilot - Review):
  discover architecture  ──→   validate & enhance
  
Agent 3 (Gemini - Analysis):  Agent 4 (Cursor - Refactor):
  optimize patterns      ──→   apply improvements
  
All → Merge to .specify/memory/ → Commit to Git
```

**Conflict Resolution:**
```
If agents disagree:
  1. Accept most comprehensive discovery
  2. Note alternative perspectives
  3. Create ADR to resolve
  4. Document in decisions/
```

---

## Performance at Scale

| Tier | Files | Size | Query Time | Update Time |
|------|-------|------|-----------|------------|
| Solo | 3 | 100KB | < 1ms | < 10s |
| Team | 15 | 5MB | < 10ms | < 30s |
| Growth | 100+ | 50MB | < 100ms | < 2min |
| Enterprise | 1000+ | 1GB | < 500ms | < 5min |

**Optimization:**
- Cache layer (JSON files for fast reads)
- Incremental updates (only changed files)
- Compression (gzip for storage)
- CDN (for remote teams)

---

## Compliance & Audit

Enterprise tier includes immutable audit log:

```
audit/2026-Q2-audit.md

Every discovery run records:
  - Who ran it (agent name)
  - When it ran (timestamp)
  - What changed (diffs)
  - Any violations found
  - Violations resolved

Result: Full audit trail for compliance
```

---

## Success Criteria by Tier

### Tier 1 (Solo)
✓ Architecture clear to yourself  
✓ Decisions documented  

### Tier 2 (Team)
✓ New team members onboard in 1 day  
✓ Shared understanding of architecture  
✓ Watch mode catches violations early  

### Tier 3 (Growth)
✓ Per-team ownership clear  
✓ Cross-team contracts documented  
✓ Automated governance enforced  
✓ Metrics guide decision-making  

### Tier 4 (Enterprise)
✓ Company-wide standards enforced  
✓ Compliance automatic  
✓ Audit trail complete  
✓ Multi-team coordination seamless  
✓ 10,000+ engineers can navigate architecture  

