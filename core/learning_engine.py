"""
Software Factory Learning Engine.
Mines failures, captures recurring architecture patterns, detects component candidates,
and formulates non-breaking self-improvement proposals.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

class LearningEngine:
    """Enterprise self-learning engine."""

    def __init__(self, workspace_root: Optional[str] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent
        else:
            self.workspace_root = Path(workspace_root)
        self.proposals_dir = self.workspace_root / "reports" / "learning_proposals"
        self.proposals_dir.mkdir(parents=True, exist_ok=True)

    def mine_failures(self, failure_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Groups failure logs by root cause category and recommends defensive measures."""
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for r in failure_records:
            cat = r.get("category", "General Error")
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(r)

        insights = []
        for cat, items in grouped.items():
            insights.append({
                "category": cat,
                "occurrence_count": len(items),
                "sample_topic": items[0].get("topic", "N/A"),
                "recommended_remediation": f"Synthesize new automated quality gate or lint rule for '{cat}'"
            })
        return insights

    def mine_reusable_components(self, project_builds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifies software blocks built repeatedly across projects as candidate raw materials."""
        feature_counts: Dict[str, int] = {}
        for b in project_builds:
            for feat in b.get("implemented_features", []):
                feature_counts[feat] = feature_counts.get(feat, 0) + 1

        candidates = []
        for feat, count in feature_counts.items():
            if count >= 2:
                candidates.append({
                    "component_name": feat,
                    "reuse_frequency": count,
                    "action": "PROMOTE_TO_RAW_MATERIAL",
                    "status": "CANDIDATE_READY_FOR_REVIEW"
                })
        return candidates

    def create_improvement_proposal(self, title: str, category: str, rationale: str, evidence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates formal self-improvement proposal requiring human or CI sign-off."""
        proposal = {
            "proposal_id": f"PROP-{int(time.time()*1000)}",
            "title": title,
            "category": category,
            "rationale": rationale,
            "created_at": time.time(),
            "evidence": evidence_data,
            "status": "PROPOSED"
        }
        prop_file = self.proposals_dir / f"{proposal['proposal_id']}.json"
        with open(prop_file, "w", encoding="utf-8") as f:
            json.dump(proposal, f, indent=2)
        return proposal
