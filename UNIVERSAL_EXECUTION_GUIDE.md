# Universal Execution Guide

**Version:** 1.0  
**Purpose:** Get started with architecture discovery + scaffolding, no matter your starting point

---

## Choose Your Starting Point

### Path A: NEW PROJECT (Starting From Zero)
→ Use **UNIVERSAL_PROJECT_SCAFFOLD.md**

### Path B: EXISTING PROJECT (Add Architecture Docs)
→ Use **ARCHITECTURE_DISCOVERY.md**

### Path C: SCALING UP (Migrate Memory Tiers)
→ Use **SCALABLE_MEMORY_FRAMEWORK.md**

### Path D: MULTIPLE AGENTS (Coordinate Teams)
→ Use **AGENT_INTEGRATION.md**

---

## Path A: New Project from Zero

**Timeline:** 2-4 hours to production-ready scaffold  
**Team:** 1+ developers + any AI agent

### Step 1: Choose Project Type (5 min)

```bash
# What are you building?
# Answer one:
rest-api              # Single service REST API
fullstack-web         # React + Python/Node backend
microservices         # Multiple services
realtime              # WebSocket-based (trading, gaming, chat)
data-pipeline         # ETL, batch processing
ml-system             # Model training + inference
saas-platform         # Multi-tenant SaaS
mobile-backend        # Mobile API
```

**Examples:**
- Trading platform → `microservices`
- Blog or e-shop → `fullstack-web`
- ML pipeline → `data-pipeline`
- Chat app → `realtime`

### Step 2: Choose Scale (5 min)

```bash
# Current team size?
solo              # 1 developer
team              # 2-5 developers
growth            # 6-20 developers
enterprise        # 20+ developers
```

**Rule of thumb:**
- You: `solo`
- Small startup: `team`
- Growing startup (Series A): `growth`
- Established company: `enterprise`

### Step 3: Choose Tech Stack (10 min)

```bash
# Languages & Frameworks
Backend:
  - Python/FastAPI (recommended for speed)
  - Python/Django (for traditional web)
  - Node.js/Express (JavaScript full-stack)
  - Go/Gin (high performance)
  - Rust/Actix (ultra-high performance)

Frontend (if fullstack):
  - React (recommended)
  - Vue
  - Next.js (React + SSR)
  - Svelte

Database:
  - PostgreSQL (most common, recommended)
  - MongoDB (document storage)
  - DynamoDB (serverless)

Cache:
  - Redis (recommended)
  - Memcached
  - None (skip if not needed)

Message Queue (if microservices/realtime):
  - RabbitMQ (recommended)
  - Kafka (high-volume events)
  - Redis Streams (simple)
```

### Step 4: Generate Scaffold (15 min)

```bash
# All-in-one command
claude /scaffold \
  --type rest-api \
  --scale team \
  --backend python-fastapi \
  --database postgresql \
  --cache redis \
  --generate \
  --init

# Or step-by-step
claude /scaffold --type rest-api --scale team
# Review generated structure
claude /scaffold --init
```

### Step 5: Verify & Deploy (30 min)

```bash
# Test it works
cd project-name
docker-compose up -d          # Start services
pytest tests/                 # Run tests
curl http://localhost:8000    # Test API

# Verify architecture docs
ls docs/architecture/
head REPOSITORY_MAP.md
head ARCHITECTURE_ANALYSIS.md

# Check memory system
ls .specify/memory/architecture/
head discovered-patterns.md
```

### Output After Step 5

```
✓ Project structure created
✓ Sample code generated
✓ Database migrations ready
✓ Tests included
✓ Docker configured
✓ CI/CD pipeline created
✓ Architecture documented
✓ Memory system initialized
✓ Ready to build features
```

### Next: Build Your Features

```bash
# As you build:
1. Create ADRs for architecture decisions
   claude /scaffold --create-adr "Add Redis caching"

2. Keep architecture docs in sync
   claude /architect-discovery --watch .

3. Add tests as you go
   pytest tests/

4. Review violations periodically
   cat docs/architecture/VIOLATIONS.md
```

---

## Path B: Existing Project Add Docs

**Timeline:** 1-3 hours  
**Team:** Any size + any AI agent

### Step 1: Navigate to Project

```bash
cd /path/to/existing-project
git status                    # Make sure it's clean
```

### Step 2: Run Quick Discovery (10 min)

```bash
claude /architect-discovery --quick

# Generates:
# - REPOSITORY_MAP.md
# - ARCHITECTURE_ANALYSIS.md
```

### Step 3: Review Results (20 min)

```bash
open docs/architecture/REPOSITORY_MAP.md
open docs/architecture/ARCHITECTURE_ANALYSIS.md

# Ask: Is the detected architecture correct?
# - If Yes → continue to Step 4
# - If No → run Step 3B
```

### Step 3B: Run Full Discovery (1-2 hours)

```bash
claude /architect-discovery --full

# Generates all 13 phases:
# REPOSITORY_MAP.md
# ARCHITECTURE_ANALYSIS.md
# DDD_MODEL.md
# C4_CONTEXT.md
# C4_CONTAINER.md
# C4_COMPONENT.md
# C4_CODE.md
# DEPENDENCY_ANALYSIS.md
# DATA_FLOW.md
# DEPLOYMENT.md
# TEST_COVERAGE.md
# SECURITY.md
# PERFORMANCE.md
```

### Step 4: Review Critical Findings (20 min)

```bash
# Must review:
1. VIOLATIONS.md → Any critical issues?
2. DEPENDENCY_ANALYSIS.md → Cyclic dependencies?
3. TEST_COVERAGE.md → Major gaps?
4. SECURITY.md → Auth/encryption issues?

# Create tickets for violations
claude /scaffold --create-adr "Fix cyclic dependency in X"
```

### Step 5: Share & Integrate (20 min)

```bash
# Commit to git
git add docs/architecture/
git commit -m "docs: initial architecture discovery"
git push

# Share with team
# Send: docs/architecture/REPOSITORY_MAP.md
# Send: docs/architecture/C4_CONTAINER.md
# Send: docs/architecture/VIOLATIONS.md

# Setup continuous updates
claude /architect-discovery --watch . --interval 60

# Or integrate into CI/CD
# Add .github/workflows/architecture.yml (see AGENT_INTEGRATION.md)
```

### Output After Step 5

```
✓ Complete architecture mapped
✓ Current state documented
✓ Violations identified
✓ Team informed
✓ Continuous updates enabled
✓ Living documentation started
```

---

## Path C: Scaling Up (Grow Memory System)

**Timeline:** 30 minutes per migration  
**Trigger:** When team size changes (hire 2nd, 6th, 20th person)

### When: You Hire 2nd Team Member

```bash
# Current state: Tier 1 (Solo)
# Target state: Tier 2 (Team)

claude /memory --migrate solo→team

# What happens:
# 1. .specify/memory/ reorganized
# 2. agent-logs/ created (shared space)
# 3. bounded-contexts.md added
# 4. Watch mode enabled
# 5. Shared Git setup

# Result: Both can see each other's discoveries
```

### When: You Hire 6th Team Member

```bash
# Current state: Tier 2 (Team)
# Target state: Tier 3 (Growth)

claude /memory --migrate team→growth

# What happens:
# 1. contexts/ created (per bounded context)
# 2. decisions/ split into per-ADR files
# 3. governance/ folder created
# 4. metrics/ folder created
# 5. CI/CD integration enabled
# 6. Daily automation starts

# Result: Scalable memory structure
```

### When: You Hire 20th Team Member

```bash
# Current state: Tier 3 (Growth)
# Target state: Tier 4 (Enterprise)

claude /memory --migrate growth→enterprise

# What happens:
# 1. platform/ for company-wide
# 2. products/ for per-team areas
# 3. governance/ with rules enforcement
# 4. compliance/ with audit logs
# 5. Webhook integrations setup
# 6. Enterprise DB configured
# 7. Multi-agent coordination enabled

# Result: Enterprise-grade governance
```

### No Data Loss

All migration steps preserve your existing memory:

```
Before migration:
  .specify/memory/
  └── architecture/
      ├── decisions.md
      ├── patterns.md
      └── violations.md

After migration to Tier 2:
  .specify/memory/
  ├── architecture/
  │   ├── decisions.md ← Original
  │   ├── patterns.md ← Original
  │   └── violations.md ← Original
  ├── agent-logs/ ← New
  └── cache/ ← New
```

---

## Path D: Multi-Agent Coordination

**Timeline:** 20 minutes setup + ongoing  
**Team:** Any size with multiple agents

### Setup One-Time (20 min)

**Step 1: Choose Agents**

```bash
# Pick which agents you'll use
# Each has different strengths

Primary Developer: Claude Code
  └─ Implements features, creates services

Code Reviewer: Copilot
  └─ Reviews code, enforces standards

Analyzer: Gemini
  └─ Analyzes patterns, optimizes

Refactor Expert: Cursor
  └─ Applies design patterns, maintains architecture
```

**Step 2: Configure Agent Roles**

```yaml
# .specify/agents.yaml
agents:
  claude-code:
    role: "Primary Developer"
    tasks:
      - implement-features
      - create-services
      - write-tests
    memory_access: "read-write"

  copilot:
    role: "Code Reviewer"
    tasks:
      - review-code
      - enforce-rules
      - validate-patterns
    memory_access: "read"

  gemini:
    role: "Analyzer"
    tasks:
      - analyze-patterns
      - suggest-optimizations
      - identify-issues
    memory_access: "read-write"

  cursor:
    role: "Refactor Expert"
    tasks:
      - refactor-code
      - apply-patterns
      - migrate-architecture
    memory_access: "read-write"
```

**Step 3: Setup Coordination**

```bash
# Enable multi-agent memory sharing
claude /agents --enable-coordination

# Setup conflict resolution
claude /agents --set-conflict-resolution merge-comprehensive

# Enable agent logging
claude /agents --enable-logging --output .specify/memory/agent-logs/
```

### Running Multi-Agent Tasks (Ongoing)

**Scenario 1: Implement New Feature**

```
Timeline:
  T+0min: Claude Code starts implementation
    └─ Creates models, services, controllers
    └─ Writes tests
    └─ Updates memory

  T+30min: Copilot reviews code
    └─ Validates against rules
    └─ Suggests improvements
    └─ Adds comments to memory

  T+60min: Gemini analyzes patterns
    └─ Checks for optimization opportunities
    └─ Flags potential issues
    └─ Suggests refactoring

  T+90min: Cursor applies improvements
    └─ Refactors per Gemini's suggestions
    └─ Applies design patterns
    └─ Optimizes performance

Result: Well-crafted, optimized feature
```

**Scenario 2: Architecture Change**

```
Timeline:
  T+0: Plan phase
    1. Claude Code reads existing architecture
    2. Creates ADR for proposed change
    3. Shares with team in memory

  T+1h: Design phase
    1. Copilot reviews ADR, suggests improvements
    2. Gemini analyzes impact on other services
    3. Cursor outlines refactoring steps

  T+2h: Implementation phase
    1. Claude Code implements main change
    2. Copilot reviews each PR
    3. Cursor handles large refactors
    4. Gemini validates patterns

  T+4h: Verification phase
    1. Discovery run confirms new architecture
    2. Tests verify behavior
    3. Team confirms satisfaction

Result: Smooth, well-coordinated architecture evolution
```

### Memory Merge Strategy

When agents disagree:

```
Agent 1 says: "Use Event Sourcing"
Agent 2 says: "Use Simple Event Log"
Agent 3 says: "Use Saga Pattern"

Resolution:
  1. Claude Code creates ADR with all options
  2. Team discusses trade-offs
  3. Decision recorded in decisions/
  4. All agents implement agreed approach
  5. No conflicting memory entries
```

---

## Quick Reference: Which Path Am I?

```
"I'm building a new project from scratch"
  → Path A: UNIVERSAL_PROJECT_SCAFFOLD.md

"I have an existing project with no docs"
  → Path B: ARCHITECTURE_DISCOVERY.md

"My team is growing and I need to scale"
  → Path C: SCALABLE_MEMORY_FRAMEWORK.md

"I want multiple AI agents working together"
  → Path D: AGENT_INTEGRATION.md + This Guide

"I'm combining multiple paths"
  → Yes! All paths work together
  → See 'Combining Paths' below
```

---

## Combining Paths

### Scenario: Startup Founder (Day 1)

```
Week 1:
  1. Path A: Generate scaffold for REST API (team scale)
  2. Start building features
  3. Push to GitHub

Week 2-3:
  1. Setup architecture watching
     claude /architect-discovery --watch .
  2. Auto-generate docs as you code
  3. Memory system tracking your decisions

Week 4 (Hire 1st engineer):
  1. Path C: Migrate memory to shared (solo → team)
  2. Share docs/architecture/ with new hire
  3. New hire runs quick discovery to understand codebase
  4. Parallel development with shared memory

Month 3 (Hire 6th person):
  1. Path C: Migrate to growth scale
  2. Split into bounded contexts
  3. Enforce governance rules
  4. Start using multiple agents
  5. Path D: Enable Copilot for code review

Month 12 (Hire 20th person):
  1. Path C: Migrate to enterprise
  2. Multiple product teams
  3. Cross-team coordination
  4. Full governance & compliance

Result: Scaled from 1 → 20+ people without losing architectural coherence
```

### Scenario: Enterprise CTO (Day 1)

```
Today:
  1. Path B: Discover existing architecture
  2. Review VIOLATIONS.md, fix critical issues
  3. Document current state in Git

Week 1:
  1. Path A: Build new service scaffold
  2. Compare to existing architecture
  3. Create ADRs for integration points
  4. Setup shared memory

Week 2:
  1. Path C: Setup Tier 4 (Enterprise) memory
  2. Create governance rules
  3. Setup compliance tracking

Week 3:
  1. Path D: Enable multi-agent coordination
  2. Claude for development
  3. Copilot for reviews across teams
  4. Gemini for optimization
  5. Cursor for migrations

Result: Enterprise architecture system integrated, automated, compliant
```

---

## Success Markers

### Path A (New Project)
- ✅ Day 1: Scaffold generated, running
- ✅ Day 1: Docs exist (REPOSITORY_MAP.md, ARCHITECTURE_ANALYSIS.md)
- ✅ Week 1: Features building on solid foundation
- ✅ Month 1: Team understands architecture without explanation

### Path B (Existing Project)
- ✅ Hour 1: Quick discovery complete
- ✅ Hour 2: VIOLATIONS.md reviewed with team
- ✅ Hour 3: Docs committed to Git
- ✅ Week 1: Architecture decisions documented in ADRs

### Path C (Scaling)
- ✅ Memory migrated successfully
- ✅ New team members onboard faster
- ✅ Violations caught automatically
- ✅ Decisions recorded at each scale

### Path D (Multi-Agent)
- ✅ Agents coordinate without conflicts
- ✅ Memory shared effectively
- ✅ Features implemented faster
- ✅ Architecture maintained despite scaling

---

## If You Get Stuck

### "I don't know which path to start"
```
Answer these:
1. Do I have existing code? (YES → Path B, NO → Path A)
2. Am I alone or with a team? (ALONE → solo scale, TEAM → team scale)
3. Do I have multiple AI agents? (NO → skip Path D for now, YES → add Path D)

If still unsure: Start with Path B (existing project discovery)
It works on ANY codebase and gives immediate clarity
```

### "Discovery output doesn't match my architecture"
```
Reasons & Fixes:
1. Code structure doesn't match your mental model
   → Fix: Refactor code to match designed architecture

2. Architecture is unconventional
   → Fix: Create .specify/architecture-rules.yaml explaining it

3. Tools misdetecting patterns
   → Fix: Use --focus flag (--focus ddd, --focus security)

4. Codebase is too young/evolving
   → Fix: Run discovery again in 1-2 weeks
```

### "Memory system getting too large"
```
Solutions:
1. Archive quarterly (2026-Q1/, 2026-Q2/)
2. Use cloud storage for old snapshots
3. Keep .specify/memory/ under version control
4. Use cache layer for performance

Storage targets:
  - Solo: < 100KB
  - Team: < 10MB
  - Growth: < 100MB
  - Enterprise: < 1GB
```

### "Multiple agents creating conflicting outputs"
```
Prevention:
1. Assign clear roles (Developer, Reviewer, Analyzer, etc.)
2. Enable conflict detection
3. Use merge resolution strategy (merge-comprehensive)
4. Create coordination ADRs

If conflicts happen:
1. Both discoveries recorded in agent-logs/
2. Merge to most comprehensive version
3. Create ADR explaining decision
4. Document in decisions/
```

---

## Commands Cheat Sheet

```bash
# NEW PROJECT
claude /scaffold --type rest-api --scale team --generate --init

# EXISTING PROJECT
claude /architect-discovery --quick               # Fast (15 min)
claude /architect-discovery --full                # Comprehensive (1-2 hours)
claude /architect-discovery --watch . --interval 60  # Continuous

# SCALING
claude /memory --migrate solo→team
claude /memory --migrate team→growth
claude /memory --migrate growth→enterprise

# MULTI-AGENT
claude /agents --enable-coordination
claude /agents --set-conflict-resolution merge-comprehensive

# GOVERNANCE
claude /scaffold --validate --rules .specify/architecture-rules.yaml
claude /scaffold --create-adr "Title of decision"

# REVIEW
cat docs/architecture/VIOLATIONS.md
cat .specify/memory/architecture/decisions.md
```

---

## Next: Choose Your Path

**Ready to start?** Pick one:

1. **Building new?** → [UNIVERSAL_PROJECT_SCAFFOLD.md](UNIVERSAL_PROJECT_SCAFFOLD.md)
2. **Have code, no docs?** → [ARCHITECTURE_DISCOVERY.md](ARCHITECTURE_DISCOVERY.md)
3. **Team growing?** → [SCALABLE_MEMORY_FRAMEWORK.md](SCALABLE_MEMORY_FRAMEWORK.md)
4. **Multiple agents?** → [AGENT_INTEGRATION.md](AGENT_INTEGRATION.md)

**15 minutes from now, you'll have an architectural map of your project.** ✨

