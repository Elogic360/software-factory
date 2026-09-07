import pytest
import shutil
from pathlib import Path
from core.target_engine import TargetEngine, TARGET_STATES
from core.cross_layer_debugger import CrossLayerDebugger
from core.bundle_router import BundleRouter
from core.architecture_state import ArchitectureStateManager

def test_target_lifecycle_and_state_machine(tmp_path):
    engine = TargetEngine(targets_dir=str(tmp_path))

    target = engine.create_target(
        target_id="TGT-TEST-1",
        title="Implement Order Book Widget",
        description="High-performance canvas order book",
        category="ui",
        acceptance_criteria=["Renders 50 levels", "Latency < 16ms"]
    )
    assert target["status"] == "PLANNED"
    assert target["category"] == "ui"

    # Forward sequential transitions: PLANNED -> PROPOSED -> IN_PROGRESS -> IMPLEMENTED -> TESTED
    t1 = engine.transition_target("TGT-TEST-1", "PROPOSED", note="Architecture approved")
    assert t1["status"] == "PROPOSED"

    t2 = engine.transition_target("TGT-TEST-1", "IN_PROGRESS", note="Coding started")
    assert t2["status"] == "IN_PROGRESS"

    t3 = engine.transition_target("TGT-TEST-1", "IMPLEMENTED", note="Code finished")
    assert t3["status"] == "IMPLEMENTED"

    t4 = engine.transition_target("TGT-TEST-1", "TESTED", note="Unit tests green")
    assert t4["status"] == "TESTED"

    # Rollback on gate failure
    t_roll = engine.transition_target("TGT-TEST-1", "IN_PROGRESS", note="A11y gate failed")
    assert t_roll["status"] == "IN_PROGRESS"

    # Resume: IN_PROGRESS -> IMPLEMENTED -> TESTED -> VERIFIED -> OBSERVED
    engine.transition_target("TGT-TEST-1", "IMPLEMENTED")
    engine.transition_target("TGT-TEST-1", "TESTED")
    engine.transition_target("TGT-TEST-1", "VERIFIED")
    final_t = engine.transition_target("TGT-TEST-1", "OBSERVED")
    assert final_t["status"] == "OBSERVED"

    # Invalid jump
    target2 = engine.create_target("TGT-TEST-2", "Another Target", "desc")
    with pytest.raises(ValueError):
        engine.transition_target("TGT-TEST-2", "OBSERVED")

    # Dashboard metrics
    dash = engine.generate_dashboard()
    assert dash["total_targets"] == 2
    assert dash["completed_observed"] == 1
    assert dash["progress_percentage"] == 50.0

def test_cross_layer_debugger_database_root(tmp_path):
    debugger = CrossLayerDebugger(evidence_dir=str(tmp_path))

    # Error originates in database (relation does not exist)
    incident = debugger.correlate_incident(
        incident_id="INC-001",
        browser_logs=[{"level": "error", "text": "POST /api/v1/orders 500 (Internal Server Error)"}],
        network_logs=[{"status": 500, "url": "/api/v1/orders", "method": "POST"}],
        backend_logs=[{"level": "error", "message": "UndefinedTable: relation 'orders' does not exist"}],
        db_logs=[{"level": "error", "error": "relation 'orders' does not exist"}]
    )
    assert incident["root_layer"] == "DATABASE_LAYER"
    assert "migration" in incident["remediation_action"].lower()
    assert "evidence_file" in incident

def test_cross_layer_debugger_backend_and_network_roots(tmp_path):
    debugger = CrossLayerDebugger(evidence_dir=str(tmp_path))

    # Backend unhandled exception without DB error
    inc_backend = debugger.correlate_incident(
        incident_id="INC-002",
        backend_logs=[{"level": "error", "message": "ZeroDivisionError: division by zero in fee_calculator.py:18"}]
    )
    assert inc_backend["root_layer"] == "BACKEND_SERVICE_LAYER"

    # API 404
    inc_api = debugger.correlate_incident(
        incident_id="INC-003",
        network_logs=[{"status": 404, "url": "/api/v1/missing_route", "method": "GET"}]
    )
    assert inc_api["root_layer"] == "API_CONTRACT_LAYER"

    # CORS
    inc_cors = debugger.correlate_incident(
        incident_id="INC-004",
        browser_logs=[{"level": "error", "text": "Access-Control-Allow-Origin header missing"}]
    )
    assert inc_cors["root_layer"] == "NETWORK_INFRASTRUCTURE_LAYER"

    # Frontend UI JS error
    inc_ui = debugger.correlate_incident(
        incident_id="INC-005",
        browser_logs=[{"level": "error", "text": "Uncaught TypeError: cannot read property of null"}]
    )
    assert inc_ui["root_layer"] == "FRONTEND_UI_LAYER"

def test_bundle_router():
    router = BundleRouter()
    bundles = router.list_bundles()
    assert len(bundles) == 12

    # Query routing
    browser_match = router.route_query("Test UI buttons and check responsive viewport")
    assert browser_match[0]["id"] == "browser-engineering"

    api_match = router.route_query("Validate OpenAPI swagger contract for REST endpoints")
    assert api_match[0]["id"] == "api-engineering"

    db_match = router.route_query("Generate database ERD and verify migration safety")
    assert db_match[0]["id"] == "database-engineering"

    debug_match = router.route_query("Debug full-stack crash across frontend and database")
    assert debug_match[0]["id"] == "cross-layer-debugging"

def test_architecture_state_manager(tmp_path):
    mgr = ArchitectureStateManager(state_path=str(tmp_path / "architecture-state.yaml"))
    state = mgr.create_default_architecture("TestSystem", archetype="python-fastapi")

    val = mgr.validate_architecture_state(state)
    assert val["valid"] is True
    assert val["boundary_count"] >= 3

    saved_path = mgr.save(state)
    assert saved_path.exists()

    loaded = mgr.load(saved_path)
    assert loaded["project"]["name"] == "TestSystem"

    # Scaffold compilation
    scaffold_dir = tmp_path / "scaffold"
    created = mgr.compile_scaffolding(state, scaffold_dir)
    assert len(created) >= 4
    assert (scaffold_dir / "core" / "__init__.py").exists()

    # Code compliance check
    compliance = mgr.verify_code_compliance(scaffold_dir, state)
    assert compliance["compliant"] is True
