# Testing Plan: QuantumVault Ledger Engine

**Document ID:** TST-QV-001  
**Version:** 1.0.0  
**Status:** Active  
**Parent PRD:** PRD-QV-001  
**Parent App Flow:** FLW-QV-001  
**Target Specification:** SPEC-QUANTUM-VAULT-2026  
**Lead QA Architect:** Principal QA Engineer  
**Last Updated:** 2026-09-07  

---

## 1. Quality Assurance Strategy & Test Pyramid

This Testing Plan governs automated and manual verification across all software layers for QuantumVault.  
**Gate Rule:** No release candidate can proceed without 100% resolution of the Acceptance Criteria Traceability Matrix.

```
                   /\
                  /  \   E2E & Critical Journeys (Playwright)
                 /----\
                /      \   Integration & Contract Tests (FastAPI / Testcontainers)
               /--------\
              /          \   Unit & Domain Invariant Tests (pytest / Vitest)
             --------------
```

---

## 2. Test Strategy by Layer

| Test Layer | Framework / Tooling | Target Scope | Coverage Threshold | Execution Gate |
|------------|---------------------|--------------|--------------------|----------------|
| **Unit Tests** | `pytest` | Domain models, double-entry arithmetic, token crypto | >= 90% Line, >= 85% Branch | Gate G7 |
| **Integration Tests** | `pytest-asyncio` / `Testcontainers` | API endpoints, serializable transactions, Redis caching | 100% of API endpoints | Gate G8 |
| **Contract Tests** | `Pydantic v2` / `OpenAPI Validator` | OpenAPI 3.1 request/response validation | 100% of public routes | Gate G8 |
| **E2E / Browser QA** | `Playwright` / `BrowserOrchestrator` | Critical user journeys, DOM state matrix, console/network error audit | 100% of Critical Journeys | Gate G9 |
| **Accessibility (A11y)** | `axe-core` | WCAG 2.2 Level AA rules, ARIA roles, keyboard navigation | Zero violations | Gate G9 |
| **Performance & Load** | `Locust` | P95 latency under 1,000 RPS concurrency | Meets [NFR-001] (< 150ms) | Gate G11 |
| **Security SAST** | `ECC AgentShield` / `Bandit` | Static analysis, dependency CVE audit | Zero High/Critical CVEs | Gate G10 |

---

## 3. Critical User Journey Verification (from App Flow)

### 3.1 Journey J-01: Treasury Authentication & Balance Inspection
- **Target Flow:** `SCR-01 -> SCR-02`
- **Automated Test File:** `tests/e2e/test_journey_auth_dashboard.py`
- **Verification Criteria:**
  1. Valid credentials transition operator to `/dashboard` within 1.0s.
  2. Invalid credentials display inline red alert banner without page reload.
  3. Live WebSocket connection established and stream icon indicates green.

### 3.2 Journey J-02: Idempotent Transfer Execution & Settlement
- **Target Flow:** `SCR-02 -> SCR-04 -> SCR-03`
- **Automated Test File:** `tests/e2e/test_journey_transfer_settlement.py`
- **Verification Criteria:**
  1. Transfer form validates balance before submission.
  2. Idempotent key deduplication verified: submitting identical key returns identical receipt.
  3. Reconciled balances update instantaneously on detail screen `SCR-03`.

---

## 4. Test Data & Fixture Isolation Strategy

- **Database Isolation:** Ephemeral PostgreSQL 16 container spawned via `testcontainers`. Each test runs inside an isolated transaction rolled back during teardown.
- **Mocking Boundaries:** External banking rails are mocked with deterministic stubs. Core database and Redis services run live.

---

## 5. Requirements Traceability Matrix (PRD Acceptance Criteria → Test Cases)

| PRD Acceptance Criterion | Requirement Summary | Automated Test Suite / File | Specific Test Function / Case Name | Gate Link |
|--------------------------|---------------------|-----------------------------|------------------------------------|-----------|
| **[AC-FR-001-1]** | Balance calculation from ledger within 50ms | `tests/test_ledger_service.py` | `test_balance_calculated_from_ledger_within_50ms` | Gate G7 |
| **[AC-FR-001-2]** | Account creation uniqueness and FK constraint | `tests/test_account_models.py` | `test_account_creation_enforces_unique_number_and_fk` | Gate G7 |
| **[AC-FR-002-1]** | Double-entry invariant (debits equal credits) | `tests/test_ledger_service.py` | `test_double_entry_debit_credit_sum_zero` | Gate G7 |
| **[AC-FR-002-2]** | Idempotency deduplication returns cached receipt | `tests/test_transfer_api.py` | `test_duplicate_idempotency_key_returns_cached_receipt` | Gate G8 |
| **[AC-FR-003-1]** | WebSocket mutation broadcast within 150ms | `tests/test_websocket_stream.py` | `test_websocket_stream_dispatches_mutation_within_150ms` | Gate G8 |
| **[AC-FR-003-2]** | Reconnected client receives full state resync | `tests/test_websocket_stream.py` | `test_reconnected_websocket_receives_state_resync` | Gate G8 |

---

## 6. Signoff & Gate Linkage

- [x] All PRD acceptance criteria mapped to automated test cases
- [x] Critical user journeys from App Flow covered by E2E test specs
- [x] Multi-layer coverage gates verified
- [x] Approved by Principal QA Engineer on 2026-09-07
