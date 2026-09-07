"""
Healthcheck script for Spec Kit & Speckit Agent Skills capability.
"""

import sys
import json
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from core.spec_kit_adapter import SpecKitAdapter


def run_healthcheck():
    checks = []
    errors = []

    try:
        adapter = SpecKitAdapter()
        checks.append("SpecKitAdapter instantiated")

        # Test spec markdown parsing
        test_spec = """# Order Service
## Overview
Handles placement and execution of customer orders.
## Requirements
- Support market orders
- Support limit orders
## Constraints
- Max latency 50ms
"""
        sections = adapter.parse_markdown_sections(test_spec)
        assert "overview" in sections
        assert "requirements" in sections
        checks.append("Markdown section parsing operational")

        # Test task markdown parsing
        test_tasks = """
- [ ] TASK-1: Design database schema for orders
  - Foreign key to users
- [ ] TASK-2: Implement POST /api/v1/orders endpoint
  - Validate request payload
- [x] TASK-3: Add unit tests
"""
        tasks = adapter.parse_tasks(test_tasks)
        assert len(tasks) == 3
        assert tasks[0]["category"] == "database"
        assert tasks[1]["category"] == "api"
        checks.append("Task breakdown and category classification operational")

        # Test interrogation
        interrogation = adapter.interrogate_requirements(test_spec)
        assert "clarifications" in interrogation
        checks.append("Requirement interrogation (/grill-with-docs) operational")

    except Exception as e:
        errors.append(str(e))

    status = "HEALTHY" if not errors else "DEGRADED"
    return {
        "capability": "spec-kit",
        "status": status,
        "checks": checks,
        "errors": errors
    }


if __name__ == "__main__":
    res = run_healthcheck()
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["status"] == "HEALTHY" else 1)
