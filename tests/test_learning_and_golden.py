import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.learning_engine import LearningEngine
from core.scheduler import FactoryScheduler
from core.golden_projects import GoldenProjectRunner
from core.observability_sre import ObservabilitySRE

def test_learning_engine():
    eng = LearningEngine()
    failures = [{"category": "Network Timeout", "topic": "DB connection reset"}]
    insights = eng.mine_failures(failures)
    assert len(insights) == 1
    assert "Network Timeout" in insights[0]["category"]

def test_scheduler_jobs():
    jobs = FactoryScheduler.list_jobs("daily")
    assert len(jobs) >= 2

def test_golden_projects():
    runner = GoldenProjectRunner()
    res = runner.run_archetype_simulation("rest_api")
    assert res["manufacturing_status"] == "MANUFACTURED_AND_VERIFIED"
    assert res["gates_passed"] == 10

def test_observability_sre():
    sre = ObservabilitySRE()
    health = sre.get_health_telemetry("TestService", p95_latency_ms=30.0, error_rate_pct=0.0)
    assert health["status"] == "HEALTHY"
    rb = sre.execute_rollback("REL-1.0", "REL-0.9")
    assert rb["status"] == "ROLLBACK_SUCCESSFUL"
