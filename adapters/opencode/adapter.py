"""
OpenCode Adapter — Configures .opencode configuration and OpenWolf memory.
"""
from pathlib import Path

def setup_opencode(target_project_dir: Path, sf_dir: Path):
    opencode_dir = target_project_dir / ".opencode"
    opencode_dir.mkdir(parents=True, exist_ok=True)
    return True
