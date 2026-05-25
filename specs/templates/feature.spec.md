# SPEC: [Feature Name]
**Status:** Draft | Review | Approved | In Progress | Done
**Date:** YYYY-MM-DD
**Author:** [name]
**Domain:** [journal | auth | copy_trading | imcharts | market_intelligence | academy]
**Backend:** [market :8000 | expert :8002 | imi :8003]

---

## Problem Statement

[1–2 sentences: what user pain does this solve, and why now]

---

## User Stories

- As a **[persona]**, I want to **[action]** so that **[benefit]**.
- As a **[persona]**, I want to **[action]** so that **[benefit]**.

---

## Acceptance Criteria

- [ ] [User can do X]
- [ ] [System responds within Y ms]
- [ ] [Edge case Z returns appropriate error]
- [ ] [Security: only authorized users can access]
- [ ] [Audit: action is logged]

---

## Technical Design

### API Endpoints
```
METHOD /api/v1/<resource>
  Auth: Bearer JWT required
  Request: { field: type }
  Response: { field: type }
  Errors: 400 (validation), 401 (auth), 403 (permission), 404 (not found)
```

### Database Changes
```sql
-- New tables / columns / indexes
-- Migration file: alembic/versions/<revision>_<description>.py
```

### Frontend Changes
```
Component: app/src/modules/<module>/components/<Component>.tsx
Hook:      app/src/modules/<module>/hooks/use<Feature>.ts
Store:     app/src/modules/<module>/store/<feature>Store.ts  (if needed)
```

### WebSocket Events (if realtime)
```
Channel: <resource>.<id>
Payload: { type: string, data: object }
```

---

## Out of Scope

- [explicit non-goal 1]
- [explicit non-goal 2]

---

## Dependencies

- [ ] [upstream feature or service this depends on]
- [ ] [DB schema change must land before this]

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [risk description] | H/M/L | H/M/L | [mitigation plan] |

---

## Success Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| [metric name] | [current] | [goal] |

---

## Implementation Notes

[Anything an implementing engineer should know that's not obvious from the design]

---

## Testing Plan

- [ ] Unit test: [what to test]
- [ ] Integration test: [API endpoint test]
- [ ] E2E test: [user journey]
- [ ] Load test: [if applicable]
