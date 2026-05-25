# SKILL: Software Product Architect
## Domain: Product Vision, Feature Scoping, Roadmap, User Stories, PRD

**Activation triggers:** new feature request, product requirements, user story,
acceptance criteria, feature scope, PRD, product roadmap, MVP definition,
feature prioritization, stakeholder alignment.

---

## Product Decision Framework

```
Before building anything, answer:
  1. WHO is this for? (user persona, job-to-be-done)
  2. WHAT problem does it solve? (pain point, current workaround)
  3. HOW will we know it works? (success metric)
  4. WHY now? (market timing, dependency, user demand signal)
  5. WHAT is the MVP? (minimum that delivers the core value)
  6. WHAT is explicitly OUT OF SCOPE? (prevents scope creep)
```

---

## Product Requirements Document Template

```markdown
# PRD: [Feature Name]
**Status:** Draft | Review | Approved
**Author:** [name]
**Date:** [YYYY-MM-DD]
**Stakeholders:** [list]

## Problem Statement
[1–2 sentences: who has what problem, and why does it matter now]

## User Stories
- As a [persona], I want to [action] so that [benefit].
- As a [persona], I want to [action] so that [benefit].

## Success Metrics
| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [metric] | [baseline] | [goal] | [when] |

## Acceptance Criteria
- [ ] [User can do X]
- [ ] [System responds within Y ms]
- [ ] [Edge case Z is handled]

## Out of Scope (for this version)
- [explicit non-goal 1]
- [explicit non-goal 2]

## Technical Constraints
- [constraint 1: e.g., must work within existing auth system]
- [constraint 2: e.g., cannot introduce new DB tables in this sprint]

## Open Questions
- [ ] [unresolved question 1]
- [ ] [unresolved question 2]

## Dependencies
- [upstream dependency: feature/service/team this depends on]

## Risk Register
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [risk] | H/M/L | H/M/L | [plan] |
```

---

## Feature Prioritization (RICE Score)

```python
# RICE = (Reach × Impact × Confidence) / Effort

def rice_score(reach: int, impact: float, confidence: float, effort: float) -> float:
    """
    reach:      estimated users affected per quarter
    impact:     0.25 (minimal) | 0.5 (low) | 1.0 (medium) | 2.0 (high) | 3.0 (massive)
    confidence: 0.0–1.0 (how sure are we about reach/impact estimates)
    effort:     person-weeks to deliver
    """
    return (reach * impact * confidence) / effort

# Example:
features = [
    {"name": "Copy Trading Signals Feed",       "rice": rice_score(500, 2.0, 0.8, 3)},
    {"name": "Journal AI Coach",                "rice": rice_score(300, 1.0, 0.7, 2)},
    {"name": "Multi-broker Dashboard",          "rice": rice_score(200, 3.0, 0.6, 8)},
    {"name": "Telegram Notifications",          "rice": rice_score(800, 0.5, 0.9, 1)},
]
features.sort(key=lambda f: f["rice"], reverse=True)
# Build in RICE order
```

---

## User Persona Definitions

```
PERSONA 1: "The Retail Day Trader" (Musa)
  - Trades FX and crypto, 2–5 hours/day
  - Has 1–3 broker accounts
  - Needs: fast order execution, clean charts, trade journal
  - Pain: broker apps are clunky, no unified analytics
  - Key features: imCharts, imJournal, multi-broker dashboard

PERSONA 2: "The Copy Trader" (Aisha)
  - Not actively trading; follows signal providers
  - Risk-averse; wants guardrails
  - Needs: provider discovery, risk controls, transparent track record
  - Pain: can't trust provider stats on other platforms
  - Key features: imCopying, verified provider badges, risk limits

PERSONA 3: "The Signal Provider" (Carlos)
  - Expert trader building a following
  - Needs: subscriber management, performance showcase, monetization
  - Pain: no platform that shows verified, audited track record
  - Key features: Provider dashboard, performance analytics, review system

PERSONA 4: "The Quant Learner" (Priya)
  - Learning trading through structured courses
  - Needs: high-quality content, progress tracking, community
  - Pain: generic YouTube content with no accountability
  - Key features: Academy, AI Coach, community forums
```

---

## MVP Scoping Checklist

```
For any new feature, MVP must:
  [ ] Solve the core pain (not the full vision)
  [ ] Work for the primary persona (not all personas)
  [ ] Be operable without supporting features
  [ ] Require ≤ 2 engineering weeks
  [ ] Have at least 1 measurable success metric
  [ ] Not require schema migrations with > 3 new tables

MVP is NOT:
  [ ] Everything the user asked for
  [ ] The polished version
  [ ] The version with all edge cases handled
  [ ] The version that scales to 1M users (optimize later)
```

---

## Platform Roadmap Phases

```
Phase 1 — CORE (current):
  ✅ IAM + RBAC (done)
  ✅ MT5 broker connection (done)
  ✅ imJournal basic (done)
  🔄 imCharts (in progress)
  🔄 imCopying (in progress)

Phase 2 — INTELLIGENCE:
  📋 Market Intelligence (AI analysis)
  📋 Journal AI Coach
  📋 Sentiment feed
  📋 Signal performance scoring

Phase 3 — MONETIZATION:
  📋 Subscription tiers (Free/Pro/Elite)
  📋 Provider commission system
  📋 Academy paid courses
  📋 Referral program

Phase 4 — SCALE:
  📋 Multi-region deployment
  📋 Mobile apps (React Native)
  📋 API marketplace
  📋 White-label platform
```

---

## Spec-Driven Development Entry Point

```
Every feature starts with a spec in:
  software-factory/specs/active/<feature-name>.spec.md

Spec lifecycle:
  1. Product creates spec (PRD above)
  2. Architect reviews and adds technical constraints
  3. Engineer creates tasks file: <feature>.tasks.md
  4. Tasks reference specific files, endpoints, schemas
  5. Implementation follows tasks
  6. Spec moved to software-factory/specs/archive/ after shipping
```

---

## Anti-Patterns

```
✗ Building without a spec (verbal agreement → scope creep)
✗ No "out of scope" section (everything becomes in scope by default)
✗ Success metrics defined after shipping (can't evaluate success)
✗ MVP includes "nice to have" features (delays core value delivery)
✗ PRD written by engineers alone (misses user perspective)
✗ PRD written by product alone (ignores technical constraints)
✗ Building for all personas equally in v1 (unfocused product)
✗ No RICE scoring (loudest voice picks features)
✗ Changing scope mid-sprint without a spec update
```
