"""
Codex CLI Adapter — Configures AGENTS.md single source of truth for Codex.
"""
from pathlib import Path

def setup_codex(target_project_dir: Path, sf_dir: Path):
    agents_md = sf_dir / "AGENTS.md"
    target_agents = target_project_dir / "AGENTS.md"
    if agents_md.exists() and not target_agents.exists():
        target_agents.write_text(agents_md.read_text())
    return True
