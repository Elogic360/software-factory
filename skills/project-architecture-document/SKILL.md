---
name: project-architecture-document
description: Full Project Architecture Document Authoring — Synthesizes C1-C3 C4 models, deployment topologies, trust boundaries, failure domains, and disaster recovery strategies rendered from architecture-state.yaml.
---

# SKILL: Full Project Architecture Document Authoring
## Domain: Enterprise Architecture, C4 Modeling, SDD Station 04 / 05

**Activation triggers:** system architecture, C4 diagrams, project architecture, deployment topology, trust boundaries, disaster recovery, architecture-state.yaml, SDD Station 04.

---

## 1. Role & Engineering Law

The Project Architecture Document skill creates the unified master architectural document for the entire software product.  
It enforces the **Single Architecture Source of Truth Law**:
- The document is a rendered human-readable view over `.factory/architecture/architecture-state.yaml`.
- It cannot introduce ad-hoc containers or relationships not present in `architecture-state.yaml`.
- `architecture-state.yaml` must exist and pass schema validation before this document can be approved.

---

## 2. Document Structure & Required Sections

Every generated Project Architecture Document must follow `.factory/specifications/templates/07_project_architecture.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent PRD/TRD IDs, Target Specification, Architecture Model Source (`.factory/architecture/architecture-state.yaml`), Principal Architect, Date.
- **Section 1: Executive System Summary:** High-level operational purpose.
- **Section 2: C4 Architecture Models:**
  - `Level 1: System Context (C1)`: Mermaid `C4Context` diagram showing external actors, external systems, and platform perimeter.
  - `Level 2: Container Architecture (C2)`: Mermaid `C4Container` diagram detailing frontend, API gateway, backend services, workers, relational databases, and caches.
  - `Level 3: Component Architecture (C3)`: Mermaid `C4Component` diagram breaking down internal services, repositories, and controllers.
- **Section 3: Deployment Topology & Environments:**
  - Table describing Development, Staging, and Production infrastructure, isolation, and access controls.
- **Section 4: Trust Boundaries & Security Zones:**
  - Demarcation of Zone 1 (Public DMZ), Zone 2 (Internal Application Tier), and Zone 3 (Protected Data Tier).
- **Section 5: Failure Domains, Resiliency & Disaster Recovery:**
  - Failure isolation boundaries, circuit breaker policies, RTO (< 15 min), and RPO (< 5 min).
- **Section 6: Architecture State Synchronization & Verification.**

---

## 3. Validation Checklist (Quality Gate G0.5 Pre-Condition)

- [ ] `.factory/architecture/architecture-state.yaml` exists and is validated by `ArchitectureStateManager`.
- [ ] C1, C2, and C3 Mermaid diagrams are syntactically valid.
- [ ] Trust boundaries and isolation zones are explicitly defined.
- [ ] RTO and RPO targets are quantified.
- [ ] Document saved to `.factory/specifications/<project>/07_project_architecture.md`.
