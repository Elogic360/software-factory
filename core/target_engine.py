"""
Software Factory Target-Driven Development (TDD) Engine.
Manages Target lifecycle state machine (PLANNED -> PROPOSED -> IN_PROGRESS ->
IMPLEMENTED -> TESTED -> VERIFIED -> OBSERVED) and real-time target metrics dashboard.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

TARGET_STATES = [
    "PLANNED",
    "PROPOSED",
    "IN_PROGRESS",
    "IMPLEMENTED",
    "TESTED",
    "VERIFIED",
    "OBSERVED"
]

VALID_CATEGORIES = ["ui", "api", "database", "performance", "security", "integration", "general"]

class TargetEngine:
    """Orchestrates Target-Driven Development workflows and state machine enforcement."""

    def __init__(self, targets_dir: Optional[str] = None):
        if targets_dir is None:
            self.targets_dir = Path(__file__).resolve().parent.parent / "targets"
        else:
            self.targets_dir = Path(targets_dir)
        self.targets_dir.mkdir(parents=True, exist_ok=True)

    def _get_target_file(self, target_id: str) -> Path:
        return self.targets_dir / f"{target_id}.yaml"

    def create_target(
        self,
        target_id: str,
        title: str,
        description: str,
        category: str = "general",
        acceptance_criteria: Optional[List[str]] = None,
        owner: str = "Antigravity"
    ) -> Dict[str, Any]:
        """Registers a new goal target in PLANNED state."""
        target_file = self._get_target_file(target_id)
        if target_file.exists():
            raise ValueError(f"Target '{target_id}' already exists.")

        cat = category.lower() if category.lower() in VALID_CATEGORIES else "general"
        target_data = {
            "id": target_id,
            "title": title,
            "description": description,
            "category": cat,
            "status": "PLANNED",
            "owner": owner,
            "acceptance_criteria": acceptance_criteria or [],
            "evidence_artifacts": [],
            "created_at": time.time(),
            "updated_at": time.time(),
            "history": [
                {
                    "from_status": None,
                    "to_status": "PLANNED",
                    "timestamp": time.time(),
                    "note": "Target created."
                }
            ]
        }

        with open(target_file, "w", encoding="utf-8") as f:
            yaml.dump(target_data, f, default_flow_style=False, sort_keys=False)

        return target_data

    def get_target(self, target_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves target by ID."""
        target_file = self._get_target_file(target_id)
        if not target_file.exists():
            return None
        with open(target_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def list_targets(
        self,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Lists all registered targets with optional filtering."""
        results = []
        for file in self.targets_dir.glob("*.yaml"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if not data or not isinstance(data, dict):
                        continue
                    if category and data.get("category") != category.lower():
                        continue
                    if status and data.get("status") != status.upper():
                        continue
                    results.append(data)
            except Exception:
                continue
        results.sort(key=lambda t: t.get("created_at", 0))
        return results

    def validate_transition(self, current_status: str, next_status: str) -> bool:
        """Enforces valid state machine transitions."""
        if current_status not in TARGET_STATES or next_status not in TARGET_STATES:
            return False

        current_idx = TARGET_STATES.index(current_status)
        next_idx = TARGET_STATES.index(next_status)

        # Forward progression by 1 step
        if next_idx == current_idx + 1:
            return True

        # Rollback to IN_PROGRESS on verification or testing failure
        if next_status in ["IN_PROGRESS", "PROPOSED"] and current_idx > TARGET_STATES.index(next_status):
            return True

        return False

    def transition_target(
        self,
        target_id: str,
        next_status: str,
        note: str = "",
        evidence_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Transitions target to next state and records evidence."""
        target = self.get_target(target_id)
        if not target:
            raise ValueError(f"Target '{target_id}' not found.")

        current_status = target.get("status", "PLANNED")
        next_status = next_status.upper()

        if not self.validate_transition(current_status, next_status):
            raise ValueError(
                f"Invalid transition from '{current_status}' to '{next_status}'. "
                f"State progression must be sequential or roll back to IN_PROGRESS."
            )

        target["status"] = next_status
        target["updated_at"] = time.time()
        if evidence_files:
            target.setdefault("evidence_artifacts", []).extend(evidence_files)

        target.setdefault("history", []).append({
            "from_status": current_status,
            "to_status": next_status,
            "timestamp": time.time(),
            "note": note,
            "evidence": evidence_files or []
        })

        target_file = self._get_target_file(target_id)
        with open(target_file, "w", encoding="utf-8") as f:
            yaml.dump(target, f, default_flow_style=False, sort_keys=False)

        return target

    def generate_dashboard(self) -> Dict[str, Any]:
        """Calculates real-time health and progress metrics across all targets."""
        all_targets = self.list_targets()
        counts_by_status = {state: 0 for state in TARGET_STATES}
        counts_by_category = {c: 0 for c in VALID_CATEGORIES}

        for t in all_targets:
            s = t.get("status", "PLANNED")
            if s in counts_by_status:
                counts_by_status[s] += 1
            cat = t.get("category", "general")
            if cat in counts_by_category:
                counts_by_category[cat] += 1

        total = len(all_targets)
        completed = counts_by_status["OBSERVED"]
        progress_pct = (completed / total * 100.0) if total > 0 else 0.0

        return {
            "total_targets": total,
            "completed_observed": completed,
            "progress_percentage": round(progress_pct, 2),
            "by_status": counts_by_status,
            "by_category": counts_by_category,
            "in_progress": [t["id"] for t in all_targets if t.get("status") == "IN_PROGRESS"],
            "timestamp": time.time()
        }
