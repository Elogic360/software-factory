# Software Factory — Capability Bundles & Intelligent Tool Routing

## 1. Overview
Rather than flooding an AI coding agent's context window with dozens of irrelevant tools, the Software Factory packages capabilities into **12 Task-Based Capability Bundles**. 

The **Bundle Router** (`core/bundle_router.py`) maps the incoming task prompt to the minimal, highest-leverage bundle, maximizing completion accuracy and saving tokens.

---

## 2. The 12 Capability Bundles

| Bundle ID | Name | Primary Skills | Primary Tools |
| :--- | :--- | :--- | :--- |
| `browser-engineering` | Browser Engineering & Visual QA | browser-qa, accessibility, e2e-testing | playwright-cli, chrome-devtools-mcp, browser-use |
| `api-engineering` | API Engineering & Contracts | api-design, im-api-contracts | api_testing_engine, curl, postman_mcp |
| `database-engineering` | Database Engineering & ERD | database-postgresql, database-migrations | database_engine, psql, alembic |
| `frontend-engineering` | Frontend Engineering & Design | frontend-patterns, design-system | vite, tailwind, eslint |
| `backend-engineering` | Backend & Service Architecture | fastapi-patterns, backend-patterns | pytest, fastapi, uvicorn, docker |
| `security-engineering` | Security Engineering & Supply Chain | security-review, security-audit | ecc-agentshield, semgrep, trufflehog |
| `observability-sre` | Observability & SRE | im-observability, dashboard-builder | sentry, prometheus, grafana |
| `performance-engineering` | Performance Engineering | performance-engineering, benchmark | lighthouse, cprofile, py-spy |
| `architecture-governance` | Architecture Governance | im-architecture, hexagonal-architecture | architecture_state, spec_compiler |
| `target-verification` | Target-Driven Development (TDD) | tdd-workflow, eval-harness | target_engine, pytest, gate_checker |
| `cross-layer-debugging` | Cross-Layer Debugging & RCA | agent-introspection-debugging | cross_layer_debugger, log_correlator |
| `autonomous-manufacturing` | Autonomous Software Manufacturing | autonomous-loops, ralphinho-rfc-pipeline | manufacturing_line, bom_generator |

---

## 3. CLI Commands

```bash
# List all 12 capability bundles
python3 factory.py bundle list

# Route a query to the optimal capability bundle
python3 factory.py bundle route --query "Inspect checkout button and fix responsive layout"
```
