"""Cursor IDE Adapter — .cursor/rules, skills directory, and MCP config."""
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
    if cmd in ("python3","python") and args:
        first = args[0]
        if first.startswith("./") or (first.endswith(".py") and not first.startswith("/")):
            args = [str(sf_dir / first)] + args[1:]
    return {"command": cmd, "args": args}

def write_mcp_config(target_project_dir: Path, sf_dir: Path) -> bool:
    servers = _load_mcp_servers(sf_dir)
    if not servers: return True
    cursor_dir = target_project_dir / ".cursor"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    mcp_path = cursor_dir / "mcp.json"
    existing = {}
    if mcp_path.exists():
        try: existing = json.loads(mcp_path.read_text())
        except: existing = {}
    mcp_servers = existing.get("mcpServers", {})
    for srv in servers:
        mcp_servers[srv["id"]] = _make_mcp_entry(srv, sf_dir)
    existing["mcpServers"] = mcp_servers
    mcp_path.write_text(json.dumps(existing, indent=2))
    return True

def setup_cursor(target_project_dir: Path, sf_dir: Path) -> bool:
    cursor_dir = target_project_dir / ".cursor"
    rules_dir = cursor_dir / "rules"
    skills_dir = cursor_dir / "skills"
    rules_dir.mkdir(parents=True, exist_ok=True)
    skills_dir.mkdir(parents=True, exist_ok=True)
    rule = rules_dir / "software-factory.mdc"
    rule.write_text("""---
description: Software Factory Universal Governance
globs: *
---
- Strictly adhere to software-factory/constitution/CONSTITUTION.md
- Follow Spec-Driven Development (SDD)
""")
    write_mcp_config(target_project_dir, sf_dir)
    return True
