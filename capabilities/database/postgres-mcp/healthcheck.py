"""
Healthcheck script for Postgres MCP Pro (crystaldba/postgres-mcp) capability.
Verifies restricted access mode enforcement and safety filters.
"""

import sys
import json
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from core.database_engine import DatabaseEngine


def run_healthcheck():
    checks = []
    errors = []

    try:
        engine = DatabaseEngine()
        checks.append("DatabaseEngine instantiated")

        # 1. Verify safe query permitted in restricted mode
        res_read = engine.validate_query_safety("SELECT id, name FROM users WHERE active = true;", access_mode="restricted")
        assert res_read["allowed"] is True
        checks.append("Safe SELECT allowed in restricted mode")

        # 2. Verify write command blocked in restricted mode
        res_write = engine.validate_query_safety("DELETE FROM users WHERE id = 10;", access_mode="restricted")
        assert res_write["allowed"] is False
        assert res_write["verdict"] == "BLOCKED"
        checks.append("Direct DELETE blocked in restricted mode")

        # 3. Verify chained destructive command blocked in restricted mode
        res_chain = engine.validate_query_safety("SELECT 1; COMMIT; DROP SCHEMA public CASCADE;", access_mode="restricted")
        assert res_chain["allowed"] is False
        assert res_chain["verdict"] == "BLOCKED"
        checks.append("Chained COMMIT; DROP SCHEMA CASCADE blocked in restricted mode")

        # 4. Verify unauthorized unrestricted mode blocked
        res_unauth = engine.validate_query_safety("ALTER TABLE users ADD COLUMN age INT;", access_mode="unrestricted")
        assert res_unauth["allowed"] is False
        assert res_unauth["verdict"] == "BLOCKED_UNAUTHORIZED"
        checks.append("Unrestricted mode without human confirmation blocked")

        # 5. Verify confirmed unrestricted permitted on disposable dev
        res_dev = engine.validate_query_safety("ALTER TABLE users ADD COLUMN age INT;", access_mode="unrestricted", is_disposable_dev=True)
        assert res_dev["allowed"] is True
        checks.append("Disposable dev instance permitted in unrestricted mode")

    except Exception as e:
        errors.append(str(e))

    status = "HEALTHY" if not errors else "DEGRADED"
    return {
        "capability": "postgres-mcp-pro",
        "status": status,
        "checks": checks,
        "errors": errors
    }


if __name__ == "__main__":
    res = run_healthcheck()
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["status"] == "HEALTHY" else 1)
