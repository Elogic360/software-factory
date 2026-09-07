"""
Healthcheck script for Google Chrome DevTools MCP capability.
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
        route = orch.select_backend("console_debugging")
        assert route["backend"] == "chrome-devtools-mcp"
        checks.append("Chrome DevTools routing verified")

        test_logs = [
            {"level": "error", "text": "Uncaught TypeError: Cannot read property 'map' of undefined at Orders.tsx:42"},
            {"level": "warn", "text": "Form field missing label"}
        ]
        res = orch.inspect_console_logs(test_logs)
        assert res["total_errors"] == 1
        assert len(res["react_errors"]) == 1
        checks.append("Console log classification & stacktrace extraction verified")

    except Exception as e:
        errors.append(str(e))

    status = "HEALTHY" if not errors else "DEGRADED"
    return {
        "capability": "chrome-devtools-mcp",
        "status": status,
        "checks": checks,
        "errors": errors
    }


if __name__ == "__main__":
    res = run_healthcheck()
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["status"] == "HEALTHY" else 1)
