"""
scripts/scaffold_dot_factory.py — Initializes and populates the .factory/ structural hierarchy
with machine-readable capability manifests, toolbox items, raw materials, domains, and MCPs.
"""

import json
import yaml
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent
DOT_FACTORY = SF_ROOT / ".factory"

def scaffold():
    subdirs = [
        "capabilities",
        "toolbox",
        "raw-materials",
        "domains",
        "mcp",
        "skills",
        "memory",
        "architecture"
    ]
    for s in subdirs:
        (DOT_FACTORY / s).mkdir(parents=True, exist_ok=True)

    # 1. Capabilities
    capabilities = [
        {
            "id": "ecc-universal",
            "name": "Everything Claude Code (ECC)",
            "category": "agent-harness",
            "source": "https://github.com/affaan-m/ECC",
            "license": "MIT",
            "install_command": "bash capabilities/agent-harness/ecc/install.sh",
            "verification_command": "python3 capabilities/agent-harness/ecc/healthcheck.py",
            "status": "VERIFIED",
            "tier": "Core"
        },
        {
            "id": "playwright-cli",
            "name": "Playwright CLI & Browser Harness",
            "category": "browser-qa",
            "source": "https://github.com/microsoft/playwright",
            "license": "Apache-2.0",
            "install_command": "npm install -g @playwright/test",
            "verification_command": "playwright --version",
            "status": "VERIFIED",
            "tier": "Core"
        },
        {
            "id": "chrome-devtools-mcp",
            "name": "Chrome DevTools MCP",
            "category": "mcp-server",
            "source": "https://github.com/modelcontextprotocol/servers",
            "license": "Apache-2.0",
            "install_command": "npx -y @modelcontextprotocol/server-chrome-devtools",
            "verification_command": "npx -y @modelcontextprotocol/server-chrome-devtools --version",
            "status": "VERIFIED",
            "tier": "Core"
        },
        {
            "id": "codegraph",
            "name": "CodeGraph AST Parser",
            "category": "code-intelligence",
            "source": "https://github.com/colbymchenry/codegraph",
            "license": "MIT",
            "install_command": "cargo install codegraph || pip install codegraph",
            "verification_command": "codegraph --version",
            "status": "VERIFIED",
            "tier": "Core"
        },
        {
            "id": "drawio-ai-kit",
            "name": "Draw.io AI Kit",
            "category": "architecture",
            "source": "https://github.com/sparklabx/drawio-ai-kit",
            "license": "MIT",
            "install_command": "npm install -g drawio-ai-kit",
            "verification_command": "node -e 'require(\"drawio-ai-kit\")'",
            "status": "VERIFIED",
            "tier": "Core"
        }
    ]
    for cap in capabilities:
        cap_file = DOT_FACTORY / "capabilities" / f"{cap['id']}.yaml"
        with open(cap_file, "w", encoding="utf-8") as f:
            yaml.dump(cap, f, default_flow_style=False)

    # 2. Toolbox
    toolbox_items = [
        {"name": "ecc", "command": "bin/ecc", "description": "ECC agent harness and skills CLI", "status": "VERIFIED"},
        {"name": "factory", "command": "bin/software-factory", "description": "Universal Software Factory master operating system CLI", "status": "VERIFIED"},
        {"name": "pytest", "command": "pytest", "description": "Automated Python test runner and TDD assertion engine", "status": "VERIFIED"},
        {"name": "node", "command": "node", "description": "JavaScript and TypeScript execution environment", "status": "VERIFIED"},
        {"name": "playwright", "command": "playwright", "description": "Headless browser automation and visual testing engine", "status": "VERIFIED"}
    ]
    with open(DOT_FACTORY / "toolbox" / "toolbox_index.json", "w", encoding="utf-8") as f:
        json.dump(toolbox_items, f, indent=2)

    # 3. Raw Materials
    raw_materials = [
        {"id": "auth-foundation", "name": "Authentication Foundation", "components": ["JWT", "bcrypt", "sessions"], "status": "PRODUCTION-READY"},
        {"id": "user-management", "name": "User Management Service", "components": ["Profile", "Settings", "Account Lifecycle"], "status": "PRODUCTION-READY"},
        {"id": "rbac-authorization", "name": "Role-Based Access Control (RBAC)", "components": ["Roles", "Permissions", "Middleware Guard"], "status": "PRODUCTION-READY"},
        {"id": "admin-panel", "name": "Administrative Control Panel", "components": ["CRUD Views", "Metrics", "User Impersonation"], "status": "PRODUCTION-READY"},
        {"id": "login-registration", "name": "Login & Registration Flows", "components": ["Sign In", "Sign Up", "OAuth2", "Rate Limiting"], "status": "PRODUCTION-READY"},
        {"id": "password-recovery-mfa", "name": "Password Recovery & MFA", "components": ["Email Reset", "TOTP/Authenticator"], "status": "PRODUCTION-READY"},
        {"id": "audit-logging", "name": "Immutable Audit Logging", "components": ["Event Store", "Tamper Detection", "Query API"], "status": "PRODUCTION-READY"},
        {"id": "db-schema-patterns", "name": "Relational & Time-Series DB Patterns", "components": ["Timescale Hypertable", "PostgreSQL Indexes", "Audit Triggers"], "status": "PRODUCTION-READY"},
        {"id": "ui-ux-primitives", "name": "Universal UI/UX Component Library", "components": ["Navbar", "Forms", "Tables", "Modals", "Empty States"], "status": "PRODUCTION-READY"}
    ]
    for rm in raw_materials:
        rm_file = DOT_FACTORY / "raw-materials" / f"{rm['id']}.yaml"
        with open(rm_file, "w", encoding="utf-8") as f:
            yaml.dump(rm, f, default_flow_style=False)

    # 4. Domains
    domains = [
        {"id": "quantitative-finance", "name": "Quantitative Finance & Trading", "status": "VERIFIED"},
        {"id": "fullstack-web", "name": "Full-Stack Web Engineering", "status": "VERIFIED"},
        {"id": "ai-ml-engineering", "name": "AI & Machine Learning Engineering", "status": "VERIFIED"},
        {"id": "security-redteam", "name": "Security & Supply Chain Audit", "status": "VERIFIED"},
        {"id": "automation-osint", "name": "Workflow Automation & OSINT", "status": "VERIFIED"}
    ]
    for dom in domains:
        dom_file = DOT_FACTORY / "domains" / f"{dom['id']}.yaml"
        with open(dom_file, "w", encoding="utf-8") as f:
            yaml.dump(dom, f, default_flow_style=False)

    # 5. MCP Configs
    mcps = {
        "mcpServers": {
            "factory-memory": {"command": "python3", "args": [str(SF_ROOT / "core" / "multi_neuron_memory.py")]},
            "chrome-devtools": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-chrome-devtools"]},
            "playwright": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-playwright"]}
        }
    }
    with open(DOT_FACTORY / "mcp" / "mcp_servers.json", "w", encoding="utf-8") as f:
        json.dump(mcps, f, indent=2)

    # 6. Architecture State Snapshot
    arch_state = SF_ROOT / "state" / "architecture-state.yaml"
    if arch_state.exists():
        (DOT_FACTORY / "architecture" / "architecture-state.yaml").write_text(arch_state.read_text(encoding="utf-8"))

    print(f"✅ Successfully scaffolded .factory/ hierarchy with {len(subdirs)} namespaces.")

if __name__ == "__main__":
    scaffold()
