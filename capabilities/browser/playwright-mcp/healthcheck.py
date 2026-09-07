"""
Healthcheck script for Microsoft Playwright MCP capability.
"""

import sys
import json
import shutil
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from core.browser_orchestrator import BrowserOrchestrator


def run_healthcheck():
    checks = []
    errors = []

    node_bin = shutil.which("node")
    npx_bin = shutil.which("npx")
    if node_bin:
        checks.append(f"Node runtime located at {node_bin}")
    else:
        errors.append("Node.js runtime not found in PATH")

    if npx_bin:
        checks.append(f"npx package runner located at {npx_bin}")
    else:
        errors.append("npx runner not found in PATH")

    try:
        orch = BrowserOrchestrator()
        route = orch.select_backend("e2e_testing")
        assert "playwright" in route["backend"]
        checks.append("Playwright backend routing verified")

        res = orch.run_accessibility_audit("http://localhost:3000/orders", violations=[])
        assert res["verdict"] == "PASSED"
        checks.append("Accessibility audit runner verified")

    except Exception as e:
        errors.append(str(e))

    status = "HEALTHY" if not errors else "DEGRADED"
    return {
        "capability": "playwright-mcp",
        "status": status,
        "checks": checks,
        "errors": errors
    }


if __name__ == "__main__":
    res = run_healthcheck()
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["status"] == "HEALTHY" else 1)
