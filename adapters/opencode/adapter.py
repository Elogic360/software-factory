"""
OpenCode Adapter — Configures .opencode/ directory: instructions, AGENTS.md,
skill symlinks, and MCP config (.opencode/mcp.json).
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
    oc_dir = target_project_dir / ".opencode"
    oc_dir.mkdir(parents=True, exist_ok=True)
    mcp_path = oc_dir / "mcp.json"
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

def setup_opencode(target_project_dir: Path, sf_dir: Path) -> bool:
    oc_dir = target_project_dir / ".opencode"
    oc_dir.mkdir(parents=True, exist_ok=True)
    # Governance instructions
    instructions = oc_dir / "instructions.md"
    if not instructions.exists():
        instructions.write_text("""# OpenCode Software Factory Governance
- Strictly adhere to software-factory/constitution/CONSTITUTION.md.
- Follow Spec-Driven Development (SDD): consult PRD/TRD before implementing.
- All routes under /api/v1/, snake_case files, PascalCase models.
- Use python3 software-factory/context-engine/skill_selector.py for task routing.
""")
    # Link AGENTS.md
    agents_md = sf_dir / "AGENTS.md"
    target_agents = oc_dir / "AGENTS.md"
    if agents_md.exists() and not target_agents.exists():
        target_agents.write_text(agents_md.read_text())
    # Symlink skills
    sf_skills = sf_dir / "skills"
    oc_skills = oc_dir / "skills"
    if sf_skills.exists():
        oc_skills.mkdir(parents=True, exist_ok=True)
        for skill in sf_skills.iterdir():
            if skill.is_dir():
                link = oc_skills / skill.name
                if not link.exists():
                    try: link.symlink_to(skill, target_is_directory=True)
                    except Exception: pass
    # Write openwolf memory bridge (cytostack/openwolf compatible)
    memory_config = oc_dir / "openwolf.json"
    if not memory_config.exists():
        memory_config.write_text(json.dumps({
            "memory_dir": ".opencode/memory",
            "auto_checkpoint": True,
            "token_accounting": True
        }, indent=2))
    write_mcp_config(target_project_dir, sf_dir)
    return True
