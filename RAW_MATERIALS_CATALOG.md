# Raw Materials Catalog — Universal Production-Ready Building Blocks

> **Standard**: Every raw material is `PRODUCTION-READY`, fully tested, schema-verified, and evidenced.  
> Components here can be directly auto-assembled into any software product by the Software Factory.

---

## 1. High-Frequency Production Building Blocks

| Raw Material | Location | Core Primitives & Features | Verification & Tests | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Authentication Foundation** | `raw-materials/auth/` | JWT token generation, verification, bcrypt password hashing (`auth_core.py`). | `tests/test_raw_materials.py` | `PRODUCTION-READY` |
| **User Management** | `raw-materials/user-management/` | User registration, profile updates, account activation/suspension (`user_service.py`). | `tests/test_raw_materials.py` | `PRODUCTION-READY` |
| **RBAC Authorization** | `raw-materials/auth/` | Multi-role permission checks, role hierarchy, route protection middleware. | `tests/test_raw_materials.py` | `PRODUCTION-READY` |
| **Admin Panel & Audit Logs** | `raw-materials/admin-panel/` | Immutable audit trail, administrative metrics, user impersonation safety guard (`admin_service.py`). | `tests/test_raw_materials.py` | `PRODUCTION-READY` |
| **Database Schema Patterns** | `raw-materials/db-patterns/` | Universal PostgreSQL DDL: UUIDs, RBAC tables, audit logs, idempotency keys (`schema_patterns.sql`). | `tests/test_api_and_database.py` | `PRODUCTION-READY` |
| **UI/UX Primitives** | `raw-materials/ui-ux/` | Design tokens, nav, data tables, modals, dashboards, empty/loading/error states (`ui_primitives.json`). | `tests/test_browser_and_qa.py` | `PRODUCTION-READY` |
| **Realtime WebSockets** | `raw-materials/realtime/` | Async ConnectionManager, channel subscription, Redis pub/sub (`connection_manager.py`). | `tests/test_learning_and_golden.py` | `PRODUCTION-READY` |
| **Trading Risk Engine** | `raw-materials/trading-engine/` | Position sizing, drawdown limits, pre-trade risk validation (`risk_engine.py`). | `tests/test_learning_and_golden.py` | `PRODUCTION-READY` |
| **Email Communications** | `raw-materials/email-communications/` | Multi-provider SMTP / Cloudflare agentic email dispatcher (`mailflare`). | `tests/test_learning_and_golden.py` | `PRODUCTION-READY` |

---

## 2. Assembly Protocol
When initializing or scaffolding an application, the Factory Spec Compiler (`core/spec_compiler.py`) copies or links requested raw materials directly into the target project under `.factory/components/` and registers them in the target project's `project.yaml`.
