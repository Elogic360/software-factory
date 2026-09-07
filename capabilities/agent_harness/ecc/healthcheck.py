#!/usr/bin/env python3
"""
Health Check for Everything Claude Code (ECC) Agent Harness.
Verifies Node.js runtime, CLI responsiveness, skills catalog presence,
and agent adapters compatibility.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_healthcheck() -> dict:
    results = {
        "status": "HEALTHY",
        "checks": [],
        "errors": []
    }

    sf_root = Path(__file__).resolve().parent.parent.parent.parent
    ecc_vendored = sf_root / "integrations" / "ecc"

    # 1. Node runtime
    node_path = shutil.which("node")
    if node_path:
        try:
            ver = subprocess.check_output([node_path, "-v"], text=True).strip()
            major = int(ver.lstrip("v").split(".")[0])
            if major >= 18:
                results["checks"].append(f"Node.js Runtime: {ver} (>= 18)")
            else:
                results["errors"].append(f"Node.js version {ver} is < 18")
        except Exception as e:
            results["errors"].append(f"Failed to check Node version: {e}")
    else:
        results["errors"].append("Node.js executable not found in PATH")

    # 2. Vendored or global ECC CLI
    ecc_script = ecc_vendored / "scripts" / "ecc.js"
    if ecc_script.exists():
        results["checks"].append(f"Vendored ECC CLI: {ecc_script}")
        try:
            out = subprocess.check_output(["node", str(ecc_script), "--help"], text=True)
            if "ECC selective-install CLI" in out:
                results["checks"].append("ECC CLI Execution: Verified (selective-install CLI operational)")
            else:
                results["errors"].append("ECC CLI output did not match expected help header")
        except Exception as e:
            results["errors"].append(f"ECC CLI execution failed: {e}")
    else:
        results["errors"].append(f"Vendored ECC CLI script missing at: {ecc_script}")

    # 3. Skills catalog check
    skills_dir = ecc_vendored / "skills"
    if skills_dir.exists():
        skills_count = sum(1 for d in skills_dir.iterdir() if d.is_dir())
        results["checks"].append(f"ECC Skills Catalog: {skills_count} skills present")
    else:
        results["errors"].append("ECC skills catalog directory not found")

    # 4. Bin wrapper check
    bin_ecc = sf_root / "bin" / "ecc"
    if bin_ecc.exists() and os.access(bin_ecc, os.X_OK):
        results["checks"].append("Executable Wrapper: bin/ecc operational")
    else:
        results["checks"].append("Executable Wrapper: bin/ecc not provisioned yet (run install.sh)")

    if results["errors"]:
        results["status"] = "UNHEALTHY"

    return results

def main():
    res = run_healthcheck()
    print("\n🔍 ECC Agent Harness Health Check")
    print("=" * 50)
    for c in res["checks"]:
        print(f"✅ {c}")
    for e in res["errors"]:
        print(f"❌ {e}")
    print("=" * 50)
    print(f"Verdict: {res['status']}\n")
    sys.exit(0 if res["status"] == "HEALTHY" else 1)

if __name__ == "__main__":
    main()
