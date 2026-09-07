import subprocess
import sys
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent

def test_skill_selector_query():
    script = SF_ROOT / "context-engine" / "skill_selector.py"
    res = subprocess.run([sys.executable, str(script), "--query", "fastapi backend database"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "backend-fastapi" in res.stdout

def test_skill_selector_list():
    script = SF_ROOT / "context-engine" / "skill_selector.py"
    res = subprocess.run([sys.executable, str(script), "--list"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "All registered skills" in res.stdout
