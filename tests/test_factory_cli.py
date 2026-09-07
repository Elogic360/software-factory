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

def test_factory_capabilities_and_skills_cli():
    res = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "capabilities", "list"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Software Factory Capabilities" in res.stdout

    res2 = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "skills", "list"], capture_output=True, text=True)
    assert res2.returncode == 0
    assert "Active Engineering Skills" in res2.stdout

def test_factory_architecture_and_spec_cli():
    res = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "architecture", "validate"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Architecture Validation" in res.stdout

    res2 = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "spec", "validate"], capture_output=True, text=True)
    assert res2.returncode == 0
    assert "Specification Validated" in res2.stdout

def test_factory_state_update_cli():
    res = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "update"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Synchronized" in res.stdout
    assert (SF_ROOT / "state" / "factory-state.yaml").exists()
