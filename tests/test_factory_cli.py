import subprocess
import sys
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent

def test_factory_doctor():
    res = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "doctor"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "FACTORY HEALTHY" in res.stdout

def test_factory_list():
    res = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "list"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Software Factory Capabilities" in res.stdout

def test_factory_search():
    res = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "search", "quant"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "gs-quant" in res.stdout or "ziplime" in res.stdout

def test_factory_audit():
    res = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "audit"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Hardened" in res.stdout
