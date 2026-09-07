import json
import pytest
import sys
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from raw_materials.auth.auth_core import create_access_token, verify_token, check_permission
from raw_materials.user_management.user_service import UserService
from raw_materials.admin_panel.admin_service import AdminService
from core.database_engine import DatabaseEngine


def test_auth_core_jwt_and_rbac():
    token = create_access_token({"sub": "user_123", "role": "trader"}, expires_delta_seconds=300)
    assert isinstance(token, str)
    assert len(token) > 20

    payload = verify_token(token)
    assert payload is not None
    assert payload.get("sub") == "user_123"

    # Permission check
    assert check_permission(["admin"], "operator") is True
    assert check_permission(["trader"], "trader") is True
    assert check_permission(["viewer"], "trader") is False

def test_user_management_service():
    svc = UserService()
    user = svc.register_user(email="alice@integralmarket.com", full_name="Alice Smith", roles=["trader"])
    assert user["id"].startswith("usr_")
    assert user["email"] == "alice@integralmarket.com"
    assert user["status"] == "ACTIVE"

    # Duplicate registration error
    with pytest.raises(ValueError):
        svc.register_user(email="alice@integralmarket.com", full_name="Alice Duplicate")

    # Profile update
    updated = svc.update_profile(user["id"], full_name="Alice Senior Trader")
    assert updated["full_name"] == "Alice Senior Trader"

    # Status transition
    suspended = svc.set_status(user["id"], "SUSPENDED")
    assert suspended["status"] == "SUSPENDED"

def test_admin_service_and_audit():
    admin = AdminService()
    event = admin.record_audit_event(
        actor_id="usr_admin1",
        action="UPDATE_USER_ROLES",
        resource="User",
        resource_id="usr_alice",
        details={"new_role": "admin"}
    )
    assert event["log_id"].startswith("aud_")
    assert event["action"] == "UPDATE_USER_ROLES"

    metrics = admin.get_system_metrics(total_users=100, active_users=85)
    assert metrics["total_users"] == 100
    assert metrics["total_audit_events"] == 1

    # Impersonation guard
    assert admin.can_impersonate(actor_roles=["superadmin"], target_roles=["admin"]) is True
    assert admin.can_impersonate(actor_roles=["admin"], target_roles=["user"]) is True
    assert admin.can_impersonate(actor_roles=["admin"], target_roles=["superadmin"]) is False

def test_raw_materials_schema_and_ui_primitives():
    # Database DDL
    ddl_file = SF_ROOT / "raw-materials" / "db-patterns" / "schema_patterns.sql"
    assert ddl_file.exists()
    db_engine = DatabaseEngine()
    schema = db_engine.parse_sql_ddl(ddl_file.read_text(encoding="utf-8"))
    assert "users" in schema["tables"]
    assert "roles" in schema["tables"]
    assert "audit_logs" in schema["tables"]

    # UI Primitives
    ui_file = SF_ROOT / "raw-materials" / "ui-ux" / "ui_primitives.json"
    assert ui_file.exists()
    ui_data = json.loads(ui_file.read_text(encoding="utf-8"))
    assert "primitives" in ui_data
    assert len(ui_data["primitives"]) >= 5
