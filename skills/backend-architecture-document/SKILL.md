---
name: backend-architecture-document
description: Backend Architecture Document Authoring — Specifies service and module boundaries, API surface, async queues, multi-tier caching, circuit breaking, and security perimeters aligned with C4 Container/Component models.
---

# SKILL: Backend Architecture Document Authoring
## Domain: Backend Engineering, Distributed Systems, SDD Station 04 / 05

**Activation triggers:** backend architecture, service boundaries, API surface, queue design, caching strategy, circuit breakers, security perimeter, SDD Station 05.

---

## 1. Role & Engineering Law

The Backend Architecture Document skill authors the definitive technical narrative for backend services, APIs, asynchronous pipelines, and security perimeters.  
It enforces the **Narrative-to-Model Alignment Law**:
- It narrates and expands upon the C4 Container and Component models defined in `architecture-state.yaml`.
- It does not invent separate, unmodeled components or protocols.
- Every API route, queue topic, and cache tier must align with the system boundaries.

---

## 2. Document Structure & Required Sections

Every generated Backend Architecture Document must follow `.factory/specifications/templates/06_backend_architecture.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent TRD ID, Target Specification, Lead Backend Architect, Date.
- **Section 1: Architectural Narrative & Scope:** Context and link to `architecture-state.yaml`.
- **Section 2: Service & Module Boundaries:**
  - Mermaid diagram showing edge, core boundaries, async workers, and databases.
  - Clear modular bounded context descriptions.
- **Section 3: API Surface Summary:**
  - Route table with Route Pattern, Method, Protocol, Auth Requirements, Contract description.
- **Section 4: Inter-Service & Component Data Flow:**
  - Synchronous request pipelines vs. asynchronous event pipelines.
- **Section 5: Background Jobs, Queues & Task Workers:**
  - Queue engine, concurrency limits, worker autoscaling, and Dead Letter Queue (DLQ) retry semantics.
- **Section 6: Multi-Tier Caching Strategy:**
  - L1 in-memory vs. L2 distributed cache, TTLs, and cache-aside invalidation triggers.
- **Section 7: Third-Party Integrations & Resilience:**
  - External dependencies, protocols, and circuit breaker configs.
- **Section 8: Error Handling & Retry Architecture:**
  - Standardized JSON error response envelope, error codes, and circuit breaker trip thresholds.
- **Section 9: Security Perimeter & Access Controls:**
  - Auth token issuance and verification, RBAC/ABAC enforcement, and secrets isolation.
- **Section 10: Verification & Gate Signoff.**

---

## 3. Validation Checklist (Quality Gate G0.5 Pre-Condition)

- [ ] All module boundaries align with C4 Container/Component models.
- [ ] API routes specify authentication requirements and HTTP methods.
- [ ] Dead letter queues and retry backoffs are defined.
- [ ] Multi-tier cache TTLs and invalidation policies are explicit.
- [ ] Document saved to `.factory/specifications/<project>/06_backend_architecture.md`.
