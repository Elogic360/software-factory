import subprocess
import sys
from pathlib import Path

# Add factory root to sys.path
SF_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from capabilities.agent_harness.ecc.healthcheck import run_healthcheck

def test_ecc_healthcheck():
    res = run_healthcheck()
    assert res["status"] == "HEALTHY"
    assert len(res["errors"]) == 0
    assert any("ECC CLI Execution" in c for c in res["checks"])
    assert any("ECC Skills Catalog" in c for c in res["checks"])

def test_ecc_cli_help():
    ecc_script = SF_ROOT / "integrations" / "ecc" / "scripts" / "ecc.js"
    proc = subprocess.run(["node", str(ecc_script), "--help"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "ECC selective-install CLI" in proc.stdout

def test_ecc_catalog_profiles():
    ecc_script = SF_ROOT / "integrations" / "ecc" / "scripts" / "ecc.js"
    proc = subprocess.run(["node", str(ecc_script), "catalog", "profiles"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "profiles" in proc.stdout.lower() or "developer" in proc.stdout.lower() or len(proc.stdout) > 0
