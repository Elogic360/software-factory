# Full Project Architecture Document: {{PRODUCT_TITLE}}

**Document ID:** ARC-PROJ-{{PROJECT_ID}}-001  
**Version:** {{VERSION}}  
**Status:** {{STATUS}} (Draft | Approved | Master Architectural Baseline)  
**Parent PRD & TRD:** PRD-{{PROJECT_ID}}-001 / TRD-{{PROJECT_ID}}-001  
**Target Specification:** {{TARGET_SPEC_ID}}  
**Architecture Model Source:** `.factory/architecture/architecture-state.yaml`  
**Principal Software Architect:** {{PRINCIPAL_ARCHITECT}}  
**Last Updated:** {{DATE}}  

---

## 1. Executive System Summary

This document serves as the master architectural blueprint for {{PRODUCT_TITLE}}, unifying the system context, container distribution, internal component breakdown, operational topology, security trust boundaries, and disaster recovery strategies.  
**Gate Rule:** This document is a rendered view over `.factory/architecture/architecture-state.yaml`. Any discrepancy between this document and `architecture-state.yaml` represents architectural drift and fails Quality Gate 0.5.

---

## 2. C4 Architecture Models

### 2.1 Level 1: System Context (C1)
Describes how users and external enterprise systems interact with {{PRODUCT_TITLE}}.

```mermaid
C4Context
    title System Context diagram for {{PRODUCT_TITLE}}
    
    Person(user, "Authenticated User", "Operates platform, reviews telemetry and executes actions.")
    Person(admin, "Platform Admin", "Configures system parameters and monitors health.")
    
    Enterprise_Boundary(b0, "{{PRODUCT_TITLE}} Platform Boundary") {
        System(core_system, "{{PRODUCT_TITLE}} System", "Delivers core domain capabilities, APIs, and real-time streaming.")
    }
    
    System_Ext(idp, "Identity Provider", "Authenticates enterprise user credentials via OIDC.")
    System_Ext(ext_broker, "External Market / Service API", "Upstream data feeds and partner webhooks.")

    Rel(user, core_system, "Uses via Web / REST & WebSockets", "HTTPS/WSS")
    Rel(admin, core_system, "Manages via Admin Console", "HTTPS")
    Rel(core_system, idp, "Validates identities against", "HTTPS/OAuth2")
    Rel(core_system, ext_broker, "Consumes upstream feeds from", "HTTPS/TLS")
```

### 2.2 Level 2: Container Architecture (C2)
Illustrates high-level execution units, web clients, API backend services, data stores, and message buses.

```mermaid
C4Container
    title Container diagram for {{PRODUCT_TITLE}}

    Person(user, "User", "Web Browser / Client")

    Container_Boundary(c1, "{{PRODUCT_TITLE}}") {
        Container(spa, "Single Page App / UI", "TypeScript, React, Tailwind", "Delivers responsive interactive frontend.")
        Container(api_gateway, "API Gateway / Reverse Proxy", "Nginx / Envoy", "Handles SSL termination, rate-limiting, and routing.")
        Container(backend_api, "Backend Core Service", "FastAPI / Node.js", "Executes business logic, domain rules, and REST/WS APIs.")
        Container(worker_engine, "Background Task Worker", "Python Celery / BullMQ", "Processes asynchronous tasks and event dispatch.")
        ContainerDb(db_relational, "Primary Database", "PostgreSQL 16", "Stores relational entities, transactions, and audit records.")
        ContainerDb(cache_redis, "Distributed Cache & Broker", "Redis / Valkey", "Provides transient caching, rate limiting, and pub/sub.")
    }

    Rel(user, spa, "Delivers UI into browser", "HTTPS")
    Rel(spa, api_gateway, "API requests", "JSON/HTTPS")
    Rel(api_gateway, backend_api, "Proxies requests to", "HTTP")
    Rel(backend_api, db_relational, "Reads / Writes", "SQL/TCP")
    Rel(backend_api, cache_redis, "Caches & Dispatches events", "RESP/TCP")
    Rel(worker_engine, cache_redis, "Pulls queued jobs", "RESP/TCP")
    Rel(worker_engine, db_relational, "Persists processed state", "SQL/TCP")
```

### 2.3 Level 3: Component Architecture (C3 - Backend Core)

```mermaid
C4Component
    title Component diagram for Backend Core Service

    Container_Boundary(b_comp, "Backend Core Container") {
        Component(ctrl_auth, "Auth Controller", "FastAPI Router", "Handles token issuance and verification.")
        Component(ctrl_domain, "Domain Controller", "FastAPI Router", "Validates input payloads and routes requests.")
        Component(svc_domain, "Domain Service", "Python Service Class", "Executes business rules and state machines.")
        Component(repo_data, "Data Repository", "SQLAlchemy / Asyncpg", "Encapsulates queries, transactions, and models.")
        Component(event_publisher, "Event Publisher", "Redis Client", "Publishes async events for workers.")
    }

    Rel(ctrl_domain, svc_domain, "Invokes operations on")
    Rel(svc_domain, repo_data, "Persists domain changes via")
    Rel(svc_domain, event_publisher, "Emits state events via")
```

---

## 3. Deployment Topology & Environments

| Environment | Host Infrastructure | Isolation Level | Access Control |
|-------------|---------------------|-----------------|----------------|
| **Development** | Local Docker Compose | Container network | Developer workstations |
| **Staging** | Kubernetes Staging Cluster | Namespace isolated | VPN + Staging SSO |
| **Production** | Multi-AZ Kubernetes (AWS EKS / Bare-Metal) | Full VPC Isolation | Strict Zero-Trust Bastion + Mutual TLS |

---

## 4. Trust Boundaries & Security Zones

1. **Zone 1 (Public DMZ):** Cloudflare / CDN and Edge Ingress. SSL termination and DDoS mitigation.
2. **Zone 2 (Internal Application Tier):** API Gateway, Backend API pods, Background Worker pods. Mutual TLS authentication.
3. **Zone 3 (Protected Data Tier):** PostgreSQL cluster with read replicas and Redis in private subnets with strict security groups.

---

## 5. Failure Domains, Resiliency & Disaster Recovery

- **Failure Isolation:** Any individual worker failure does not impact synchronous API serving.
- **Circuit Breaking:** External integration failures degrade gracefully without cascading container crashes.
- **RTO (Recovery Time Objective):** < 15 minutes. Automated pod rescheduling and DB failover.
- **RPO (Recovery Point Objective):** < 5 minutes. Continuous WAL streaming and hourly database snapshots.

---

## 6. Architecture State Synchronization & Verification

- [ ] System Context, Containers, and Components match `.factory/architecture/architecture-state.yaml`
- [ ] Trust boundaries and deployment topologies documented
- [ ] Disaster recovery parameters (RTO/RPO) defined
- [ ] Approved by Principal Architect: {{APPROVER}} on {{SIGNOFF_DATE}}
