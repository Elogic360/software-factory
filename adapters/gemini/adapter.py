"""
Gemini CLI Adapter — Configures GEMINI.md, central memory integration,
progressive skills loading, and MCP config to .gemini/settings.json.
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
    gemini_dir = target_project_dir / ".gemini"
    gemini_dir.mkdir(parents=True, exist_ok=True)
    settings_path = gemini_dir / "settings.json"
    existing = {}
    if settings_path.exists():
        try: existing = json.loads(settings_path.read_text())
        except: existing = {}
    mcp_s = existing.get("mcpServers", {})
    for srv in servers:
        mcp_s[srv["id"]] = _make_mcp_entry(srv, sf_dir)
    existing["mcpServers"] = mcp_s
    settings_path.write_text(json.dumps(existing, indent=2))
    return True

def setup_gemini(target_project_dir: Path, sf_dir: Path) -> bool:
    gemini_md = sf_dir / "GEMINI.md"
    target_gemini = target_project_dir / "GEMINI.md"
    if gemini_md.exists() and not target_gemini.exists():
        target_gemini.write_text(gemini_md.read_text())
    write_mcp_config(target_project_dir, sf_dir)
    return True
