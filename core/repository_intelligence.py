"""
core/repository_intelligence.py — Repository Intelligence & Capability Scoring Engine
Evaluates candidate tools and libraries using a multi-factor quality scoring model.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

class RepositoryIntelligence:
    @staticmethod
    def calculate_score(
        maintenance: float = 85.0,
        security: float = 95.0,
        license_score: float = 100.0,
        test_quality: float = 90.0,
        documentation: float = 90.0,
        integration_value: float = 95.0,
        agent_usefulness: float = 95.0,
        performance: float = 90.0,
        community: float = 85.0,
        deductions: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates normalized weighted capability score (0-100) and letter grade (A-D, REJECTED).
        """
        weights = {
            "maintenance": 0.15,
            "security": 0.15,
            "license": 0.10,
            "test_quality": 0.10,
            "documentation": 0.10,
            "integration_value": 0.15,
            "agent_usefulness": 0.15,
            "performance": 0.05,
            "community": 0.05,
        }

        weighted_sum = (
            maintenance * weights["maintenance"] +
            security * weights["security"] +
            license_score * weights["license"] +
            test_quality * weights["test_quality"] +
            documentation * weights["documentation"] +
            integration_value * weights["integration_value"] +
            agent_usefulness * weights["agent_usefulness"] +
            performance * weights["performance"] +
            community * weights["community"]
        )

        final_score = max(0.0, min(100.0, weighted_sum - deductions))

        if final_score >= 90.0:
            grade = "A"
            recommendation = "ADOPT_CORE"
        elif final_score >= 80.0:
            grade = "B"
            recommendation = "ADOPT_SPECIALIZED"
        elif final_score >= 70.0:
            grade = "C"
            recommendation = "EXPERIMENT_QUARANTINE"
        elif final_score >= 60.0:
            grade = "D"
            recommendation = "REFERENCE_ONLY"
        else:
            grade = "REJECTED"
            recommendation = "REJECT"

        return {
            "score": round(final_score, 1),
            "grade": grade,
            "recommendation": recommendation,
            "breakdown": {
                "maintenance": maintenance,
                "security": security,
                "license": license_score,
                "test_quality": test_quality,
                "documentation": documentation,
                "integration_value": integration_value,
                "agent_usefulness": agent_usefulness,
                "performance": performance,
                "community": community,
                "deductions": deductions
            }
        }
