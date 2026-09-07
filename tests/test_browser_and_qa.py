import pytest
from core.browser_orchestrator import BrowserOrchestrator, RESPONSIVE_VIEWPORTS

def test_browser_backend_selection():
    orch = BrowserOrchestrator()
    c_mcp = orch.select_backend("console_debugging")
    assert c_mcp["backend"] == "chrome-devtools-mcp"

    a11y = orch.select_backend("accessibility")
    assert a11y["backend"] == "playwright-cli"

    explore = orch.select_backend("exploratory_qa")
    assert explore["backend"] == "browser-use"

    quick = orch.select_backend("quick_inspection")
    assert quick["backend"] == "antigravity-browser"

def test_console_log_classifier_clean():
    orch = BrowserOrchestrator()
    logs = [
        {"level": "info", "text": "App loaded"},
        {"level": "warning", "text": "Cache miss for asset"}
    ]
    res = orch.inspect_console_logs(logs)
    assert res["status"] == "PASSED"
    assert res["total_errors"] == 0
    assert len(res["warnings"]) == 1

def test_console_log_classifier_errors():
    orch = BrowserOrchestrator()
    logs = [
        {"level": "error", "text": "Uncaught TypeError: Cannot read properties of undefined"},
        {"level": "error", "text": "Access to fetch has been blocked by CORS policy"},
        {"level": "error", "text": "Hydration failed because the server-rendered HTML didn't match"},
        {"level": "error", "text": "WebSocket connection to 'wss://im/feed' failed: 401 Unauthorized"}
    ]
    res = orch.inspect_console_logs(logs)
    assert res["status"] == "FAILED"
    assert res["total_errors"] == 4
    assert len(res["react_errors"]) == 1
    assert len(res["network_cors_errors"]) == 1
    assert len(res["hydration_errors"]) == 1
    assert len(res["auth_errors"]) == 1 or len(res["websocket_errors"]) == 1

def test_network_traffic_inspector():
    orch = BrowserOrchestrator()
    requests = [
        {"url": "https://api.integralmarket.com/v1/health", "status": 200, "duration_ms": 45.0},
        {"url": "https://api.integralmarket.com/v1/slow", "status": 200, "duration_ms": 1250.0},
        {"url": "https://api.integralmarket.com/v1/orders", "status": 500, "duration_ms": 80.0, "response_payload": {"detail": "Internal Error"}}
    ]
    res = orch.inspect_network_traffic(requests)
    assert res["status"] == "FAILED"
    assert len(res["failed_requests"]) == 1
    assert len(res["slow_requests"]) == 1
    assert res["failed_requests"][0]["status"] == 500

def test_accessibility_audit():
    orch = BrowserOrchestrator()
    violations = [
        {"id": "color-contrast", "impact": "minor", "description": "Element has insufficient color contrast"},
        {"id": "button-name", "impact": "critical", "description": "Buttons must have discernible text"}
    ]
    res = orch.run_accessibility_audit("https://integralmarket.com", violations=violations)
    assert res["verdict"] == "FAILED"
    assert res["total_violations"] == 2
    assert res["critical_violations"] == 1
    assert "evidence_file" in res

    # Test clean audit
    clean_res = orch.run_accessibility_audit("https://integralmarket.com", violations=[])
    assert clean_res["verdict"] == "PASSED"
    assert clean_res["critical_violations"] == 0

def test_responsive_matrix():
    orch = BrowserOrchestrator()
    res = orch.evaluate_responsive_matrix("https://integralmarket.com")
    assert res["overall_status"] == "PASSED"
    assert res["viewports_tested"] == 5
    assert "mobile" in res["results"]
    assert "desktop" in res["results"]

def test_exploratory_qa():
    orch = BrowserOrchestrator()
    res = orch.run_exploratory_qa(goal="Audit trade terminal buttons", start_url="https://integralmarket.com/trade", steps_to_explore=3)
    assert res["verdict"] == "EXPLORATION_PASSED"
    assert res["steps_executed"] == 3
    assert res["broken_journeys_found"] == 0
