# Spec-Driven Development — Complete Workflow
## Every Feature, Every Time: IDEA → PRODUCTION

> **No code ships without a spec. No spec ships without a plan. No plan ships
> without tasks. This is the Integral Market engineering contract.**

---

## The 8 Stages

```
┌─────────────────────────────────────────────────────────────────────┐
│  IDEA                                                               │
│    ↓  [1 — SPECIFICATION]  Write the spec                          │
│  SPEC                                                               │
│    ↓  [2 — ARCHITECTURE]   Design the technical approach           │
│  PLAN                                                               │
│    ↓  [3 — TASK BREAKDOWN] Decompose into atomic tasks             │
│  TASKS                                                              │
│    ↓  [4 — IMPLEMENTATION] Build incrementally                     │
│  CODE                                                               │
│    ↓  [5 — STATIC VALIDATION] Types, lint, imports                 │
│  VALIDATED                                                          │
│    ↓  [6 — TESTING] Unit → integration → E2E → load               │
│  TESTED                                                             │
│    ↓  [7 — REFACTOR] Clean up before merging                       │
│  CLEAN                                                              │
│    ↓  [8 — DOCUMENT] Update specs, memory, registry                │
│  SHIPPED                                                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Stage 1 — SPECIFICATION

**Entry criteria:** A feature request, bug report, or product idea exists.
**Exit criteria:** Spec is approved and all open questions are resolved.

**Artifact:** `software-factory/specs/active/<feature-name>.spec.md`

```bash
# Create the spec from template
cp software-factory/specs/templates/feature.spec.md \
   software-factory/specs/active/<feature-name>.spec.md
```

**Minimum spec content (block on missing items):**
```
✅ Problem statement (1–2 sentences)
✅ User stories (at least 1)
✅ Acceptance criteria (at least 3, testable)
✅ Out of scope (explicit)
✅ Success metric (at least 1)
✅ Open questions section (even if empty)
```

**Agent actions:**
```bash
# Select skills for this domain
python3 software-factory/context-engine/skill_selector.py \
  --query "<feature description>"

# Check if spec conflicts with constitution
grep -i "never\|must not\|forbidden" software-factory/constitution/CONSTITUTION.md
```

---

## Stage 2 — ARCHITECTURE PLAN

**Entry criteria:** Spec is approved.
**Exit criteria:** Technical design is reviewed and all service impacts identified.

**Artifact:** `software-factory/specs/active/<feature-name>.plan.md`

```markdown
# PLAN: <Feature Name>

## Affected Services
- [ ] Market Backend (:8000) — [what changes]
- [ ] Expert Backend (:8002) — [what changes]
- [ ] IMI Backend (:8003) — [what changes]
- [ ] Frontend (:5173) — [what changes]

## Database Changes
- Schema: [which schema]
- Tables added/modified: [list]
- Migrations required: YES / NO

## API Contract Changes
- New endpoints: [list]
- Modified endpoints: [list — breaking? non-breaking?]
- TypeScript types to update: [list]

## CodeGraph Impact Analysis
[Run: codegraph_impact("<affected symbol>")] — paste output here

## Risk: Registry Collisions
[Run: codegraph_search("<new class name>")] — paste output here

## WebSocket / Event Changes
- [ ] New WS channels needed
- [ ] New domain events needed

## Security Implications
- [ ] New endpoints require auth
- [ ] RBAC permissions needed
- [ ] Rate limiting required
```

**Agent actions:**
```python
# Always run before writing plan:
codegraph_impact("any_affected_function_or_class")
codegraph_context("domain_name")
codegraph_search("NewClassName")  # check for registry collision
```

---

## Stage 3 — TASK BREAKDOWN

**Entry criteria:** Plan is written.
**Exit criteria:** Tasks are atomic (≤ 4 hours each), ordered by dependency.

**Artifact:** `software-factory/specs/active/<feature-name>.tasks.md`

```markdown
# TASKS: <Feature Name>

## Dependency Order

### T1: Database migration [BLOCKS: T2, T3]
- File: alembic/versions/<revision>_<name>.py
- Action: Add columns/tables per plan
- Verify: alembic upgrade head && alembic check

### T2: Backend model update [BLOCKS: T3] [BLOCKED BY: T1]
- File: integral-expert-backend/app/models/<model>.py
- Action: Add new fields matching migration
- Verify: python3 -c "from app.models import *"

### T3: Backend service + endpoint [BLOCKED BY: T2]
- Files: app/services/<service>.py, app/api/v1/endpoints/<endpoint>.py
- Action: Implement business logic + route
- Verify: curl -X POST http://localhost:8002/api/v1/<endpoint>

### T4: Pydantic schemas
- File: integral-expert-backend/app/schemas/<domain>.py
- Action: Add request/response schemas

### T5: Frontend types + hook [BLOCKED BY: T3]
- Files: app/src/shared/api/types/<domain>.ts,
         app/src/modules/<module>/hooks/use<Feature>.ts
- Action: TypeScript types + React Query hook

### T6: Frontend component [BLOCKED BY: T5]
- File: app/src/modules/<module>/components/<Component>.tsx
- Action: UI implementation

### T7: Tests [BLOCKED BY: T3]
- File: tests/integration/test_<feature>.py
- Action: API integration tests

### T8: Documentation [BLOCKED BY: T7]
- Action: Update spec, memory, SKILLS_REGISTRY if needed
```

---

## Stage 4 — IMPLEMENTATION

**Entry criteria:** Tasks are listed with dependency order.
**Rules:**
- Implement one task at a time, in dependency order
- Never start T3 before T1 migrations have run
- Run `codegraph_impact()` before modifying shared utilities
- `git add` specific files — never `git add .`

```bash
# Before each task:
python3 software-factory/context-engine/skill_selector.py --query "<task description>"
# Load the top-ranked skill, then implement

# After each task:
python3 software-factory/context-engine/change_detector.py --since HEAD~1
# Verify no unintended changes, auto-document if needed
```

---

## Stage 5 — STATIC VALIDATION

**Run ALL of these before calling implementation done:**

```bash
# Backend (Python)
cd integral-expert-backend && source venv/bin/activate
python3 -c "from app.main import app; print('✅ imports OK')"
python3 -m mypy app/ --ignore-missing-imports --no-error-summary
ruff check app/

# Market backend
cd integral-market-backend && source venv/bin/activate
python3 -c "from app.main import app; print('✅ imports OK')"

# Frontend (TypeScript)
cd app
pnpm type-check          # zero TypeScript errors required
pnpm lint                # zero ESLint errors required

# Database schema matches models
cd integral-expert-backend && source venv/bin/activate
alembic check            # exits 0 if DB matches current models
```

---

## Stage 6 — TESTING

**Test pyramid — run in order:**

```bash
# Layer 1: Unit tests (pure logic, no DB)
cd integral-expert-backend && source venv/bin/activate
pytest tests/unit/ -v --tb=short

# Layer 2: Integration tests (DB + API)
pytest tests/integration/ -v --tb=short

# Layer 3: E2E tests (browser — needs all services running)
cd app
pnpm test:e2e            # or: npx playwright test

# Layer 4: Load test (if endpoint handles >100 rps)
locust -f tests/load/locustfile.py \
  --host=http://localhost:8002 \
  --users=50 --spawn-rate=5 \
  --run-time=60s --headless

# Interactive dev testing (capture UI bugs + backend logs simultaneously):
python3 software-factory/context-engine/dev_runner.py --watch
```

**Exit criteria for testing:**
```
✅ All unit tests pass
✅ All integration tests pass
✅ Happy path E2E test passes
✅ No new 5xx errors in backend log during E2E run
✅ Load test P99 < SLA target
```

---

## Stage 7 — REFACTOR

**Run change_detector to see the full diff:**
```bash
python3 software-factory/context-engine/change_detector.py \
  --since $(git merge-base HEAD main)
```

**Refactor checklist:**
```
[ ] No function > 50 lines
[ ] No duplicated logic (if same code in 3+ places → extract)
[ ] Magic numbers have named constants
[ ] All new code has type annotations
[ ] No TODO/FIXME left in staged code
[ ] Error paths have logging (logger.exception, not print)
[ ] No print() statements in backend code
[ ] No console.log() left in frontend production code
```

---

## Stage 8 — DOCUMENT

**Mandatory documentation updates:**

```bash
# 1. Move spec to archive
mv software-factory/specs/active/<feature>.spec.md \
   software-factory/specs/archive/<feature>.spec.md

# 2. Update architectural memory
cat >> software-factory/memory/decisions/$(date +%Y-%m).md << EOF

## $(date -I) — <Feature Name>
**What changed:** <brief summary>
**Key files:** <list>
**Decisions made:** <why this approach>
**Alternatives rejected:** <what was not chosen>
EOF

# 3. Update change log
python3 software-factory/context-engine/change_detector.py \
  --since HEAD~1 --document

# 4. If new skill needed, create it:
# Load skills/skill-builder/SKILL.md → follow the checklist

# 5. Commit with conventional commit message
git commit -m "feat(<scope>): <what was added and why>"
```

---

## Quick Reference — File Locations

```
Specs (active):    software-factory/specs/active/
Specs (done):      software-factory/specs/archive/
Plans:             software-factory/specs/active/*.plan.md
Tasks:             software-factory/specs/active/*.tasks.md
Templates:         software-factory/specs/templates/
Decisions:         software-factory/memory/decisions/
Patterns:          software-factory/memory/patterns/
Skills:            software-factory/skills/
Registry:          software-factory/SKILLS_REGISTRY.md
Kernel:            software-factory/kernel/ARCHITECTURE.md
Constitution:      software-factory/constitution/CONSTITUTION.md
```

---

## SDD Health Metrics

A healthy SDD process shows:
```
Spec-to-ship time:      < 2 sprints for medium features
Spec coverage:          100% of shipped features have an archived spec
Regression rate:        < 5% of features require immediate hotfix after ship
Documentation lag:      0 days (document in the same PR as code)
Memory freshness:       No decision older than 90 days without review
```
