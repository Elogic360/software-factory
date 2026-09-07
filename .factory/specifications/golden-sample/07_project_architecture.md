# Full Project Architecture Document: QuantumVault Ledger Engine

**Document ID:** ARC-PROJ-QV-001  
**Version:** 1.0.0  
**Status:** Master Architectural Baseline  
**Parent PRD & TRD:** PRD-QV-001 / TRD-QV-001  
**Target Specification:** SPEC-QUANTUM-VAULT-2026  
**Architecture Model Source:** `.factory/architecture/architecture-state.yaml`  
**Principal Software Architect:** Principal Systems Architect  
**Last Updated:** 2026-09-07  

---

## 1. Executive System Summary

This document unifies the entire architectural specification for the QuantumVault ledger platform, defining its system context, container topology, internal component organization, deployment infrastructure, and disaster recovery procedures.  
**Gate Rule:** This document is the rendered view over `.factory/architecture/architecture-state.yaml`.

---

## 2. C4 Architecture Models

### 2.1 Level 1: System Context (C1)

```mermaid
C4Context
    title System Context diagram for QuantumVault Ledger Engine
    
    Person(operator, "Treasury Operator", "Monitors liquidity, submits transfers, and reviews balances.")
    Person(auditor, "Compliance Auditor", "Inspects tamper-proof audit trails and transaction lineages.")
    
    Enterprise_Boundary(b0, "QuantumVault Platform Perimeter") {
        System(core_vault, "QuantumVault Core", "Executes real-time double-entry settlement and streaming telemetry.")
    }
    
    System_Ext(idp, "Enterprise Identity Provider", "Authenticates institutional operators via OIDC.")
    System_Ext(fed_wire, "Banking Settlement Network", "Upstream correspondent banking rails.")

    Rel(operator, core_vault, "Submits transfers & streams ledger", "HTTPS/WSS")
    Rel(auditor, core_vault, "Queries audit logs", "HTTPS")
    Rel(core_vault, idp, "Validates JWT credentials", "HTTPS/OAuth2")
    Rel(core_vault, fed_wire, "Reports external settlement status", "mTLS/REST")
```

### 2.2 Level 2: Container Architecture (C2)

```mermaid
C4Container
    title Container diagram for QuantumVault Ledger Engine

    Person(operator, "Operator", "Web Client")

    Container_Boundary(c1, "QuantumVault System") {
        Container(spa, "Treasury Web Console", "TypeScript, React, Tailwind", "Real-time ledger UI with live streaming tables.")
        Container(api_gateway, "Edge API Gateway", "Nginx / Reverse Proxy", "SSL termination, rate-limiting, and routing.")
        Container(backend_api, "Ledger API Service", "Python 3.12, FastAPI", "Executes domain logic, REST routes, and WebSocket server.")
        Container(worker_engine, "Settlement Worker", "Python Celery / Async Worker", "Processes asynchronous journal indexing and audit dispatch.")
        ContainerDb(db_relational, "Primary Database", "PostgreSQL 16", "Stores double-entry journals, accounts, and audit records.")
        ContainerDb(cache_redis, "Cache & Broker", "Valkey / Redis 7", "Caches balances, idempotency keys, and powers WebSocket pub/sub.")
    }

    Rel(operator, spa, "Operates console", "HTTPS")
    Rel(spa, api_gateway, "API requests & WebSocket", "JSON/WSS")
    Rel(api_gateway, backend_api, "Proxies traffic", "HTTP/TCP")
    Rel(backend_api, db_relational, "Reads / Writes (Serializable)", "SQL/TCP")
    Rel(backend_api, cache_redis, "Caches & Publishes mutations", "RESP/TCP")
    Rel(worker_engine, cache_redis, "Pulls queue jobs", "RESP/TCP")
    Rel(worker_engine, db_relational, "Persists audit indices", "SQL/TCP")
```

### 2.3 Level 3: Component Architecture (C3 - Ledger API Service)

```mermaid
C4Component
    title Component diagram for Ledger API Service

    Container_Boundary(b_comp, "Ledger API Service Container") {
        Component(ctrl_auth, "Auth Controller", "FastAPI Router", "Validates JWT tokens and manages session states.")
        Component(ctrl_transfers, "Transfer Controller", "FastAPI Router", "Receives and validates idempotent transfer payloads.")
        Component(svc_ledger, "Ledger Domain Service", "Python Service Class", "Enforces double-entry balance arithmetic and invariants.")
        Component(repo_ledger, "Ledger Repository", "SQLAlchemy / Asyncpg", "Executes serializable database transactions.")
        Component(stream_gw, "WebSocket Stream Gateway", "FastAPI WebSocket", "Broadcasting state mutations to connected clients.")
    }

    Rel(ctrl_transfers, svc_ledger, "Executes transfer instruction")
    Rel(svc_ledger, repo_ledger, "Commits journal transaction")
    Rel(svc_ledger, stream_gw, "Dispatches mutation event")
```

---

## 3. Deployment Topology & Environments

| Environment | Host Infrastructure | Isolation Level | Access Control |
|-------------|---------------------|-----------------|----------------|
| **Development** | Local Docker Compose | Container network | Local developer host |
| **Staging** | Multi-node Kubernetes Staging | Namespace isolated | Tailscale VPN + Staging SSO |
| **Production** | Multi-AZ Kubernetes (AWS EKS) | Private VPC + Subnet Isolation | Zero-Trust Bastion + Mutual TLS |

---

## 4. Trust Boundaries & Security Zones

1. **Zone 1 (Public DMZ):** Cloudflare Edge -> Ingress Gateway (DDoS protection, TLS termination).
2. **Zone 2 (Application Tier):** API Service pods and Worker pods in private subnets with strict egress filtering.
3. **Zone 3 (Data Tier):** Managed PostgreSQL cluster and Redis instances restricted to Zone 2 security group.

---

## 5. Failure Domains, Resiliency & Disaster Recovery

- **Failure Isolation:** Asynchronous worker or cache failure will not block read access to ledger balances.
- **Circuit Breaking:** External network timeouts trip circuit breakers to prevent connection pool starvation.
- **RTO (Recovery Time Objective):** < 15 minutes via automated pod restart and read-replica promotion.
- **RPO (Recovery Point Objective):** < 5 minutes via continuous WAL streaming to cloud object storage.

---

## 6. Architecture State Synchronization & Verification

- [x] System Context, Containers, and Components match `.factory/architecture/architecture-state.yaml`
- [x] Trust boundaries and deployment topologies documented
- [x] Disaster recovery parameters (RTO/RPO) defined
- [x] Approved by Principal Systems Architect on 2026-09-07
