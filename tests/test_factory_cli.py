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

def test_factory_browser_and_api_cli():
    res = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "browser", "status"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Browser Engineering Plane" in res.stdout
    assert "playwright-cli" in res.stdout

    res_api = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "api", "validate"], capture_output=True, text=True)
    assert res_api.returncode == 0
    assert "API Testing Plane" in res_api.stdout
    assert "Valid Structure: YES" in res_api.stdout

def test_factory_database_and_target_cli():
    res_db = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "database", "inspect-ddl"], capture_output=True, text=True)
    assert res_db.returncode == 0
    assert "Database Engineering Plane" in res_db.stdout
    assert "Parsed 2 tables" in res_db.stdout

    res_tgt = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "target", "dashboard"], capture_output=True, text=True)
    assert res_tgt.returncode == 0
    assert "Target-Driven Development Plane" in res_tgt.stdout

def test_factory_diagnose_and_verify_cli():
    res_diag = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "diagnose"], capture_output=True, text=True)
    assert res_diag.returncode == 0
    assert "Cross-Layer Diagnostic" in res_diag.stdout
    assert "Root Cause Layer:" in res_diag.stdout

    res_ver = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "verify"], capture_output=True, text=True)
    assert res_ver.returncode == 0
    assert "Full-Spectrum Verification Loop" in res_ver.stdout
    assert "Verification Verdict: VERIFIED" in res_ver.stdout

def test_factory_bundle_and_control_room_cli():
    res_bnd = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "bundle", "list"], capture_output=True, text=True)
    assert res_bnd.returncode == 0
    assert "Registered Capability Bundles (12)" in res_bnd.stdout

    res_ctrl = subprocess.run([sys.executable, str(SF_ROOT / "factory.py"), "control-room"], capture_output=True, text=True)
    assert res_ctrl.returncode == 0
    assert "SOFTWARE FACTORY CENTRAL CONTROL ROOM" in res_ctrl.stdout

