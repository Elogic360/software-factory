"""
GitHub Copilot Adapter — Configures .github/copilot-instructions.md.
"""
from pathlib import Path

def setup_copilot(target_project_dir: Path, sf_dir: Path):
    github_dir = target_project_dir / ".github"
    github_dir.mkdir(parents=True, exist_ok=True)
    instr = github_dir / "copilot-instructions.md"
    instr.write_text("""# GitHub Copilot Software Factory Instructions
Follow software-factory/constitution/CONSTITUTION.md guidelines.
Respect service boundaries and API versioning.
""")
    return True
