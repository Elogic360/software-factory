---
name: implementation-plan-compiler
description: Implementation Plan Compiler — Compiles PRD, TRD, Architecture, App Flow, UI/UX, and Testing specifications into an ordered dependency DAG with work packages, assigned agents, required skills/MCPs, and rollback strategies.
---

# SKILL: Implementation Plan Compiler
## Domain: Project Engineering, Work Package Compilation, SDD Station 07 Entry

**Activation triggers:** implementation plan, work breakdown, task compilation, dependency graph, DAG, work orders, SDD Station 07.

---

## 1. Role & Engineering Law

The Implementation Plan Compiler skill transforms the full suite of SDD documents into an executable manufacturing schedule.  
It enforces the **Comprehensive Input Compilation Law**:
- The plan MUST NOT be generated from the PRD alone.
- It must explicitly consume and verify the inputs from:
  1. `01_prd.md` (Functional & Non-Functional requirements)
  2. `02_trd.md` (Technical constraints & interfaces)
  3. `03_app_flow.md` (User journeys & screen transitions)
  4. `04b_uiux_specification.md` (UI screens & component inventory)
  5. `05_schema_document.md` (Database models & migration sequence)
  6. `07_project_architecture.md` (Container & component structure)
  7. `09_testing_plan.md` (Layered test suites & acceptance criteria)
- Every task must form part of an acyclic directed graph (DAG).

---

## 2. Document Structure & Required Sections

Every generated Implementation Plan must follow `.factory/specifications/templates/08_implementation_plan.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent PRD/TRD/Architecture IDs, Delivery Lead, Date.
- **Section 1: Plan Synthesis & Input Verification:** Checkboxes verifying all prerequisite SDD documents.
- **Section 2: Work Breakdown Structure & Phases:**
  - Mermaid `gantt` chart illustrating execution phases and dependencies.
- **Section 3: Ordered Task Specifications & Dependency DAG:**
  - Per-task specification (`TSK-001`, `TSK-002`, etc.):
    - Station (e.g. Station 04 Data Architecture, Station 08 Backend, etc.)
    - Assigned Agent
    - Traceability (linked PRD/TRD/Schema items)
    - Dependencies (`dependencies: [TSK-001]`)
    - Required Skills (e.g. `fastapi-patterns`, `database-postgresql`)
    - Required MCP Servers (e.g. `postgres`, `playwright`)
    - Required Raw Materials (e.g. templates, scaffolds)
    - Complexity / Risk rating
    - Clear Acceptance Criteria
    - Explicit Rollback Procedure
- **Section 4: Execution Readiness Signoff.**

---

## 3. Validation Checklist (Quality Gate G5 & G0.5 Pre-Condition)

- [ ] All 7 prerequisite SDD documents are cited and verified.
- [ ] Task dependency graph has zero circular dependencies (valid DAG).
- [ ] Every task specifies required skills, MCP servers, and assigned agent.
- [ ] Every task includes a concrete rollback procedure.
- [ ] Document saved to `.factory/specifications/<project>/08_implementation_plan.md`.
