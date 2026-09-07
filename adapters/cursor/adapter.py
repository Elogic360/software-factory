"""
Cursor IDE Adapter — Configures .cursor/rules and skills directory.
"""
from pathlib import Path

def setup_cursor(target_project_dir: Path, sf_dir: Path):
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
    return True
