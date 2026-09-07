"""
Codex CLI Adapter — Configures AGENTS.md single source of truth for Codex,
and writes MCP config to .codex/mcp.json.
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
    return {"command": cmd, "args": args}

def write_mcp_config(target_project_dir: Path, sf_dir: Path) -> bool:
    servers = _load_mcp_servers(sf_dir)
    if not servers: return True
    codex_dir = target_project_dir / ".codex"
    codex_dir.mkdir(parents=True, exist_ok=True)
    mcp_path = codex_dir / "mcp.json"
    existing = {}
    if mcp_path.exists():
        try: existing = json.loads(mcp_path.read_text())
        except: existing = {}
    mcp_s = existing.get("mcpServers", {})
    for srv in servers:
        mcp_s[srv["id"]] = _make_mcp_entry(srv, sf_dir)
    existing["mcpServers"] = mcp_s
    mcp_path.write_text(json.dumps(existing, indent=2))
    return True

def setup_codex(target_project_dir: Path, sf_dir: Path) -> bool:
    agents_md = sf_dir / "AGENTS.md"
    target_agents = target_project_dir / "AGENTS.md"
    if agents_md.exists() and not target_agents.exists():
        target_agents.write_text(agents_md.read_text())
    write_mcp_config(target_project_dir, sf_dir)
    return True
