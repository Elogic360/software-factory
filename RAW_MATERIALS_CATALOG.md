# Raw Materials Catalog — Reusable Engineering Blueprints

| Module | Location | Blueprint & Contracts |
| :--- | :--- | :--- |
| **Authentication & RBAC** | `raw-materials/auth/` | JWT issuance, password hashing, RBAC permission checker (`auth_core.py`). |
| **Realtime WebSockets** | `raw-materials/realtime/` | Async ConnectionManager, channel subscription, Redis pub/sub (`connection_manager.py`). |
| **Trading Risk Engine** | `raw-materials/trading-engine/` | Position sizing, drawdown limits, pre-trade risk validation (`risk_engine.py`). |
| **AI RAG Retriever** | `raw-materials/ai-rag/` | Hybrid dense/sparse vector retriever and document chunking. |
| **Email Communications** | `raw-materials/email-communications/` | Multi-provider SMTP/Cloudflare agentic email dispatcher. |
