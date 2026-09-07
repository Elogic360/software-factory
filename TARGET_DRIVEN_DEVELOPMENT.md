# Software Factory — Target-Driven Development (TDD) Framework

## 1. Concept
Target-Driven Development (TDD) aligns Test-Driven Development with architectural Goal State Machines. Every feature, bug fix, or refactor must be represented by a **Target** with verifiable acceptance criteria.

---

## 2. Target Lifecycle State Machine

```text
  [ PLANNED ] ──► [ PROPOSED ] ──► [ IN_PROGRESS ] ──► [ IMPLEMENTED ]
                                          ▲                     │
                                          │                     ▼
  [ OBSERVED ] ◄── [ VERIFIED ] ◄── [ TESTED ] ◄───────────────┘
                                          │
                        (Failure Rollback)└─────────────────────► [ IN_PROGRESS ]
```

| State | Definition | Exit Gate Criteria |
| :--- | :--- | :--- |
| `PLANNED` | Goal registered in backlog | Detailed title, description, category, and acceptance criteria |
| `PROPOSED` | Work decomposed & assigned | Architecture boundaries checked, capability bundle mapped |
| `IN_PROGRESS` | Implementation active | Code being authored or refactored |
| `IMPLEMENTED` | Code complete | Static analysis, linting, and type checking passing |
| `TESTED` | Tests passing | 100% unit and integration test pass rate |
| `VERIFIED` | Formal gates passed | Contract tests, accessibility audit, and security review green |
| `OBSERVED` | Production/staging proof | Real runtime execution with evidence files persisted |

---

## 3. CLI Commands

```bash
# Display real-time target health & progress dashboard
python3 factory.py target dashboard

# Create a new goal target
python3 factory.py target create --id TGT-001 --title "Order Execution Service" --category api

# List all targets
python3 factory.py target list

# Transition target through lifecycle
python3 factory.py target transition --id TGT-001 --status PROPOSED
python3 factory.py target transition --id TGT-001 --status IN_PROGRESS
python3 factory.py target transition --id TGT-001 --status IMPLEMENTED
python3 factory.py target transition --id TGT-001 --status TESTED
python3 factory.py target transition --id TGT-001 --status VERIFIED
python3 factory.py target transition --id TGT-001 --status OBSERVED
```
