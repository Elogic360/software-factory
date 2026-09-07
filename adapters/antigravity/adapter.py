"""
Antigravity Agent Adapter — Configures discovery, progressive skill disclosure,
rules loading, and memory persistence for the Antigravity pair programmer.
"""
import os
from pathlib import Path

def setup_antigravity(target_project_dir: Path, sf_dir: Path):
    target_agents = target_project_dir / ".agents"
    target_skills = target_agents / "skills"
    target_rules = target_agents / "rules"
    target_skills.mkdir(parents=True, exist_ok=True)
    target_rules.mkdir(parents=True, exist_ok=True)

    # Symlink skills
    sf_skills = sf_dir / "skills"
    if sf_skills.exists():
        for skill in sf_skills.iterdir():
            if skill.is_dir():
                link = target_skills / skill.name
                if not link.exists():
                    try:
                        link.symlink_to(skill, target_is_directory=True)
                    except Exception:
                        pass

    # Write rule
    rule_file = target_rules / "software-factory.md"
    rule_file.write_text("""# Antigravity Software Factory Governance
- Adhere strictly to the Engineering Constitution.
- Use `python3 software-factory/context-engine/skill_selector.py` for task routing.
- Validate changes incrementally with automated tests.
""")
    return True
