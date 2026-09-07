import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.production_readiness import ProductionReadinessScorer

def test_production_readiness_approved():
    scores = {
        "requirements": 100.0,
        "architecture": 95.0,
        "implementation": 98.0,
        "tests": 96.0,
        "security": 92.0,
        "performance": 90.0,
        "observability": 100.0,
        "backup_recovery": 90.0,
        "deployment": 100.0,
        "rollback": 90.0
    }
    res = ProductionReadinessScorer.evaluate(scores)
    assert res["status"] == "APPROVED"
    assert res["threshold_passed"] is True
    assert res["overall_score"] >= 90.0

def test_production_readiness_rejected():
    scores = {"security": 50.0, "tests": 40.0}
    res = ProductionReadinessScorer.evaluate(scores)
    assert res["status"] in ["REJECTED", "CONDITIONAL_APPROVAL"]
