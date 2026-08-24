#!/usr/bin/env python3
"""Preload and validate Software Factory MCP/skills/memory runtime readiness."""

from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _extract_env_placeholders(env_map: dict[str, str]) -> list[str]:
    names: list[str] = []
    pattern = re.compile(r"^\$\{([A-Z0-9_]+)\}$")
    for value in env_map.values():
        matched = pattern.match(value.strip())
        if matched:
            names.append(matched.group(1))
    return names


def _parse_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        values[key] = value
    return values


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    sf_root = repo_root / "software-factory"
    integrations = sf_root / "integrations" / "mcp-servers.json"
    local_mcp = repo_root / ".mcp.json"
    skills_root = sf_root / "skills"
    memory_root = sf_root / "memory"
    specify_memory = repo_root / ".specify" / "memory"
    dotenv_candidates = (
        repo_root / ".env",
        repo_root / ".env.production",
        repo_root / "app" / ".env",
        repo_root / "app" / ".env.production",
        sf_root / ".env",
    )

    dotenv_values: dict[str, str] = {}
    for env_file in dotenv_candidates:
        dotenv_values.update(_parse_dotenv(env_file))

    catalog_servers = _read_json(integrations).get("mcpServers", {})
    local_servers = _read_json(local_mcp).get("mcpServers", {}) if local_mcp.exists() else {}

    merged_servers: dict[str, Any] = {}
    for name in sorted(set(catalog_servers) | set(local_servers)):
        # Canonical catalog wins for overlapping entries; local-only entries are preserved.
        merged_servers[name] = catalog_servers.get(name, local_servers.get(name))

    previous = {"mcpServers": local_servers}
    current = {"mcpServers": merged_servers}
    if previous != current:
        _write_json(local_mcp, current)

    for directory in (
        memory_root,
        memory_root / "decisions",
        memory_root / "patterns",
        memory_root / "api-evolution",
        specify_memory,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    skill_files = sorted(skills_root.rglob("SKILL.md"))
    skill_entries: list[dict[str, str]] = []
    for skill_path in skill_files:
        relative = skill_path.relative_to(repo_root)
        skill_path.read_text(encoding="utf-8")
        skill_entries.append(
            {
                "path": str(relative),
                "skill": skill_path.parent.name,
            }
        )

    command_presence = {
        command: shutil.which(command) is not None
        for command in ("git", "python3", "node", "npx", "uvx", "gh", "curl")
    }

    mcp_status: dict[str, Any] = {}
    blocking_issues: list[str] = []

    for name, config in merged_servers.items():
        command = config.get("command", "")
        priority = config.get("priority", "medium")
        env_map = config.get("env", {}) or {}
        required_env_vars = _extract_env_placeholders(env_map)
        missing_env_vars = []
        for var in required_env_vars:
            runtime_value = os.environ.get(var)
            configured_value = dotenv_values.get(var, "")
            has_value = bool(runtime_value) or (
                bool(configured_value) and not configured_value.startswith("${")
            )
            if not has_value:
                missing_env_vars.append(var)
        command_found = shutil.which(command) is not None

        if not command_found:
            blocking_issues.append(f"{name}: command '{command}' not found")
        if priority == "critical" and missing_env_vars:
            blocking_issues.append(f"{name}: missing env vars {', '.join(missing_env_vars)}")

        mcp_status[name] = {
            "command": command,
            "priority": priority,
            "command_found": command_found,
            "required_env_vars": required_env_vars,
            "missing_env_vars": missing_env_vars,
        }

    status = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mcp": {
            "catalog_count": len(catalog_servers),
            "active_count": len(merged_servers),
            "servers": mcp_status,
        },
        "skills": {
            "count": len(skill_entries),
            "entries": skill_entries,
        },
        "memory": {
            "paths": [
                str(memory_root.relative_to(repo_root)),
                str((memory_root / "decisions").relative_to(repo_root)),
                str((memory_root / "patterns").relative_to(repo_root)),
                str((memory_root / "api-evolution").relative_to(repo_root)),
                str(specify_memory.relative_to(repo_root)),
            ],
        },
        "toolchain": command_presence,
        "ready": len(blocking_issues) == 0,
        "blocking_issues": blocking_issues,
    }

    status_path = sf_root / "memory" / "patterns" / "factory_runtime_preload_status.json"
    _write_json(status_path, status)

    print(f"[factory-preload] MCP servers active: {len(merged_servers)}")
    print(f"[factory-preload] Skills preloaded: {len(skill_entries)}")
    print(f"[factory-preload] Status file: {status_path}")

    if blocking_issues:
        print("[factory-preload] Blocking issues:")
        for issue in blocking_issues:
            print(f"  - {issue}")
        return 2

    print("[factory-preload] Ready: all critical MCP/tool requirements satisfied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
