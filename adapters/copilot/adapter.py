"""
GitHub Copilot Adapter — Configures .github/copilot-instructions.md
and writes MCP config to .vscode/settings.json (Copilot MCP extension format).
"""
import json
from pathlib import Path

try:
    import yaml; _YAML_OK = True
except ImportError:
    _YAML_OK = False

MCP_TRUSTED_STATUSES = {"PRODUCTION_APPROVED", "VERIFIED"}

def _load_mcp_servers(sf_dir):
    reg = sf_dir / "registries" / "mcp_registry.yaml"
    if not reg.exists() or not _YAML_OK: return []
    with open(reg) as f: data = yaml.safe_load(f) or {}
    return [s for s in data.get("mcp_servers", []) if s.get("evaluation_status") in MCP_TRUSTED_STATUSES]

def _make_mcp_entry(srv, sf_dir):
    cmd = srv.get("command",""); args = list(srv.get("args") or [])
    if cmd in ("python3","python") and args:
        first = args[0]
        if first.startswith("./") or (first.endswith(".py") and not first.startswith("/")):
            args = [str(sf_dir / first)] + args[1:]
    return {"type": "stdio", "command": cmd, "args": args}

def write_mcp_config(target_project_dir: Path, sf_dir: Path) -> bool:
    servers = _load_mcp_servers(sf_dir)
    if not servers: return True
    vscode_dir = target_project_dir / ".vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)
    settings_path = vscode_dir / "settings.json"
    existing = {}
    if settings_path.exists():
        try: existing = json.loads(settings_path.read_text())
        except: existing = {}
    mcp_s = existing.get("github.copilot.chat.mcp.servers", {})
    for srv in servers:
        mcp_s[srv["id"]] = _make_mcp_entry(srv, sf_dir)
    existing["github.copilot.chat.mcp.servers"] = mcp_s
    settings_path.write_text(json.dumps(existing, indent=2))
    return True

def setup_copilot(target_project_dir: Path, sf_dir: Path) -> bool:
    github_dir = target_project_dir / ".github"
    github_dir.mkdir(parents=True, exist_ok=True)
    instructions = github_dir / "copilot-instructions.md"
    if not instructions.exists():
        instructions.write_text("""# GitHub Copilot Instructions — Software Factory
- Follow software-factory/constitution/CONSTITUTION.md at all times.
- Use Spec-Driven Development: always consult PRD/TRD before implementing.
- All routes under /api/v1/, snake_case files/functions, PascalCase models.
""")
    write_mcp_config(target_project_dir, sf_dir)
    return True
