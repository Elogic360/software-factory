"""
Software Factory Production Readiness Scorer.
Evaluates 10 core dimensions before release candidate authorization.
"""

from typing import Dict, Any

DIMENSION_WEIGHTS = {
    "requirements": 0.10,
    "architecture": 0.10,
    "implementation": 0.15,
    "tests": 0.15,
    "security": 0.15,
    "performance": 0.10,
    "observability": 0.10,
    "backup_recovery": 0.05,
    "deployment": 0.05,
    "rollback": 0.05
}

class ProductionReadinessScorer:
    """Calculates enterprise production readiness score and approval verdict."""

    @staticmethod
    def evaluate(dimension_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates weighted composite score.
        Scores must be provided as percentages (0 - 100).
        """
        normalized_scores = {}
        weighted_sum = 0.0

        for dim, weight in DIMENSION_WEIGHTS.items():
            score = dimension_scores.get(dim, 100.0)
            score = max(0.0, min(100.0, float(score)))
            normalized_scores[dim] = round(score, 1)
            weighted_sum += (score * weight)

        overall_score = round(weighted_sum, 1)
        # Approval threshold: Overall >= 90.0 and no critical dimension below 80.0
        min_critical = min(
            normalized_scores["requirements"],
            normalized_scores["implementation"],
            normalized_scores["tests"],
            normalized_scores["security"]
        )

        if overall_score >= 90.0 and min_critical >= 80.0:
            status = "APPROVED"
        elif overall_score >= 75.0:
            status = "CONDITIONAL_APPROVAL"
        else:
            status = "REJECTED"

        return {
            "overall_score": overall_score,
            "status": status,
            "dimension_scores": normalized_scores,
            "threshold_passed": status == "APPROVED"
        }
