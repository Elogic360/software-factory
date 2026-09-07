# Software Factory — Universal AI-Native Engineering Capability Platform

> **A domain-general capability operating system** providing skills, tools, MCP servers, raw materials, quant engines, multi-agent adapters, and project scaffolding for AI coding agents to construct, test, and ship high-reliability software.

---

## 🏛️ Core Architecture

```
                  SOFTWARE FACTORY
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     SKILLS            TOOLS             MCP
        │                │                │
        └────────────────┼────────────────┘
                         │
                  CAPABILITY REGISTRY
                         │
        ┌────────────────┼────────────────┐
        │                │                │
 RAW MATERIALS       DOMAIN PACKS       KNOWLEDGE
        │                │                │
        └────────────────┼────────────────┘
                         │
                 PROJECT BOOTSTRAPPER
                         │
                ┌────────┴────────┐
                │                 │
             AGENTS            PROJECT
                │                 │
                └────────┬────────┘
                         │
                   BUILD SYSTEM
                         │
          ┌──────────────┼──────────────┐
          │              │              │
        TEST           SECURITY      OBSERVABILITY
          │              │              │
          └──────────────┼──────────────┘
                         │
                    VALIDATION
                         │
                       SHIP
```

---

## ⚡ Quick Start: Factory CLI

The unified `factory` CLI manages all capabilities, diagnostics, validation, and project bootstrapping:

```bash
# Health & integrity check (verifies all skills, registries, constitution)
python3 factory.py doctor

# List all capabilities across all tiers (Tier 0 Core to Tier 3 Domain)
python3 factory.py list

# Search capabilities
python3 factory.py search "quant"
python3 factory.py search "websocket"

# Inspect detailed capability metadata
python3 factory.py inspect codegraph

# Bootstrap the factory into any target project
python3 factory.py init /path/to/my-new-project --domain quantitative-finance

# Validate against formal JSON schema
python3 factory.py validate

# Comprehensive capability audit
python3 factory.py audit
```

---

## 🧰 Key Subsystems & Registries

| Subsystem | Location | Description |
| :--- | :--- | :--- |
| **Capability Registry** | `registries/capability_registry.yaml` | Canonical index of all tools, libraries, engines, and frameworks. |
| **MCP Registry** | `registries/mcp_registry.yaml` | Machine-readable manifest of verified MCP servers (`codegraph`, `gortex`, `playwright`, `ziplime`, `github`, etc.). |
| **Domain Packs** | `domains/` | Modular packs: `quantitative-finance`, `ai-ml`, `web-fullstack`, `security-redteam`, `automation-osint`. |
| **Raw Materials** | `raw-materials/` | Production-ready blueprints: Auth (JWT/RBAC), Realtime (WebSocket/Redis), Trading Risk Engine, RAG, Email. |
| **Multi-Agent Adapters** | `adapters/` | Seamless integrations for Antigravity, Claude Code (`ecc@ecc`), Codex, Cursor, OpenCode, and Copilot. |
| **Universal Toolbox** | `TOOLBOX.md` | Catalog of 207+ starred open-source engines, quant toolkits, scraping frameworks, and AI harnesses. |
| **Context Engine** | `context-engine/skill_selector.py` | Smart Skill Router matching queries with exact required skills, MCPs, and tools. |
| **Supreme Governance** | `constitution/CONSTITUTION.md` | Non-negotiable architectural boundaries, naming conventions, and service isolation rules. |

---

## 🔬 Testing & Continuous Verification

Run the test suite:
```bash
pytest tests/ -v
```

Automated GitHub Actions CI runs on every push: `.github/workflows/factory-ci.yml`.
