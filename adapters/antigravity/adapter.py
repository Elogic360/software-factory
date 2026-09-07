"""
Antigravity Agent Adapter — skills symlinks, rules, and MCP config for .gemini/settings.json.
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
    cmd = srv.get("command", ""); args = list(srv.get("args") or [])
    env = {k: v for k, v in (srv.get("env") or {}).items() if not str(v).startswith("${")}
    if cmd in ("python3","python") and args:
        first = args[0]
        if first.startswith("./") or (first.endswith(".py") and not first.startswith("/")):
            args = [str(sf_dir / first)] + args[1:]
    entry = {"command": cmd, "args": args}
    if env: entry["env"] = env
    return entry

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
    mcp_servers = existing.get("mcpServers", {})
    for srv in servers:
        mcp_servers[srv["id"]] = _make_mcp_entry(srv, sf_dir)
    existing["mcpServers"] = mcp_servers
    settings_path.write_text(json.dumps(existing, indent=2))
    return True

def setup_antigravity(target_project_dir: Path, sf_dir: Path) -> bool:
    target_agents = target_project_dir / ".agents"
    target_skills = target_agents / "skills"
    target_rules = target_agents / "rules"
    target_skills.mkdir(parents=True, exist_ok=True)
    target_rules.mkdir(parents=True, exist_ok=True)
    sf_skills = sf_dir / "skills"
    if sf_skills.exists():
        for skill in sf_skills.iterdir():
            if skill.is_dir():
                link = target_skills / skill.name
                if not link.exists():
                    try: link.symlink_to(skill, target_is_directory=True)
                    except Exception: pass
    rule_file = target_rules / "software-factory.md"
    rule_file.write_text("""# Antigravity Software Factory Governance
- Adhere strictly to the Engineering Constitution.
- Use `python3 software-factory/context-engine/skill_selector.py` for task routing.
- Validate changes incrementally with automated tests.
""")
    write_mcp_config(target_project_dir, sf_dir)
    return True
