"""
Claude Code Agent Adapter — Configures CLAUDE.md, ecc@ecc, gstack,
and writes active MCP server configs to .claude/settings.json.
"""
import json
from pathlib import Path

try:
    import yaml
    _YAML_OK = True
except ImportError:
    _YAML_OK = False

MCP_TRUSTED_STATUSES = {"PRODUCTION_APPROVED", "VERIFIED"}


def _load_mcp_servers(sf_dir: Path):
    reg = sf_dir / "registries" / "mcp_registry.yaml"
    if not reg.exists() or not _YAML_OK:
        return []
    with open(reg) as f:
        data = yaml.safe_load(f) or {}
    return [s for s in data.get("mcp_servers", [])
            if s.get("evaluation_status") in MCP_TRUSTED_STATUSES]


def _make_mcp_entry(srv: dict, sf_dir: Path) -> dict:
    cmd = srv.get("command", "")
    args = list(srv.get("args") or [])
    env = {k: v for k, v in (srv.get("env") or {}).items()
           if not str(v).startswith("${")}
    # Resolve relative Python paths to absolute
    if cmd in ("python3", "python") and args:
        first = args[0]
        if first.startswith("./") or (first.endswith(".py") and not first.startswith("/")):
            args = [str(sf_dir / first)] + args[1:]
    entry = {"command": cmd, "args": args}
    if env:
        entry["env"] = env
    return entry


def write_mcp_config(target_project_dir: Path, sf_dir: Path) -> bool:
    servers = _load_mcp_servers(sf_dir)
    if not servers:
        return True
    claude_dir = target_project_dir / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    settings_path = claude_dir / "settings.json"
    existing = {}
    if settings_path.exists():
        try:
            existing = json.loads(settings_path.read_text())
        except Exception:
            existing = {}
    mcp_servers = existing.get("mcpServers", {})
    for srv in servers:
        mcp_servers[srv["id"]] = _make_mcp_entry(srv, sf_dir)
    existing["mcpServers"] = mcp_servers
    settings_path.write_text(json.dumps(existing, indent=2))
    return True


def setup_claude(target_project_dir: Path, sf_dir: Path) -> bool:
    claude_md = sf_dir / "CLAUDE.md"
    target_claude = target_project_dir / "CLAUDE.md"
    if claude_md.exists() and not target_claude.exists():
        target_claude.write_text(claude_md.read_text())
    write_mcp_config(target_project_dir, sf_dir)
    return True
