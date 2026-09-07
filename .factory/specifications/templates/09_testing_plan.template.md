# Testing Plan: {{PRODUCT_TITLE}}

**Document ID:** TST-{{PROJECT_ID}}-001  
**Version:** {{VERSION}}  
**Status:** {{STATUS}} (Draft | Active | Verified)  
**Parent PRD:** PRD-{{PROJECT_ID}}-001  
**Parent App Flow:** FLW-{{PROJECT_ID}}-001  
**Target Specification:** {{TARGET_SPEC_ID}}  
**Lead QA Architect:** {{QA_LEAD}}  
**Last Updated:** {{DATE}}  

---

## 1. Quality Assurance Strategy & Test Pyramid

This Testing Plan governs automated and manual verification across all software layers for {{PRODUCT_TITLE}}.  
**Gate Rule:** No release candidate can proceed without 100% resolution of the Acceptance Criteria Traceability Matrix defined herein.

```
                   /\
                  /  \   E2E & Critical Journeys (Playwright)
                 /----\
                /      \   Integration & Contract Tests (FastAPI / Schemathesis)
               /--------\
              /          \   Unit & Domain Invariant Tests (pytest / Vitest)
             --------------
```

---

## 2. Test Strategy by Layer

| Test Layer | Framework / Tooling | Target Scope | Coverage Threshold | Execution Gate |
|------------|---------------------|--------------|--------------------|----------------|
| **Unit Tests** | `pytest` / `Vitest` | Domain models, business algorithms, pure utilities | >= 85% Line, >= 80% Branch | Gate G7 |
| **Integration Tests** | `pytest-asyncio` / `Testcontainers` | API endpoints, database transactions, cache invalidation | 100% of API endpoints | Gate G8 |
| **Contract Tests** | `Pydantic` / `OpenAPI validator` | Client-server schema compliance, payload validation | 100% of public routes | Gate G8 |
| **E2E / Browser QA** | `Playwright` / `BrowserOrchestrator` | Complete user journeys, DOM states, console & network errors | 100% of Critical Journeys | Gate G9 |
| **Accessibility (A11y)** | `axe-core` / `@axe-core/playwright` | WCAG 2.2 Level AA rules, ARIA roles, keyboard focus | Zero critical/serious violations | Gate G9 |
| **Performance & Load** | `Locust` / `k6` | P95 latency under target concurrency | Meets [NFR-001] (< 300ms) | Gate G11 |
| **Security SAST** | `ECC AgentShield` / `Bandit` / `Semgrep` | Static code analysis, dependency CVE audit | Zero High/Critical CVEs | Gate G10 |

---

## 3. Critical User Journey Verification (from App Flow)

*All journeys mapped from `FLW-{{PROJECT_ID}}-001` must have dedicated automated test coverage.*

### 3.1 Journey J-01: Authentication & Workspace Entry
- **Target Flow:** `SCR-01 -> SCR-02`
- **Automated Test File:** `tests/e2e/test_journey_auth_workspace.py`
- **Verification Criteria:**
  1. Valid credentials transition user cleanly to `/dashboard` within 1.0s.
  2. Invalid credentials trigger inline red error message without page reload.
  3. Session token persisted in secure, HttpOnly storage.

### 3.2 Journey J-02: Resource Inspection & Creation Flow
- **Target Flow:** `SCR-02 -> SCR-04 -> SCR-03`
- **Automated Test File:** `tests/e2e/test_journey_resource_lifecycle.py`
- **Verification Criteria:**
  1. User can navigate from dashboard table to creation wizard.
  2. Input validation traps malformed inputs before API submission.
  3. Newly created resource appears immediately in detail view and dashboard.

---

## 4. Test Data & Fixture Isolation Strategy

- **Database Fixtures:** Transactional isolation via test-scoped DB sessions that rollback upon test completion.
- **Mocking Policy:** Pure unit tests mock external network boundaries. Integration and E2E tests run against live, ephemeral test containers (PostgreSQL, Redis).
- **Synthetic Data Sets:** Standard test accounts and seed fixtures loaded from `.factory/specifications/{{PROJECT_ID}}/fixtures/seed.json`.

---

## 5. Requirements Traceability Matrix (PRD Acceptance Criteria → Test Cases)

*Every PRD acceptance criterion [AC-FR-xxx] MUST map directly to an automated test case. Unmapped criteria fail Quality Gate G0.5.*

| PRD Acceptance Criterion | Requirement Summary | Automated Test Suite / File | Specific Test Function / Case Name | Gate Link |
|--------------------------|---------------------|-----------------------------|------------------------------------|-----------|
| **[AC-FR-001-1]** | Token issuance upon valid credentials | `tests/test_auth_api.py` | `test_valid_login_issues_jwt_token` | Gate G7 |
| **[AC-FR-001-2]** | Rejection of expired tokens | `tests/test_auth_api.py` | `test_expired_token_rejected_with_401` | Gate G7 |
| **[AC-FR-002-1]** | Resource creation schema validation | `tests/test_resources_api.py`| `test_create_resource_with_valid_payload` | Gate G8 |
| **[AC-FR-002-2]** | Resource creation idempotency | `tests/test_resources_api.py`| `test_duplicate_resource_idempotency_key` | Gate G8 |
| **[AC-FR-003-1]** | E2E authentication happy path | `tests/e2e/test_auth_e2e.py` | `test_e2e_user_login_and_redirect` | Gate G9 |

---

## 6. Signoff & Gate Linkage

- [ ] All PRD acceptance criteria mapped to automated test cases
- [ ] Critical user journeys from App Flow covered by E2E test specs
- [ ] Multi-layer coverage gates verified
- [ ] Approved by QA Lead: {{APPROVER}} on {{SIGNOFF_DATE}}
