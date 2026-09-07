"""
Claude Code Agent Adapter — Configures marketplace, ecc@ecc, gstack, and CLAUDE.md.
"""
import subprocess
from pathlib import Path

def setup_claude(target_project_dir: Path, sf_dir: Path):
    claude_md = sf_dir / "CLAUDE.md"
    target_claude = target_project_dir / "CLAUDE.md"
    if claude_md.exists() and not target_claude.exists():
        target_claude.write_text(claude_md.read_text())
    return True
