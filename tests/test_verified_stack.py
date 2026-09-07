"""
Test suite for Verified Capability Stack across Lifecycle Stages 0-6.
Verifies Spec Kit, Constitution Guard, Official Draw.io, Postgres MCP Pro governance,
Postman MCP contract generation, Playwright & Chrome DevTools routing, Antigravity browser,
Multi-source Radar, and Agent Skills Open Standard.
"""

import pytest
import sys
from pathlib import Path
import yaml

SF_ROOT = Path(__file__).resolve().parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from core.spec_kit_adapter import SpecKitAdapter
from core.constitution_guard import ConstitutionGuard
from core.architecture_engine import ArchitectureEngine
from core.database_engine import DatabaseEngine
from core.api_testing_engine import APITestingEngine
from core.browser_orchestrator import BrowserOrchestrator
from core.antigravity_browser_adapter import AntigravityBrowserAdapter
from core.radar_aggregator import MultiSourceRadarAggregator
from core.agent_skills_validator import AgentSkillsValidator
from core.target_engine import TargetEngine


def test_speckit_adapter_and_interrogation(tmp_path):
    adapter = SpecKitAdapter(workspace_root=str(tmp_path))
    target_engine = TargetEngine(targets_dir=str(tmp_path / "targets"))

    spec_md = """# Order Matching Engine
## Overview
Ultra low-latency matching engine for trading pairs.
## Requirements
- Support Limit and Market orders
- FIFO execution priority
## Security
- Authenticate all orders with JWT and user identity
"""

    tasks_md = """
- [ ] TASK-1: Design database schema for orderbook
- [ ] TASK-2: Implement POST /api/v1/orders endpoint
- [x] TASK-3: Add unit tests
"""

    # Interrogation
    interrogation = adapter.interrogate_requirements(spec_md)
    assert "clarifications" in interrogation
    assert interrogation["total_questions"] > 0

    # Compile to targets
    targets = adapter.compile_spec_to_targets(spec_md, tasks_md, target_engine=target_engine)
    assert len(targets) == 3
    assert any(t["category"] == "database" for t in targets)
    assert any(t["category"] == "api" for t in targets)

    # Compile to C4 architecture
    c4 = adapter.compile_spec_to_c4_architecture(spec_md, "plan")
    assert c4["system_name"] == "Order Matching Engine"
    assert len(c4["c4_levels"]["containers"]) >= 3


def test_constitution_guard_and_destructive_blocker():
    guard = ConstitutionGuard()

    # Destructive commands blocked
    b1 = guard.verify_command_safety("rm -rf /")
    assert b1["allowed"] is False
    assert b1["verdict"] == "BLOCKED"

    b2 = guard.verify_command_safety("git push origin main --force")
    assert b2["allowed"] is False

    b3 = guard.verify_command_safety("psql -c 'DROP SCHEMA public CASCADE;'")
    assert b3["allowed"] is False

    # Safe command permitted
    s1 = guard.verify_command_safety("pytest tests/ -v")
    assert s1["allowed"] is True

    # TDD Gate
    tdd_fail = guard.evaluate_tdd_gate(modified_impl_files=["services/order_service.py"], test_files=[])
    assert tdd_fail["status"] == "BLOCKED"

    tdd_pass = guard.evaluate_tdd_gate(
        modified_impl_files=["services/order_service.py"],
        test_files=["tests/test_order_service.py"],
        test_run_passed=True
    )
    assert tdd_pass["status"] == "PASSED"


def test_drawio_layout_validation_and_conversion():
    arch = ArchitectureEngine()

    c4_stub = {
        "product": "TradeEngine",
        "c2_containers": [
            {"name": "Web UI", "tech": "React", "description": "Front"},
            {"name": "API", "tech": "FastAPI", "description": "Gateway"}
        ]
    }
    xml_out = arch.generate_drawio_architecture(c4_stub)
    val = arch.validate_diagram_layout(xml_out)
    assert val["valid"] is True
    assert val["verdict"] == "APPROVED"

    mermaid_sample = """graph TD
UI --> API
API --> DB
"""
    converted = arch.convert_mermaid_to_drawio_xml(mermaid_sample)
    assert "<mxGraphModel" in converted
    assert "DB" in converted


def test_postgres_pro_access_mode_governance():
    db = DatabaseEngine()

    # Safe query in restricted mode
    q1 = db.validate_query_safety("SELECT * FROM accounts WHERE id = '1';", access_mode="restricted")
    assert q1["allowed"] is True

    # Destructive commands blocked in restricted mode
    q2 = db.validate_query_safety("DROP TABLE accounts;", access_mode="restricted")
    assert q2["allowed"] is False

    # Chained bypass blocked in restricted mode
    q3 = db.validate_query_safety("SELECT 1; COMMIT; DROP SCHEMA public CASCADE;", access_mode="restricted")
    assert q3["allowed"] is False

    # Unrestricted without human confirmation blocked
    q4 = db.validate_query_safety("CREATE TABLE audit_log (id INT);", access_mode="unrestricted")
    assert q4["allowed"] is False
    assert q4["verdict"] == "BLOCKED_UNAUTHORIZED"

    # Unrestricted with disposable dev flag permitted
    q5 = db.validate_query_safety("CREATE TABLE audit_log (id INT);", access_mode="unrestricted", is_disposable_dev=True)
    assert q5["allowed"] is True


def test_api_testing_engine_contract_generation():
    api = APITestingEngine()

    sample_spec = {
        "openapi": "3.0.0",
        "paths": {
            "/api/v1/orders": {
                "post": {
                    "operationId": "create_order",
                    "summary": "Create a new trade order",
                    "responses": {"201": {"description": "Created"}, "400": {"description": "Bad Request"}}
                }
            }
        }
    }

    test_cases = api.generate_contract_tests_from_spec(sample_spec)
    assert len(test_cases) == 2
    assert test_cases[0]["test_name"] == "test_create_order_201"
    assert test_cases[1]["expected_status"] == 400

    cfg_minimal = api.get_postman_mcp_config("minimal")
    assert cfg_minimal["toolset"] == "minimal"
    assert cfg_minimal["token_budget_impact"] == "low"


def test_browser_plane_backends_and_antigravity_adapter():
    orch = BrowserOrchestrator()

    # Routing distinction
    drive_route = orch.select_backend("e2e_testing")
    assert "playwright" in drive_route["backend"]

    debug_route = orch.select_backend("console_debugging")
    assert "chrome-devtools" in debug_route["backend"]

    # Antigravity native browser adapter
    ag = AntigravityBrowserAdapter(session_id="test-ag-session")
    nav = ag.navigate("http://localhost:8000/api/v1/health")
    assert nav["url"] == "http://localhost:8000/api/v1/health"

    logs = [
        {"level": "error", "text": "ReferenceError: x is not defined", "line": 15},
        {"level": "info", "text": "Initialized"}
    ]
    errors = ag.harvest_console_errors(logs)
    assert len(errors) == 1
    assert errors[0]["message"] == "ReferenceError: x is not defined"

    elem = ag.inspect_element("#submit-order-btn")
    assert elem["found"] is True
    assert elem["attributes"]["role"] == "button"


def test_radar_aggregator_multi_source():
    radar = MultiSourceRadarAggregator()
    scan = radar.scan_ecosystem_sample()
    assert scan["scanned_sources"] == 4
    assert scan["total_candidates_reconciled"] > 0
    assert any("@playwright/mcp" in r["canonical_name"] for r in scan["verified_candidates"])


def test_agent_skills_open_standard_validator():
    validator = AgentSkillsValidator()

    # Test open standard skill frontmatter
    open_std_skill = """---
name: order-routing-skill
description: Routes orders to optimal execution venues
---
# Order Routing Skill
Guidance for multi-venue smart order routing.
"""
    parsed = validator.parse_frontmatter(open_std_skill)
    assert parsed["has_frontmatter"] is True
    assert parsed["frontmatter"]["name"] == "order-routing-skill"

    # Test migration of legacy skill
    legacy_skill = """# SKILL: Execution Router
**Activation triggers:** route order, venue selection
## Guidelines
...
"""
    migrated = validator.generate_open_standard_frontmatter(legacy_skill)
    parsed_migrated = validator.parse_frontmatter(migrated)
    assert parsed_migrated["has_frontmatter"] is True
    assert parsed_migrated["frontmatter"]["name"] == "Execution Router"
