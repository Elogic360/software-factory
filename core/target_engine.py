"""
Software Factory Target-Driven Development (TDD) Engine.
Manages 12-state Target lifecycle state machine:
PLANNED -> DESIGNED -> READY -> IMPLEMENTING -> IMPLEMENTED -> TESTING -> VERIFIED -> STAGED -> RELEASED -> DEPLOYED -> OBSERVED,
plus the FAILED -> DIAGNOSING -> FIXING -> RETESTING branch and real-time coverage dashboard.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

PRIMARY_TARGET_STATES = [
    "PLANNED",
    "DESIGNED",
    "READY",
    "IMPLEMENTING",
    "IMPLEMENTED",
    "TESTING",
    "VERIFIED",
    "STAGED",
    "RELEASED",
    "DEPLOYED",
    "OBSERVED"
]

FAILURE_BRANCH_STATES = [
    "FAILED",
    "DIAGNOSING",
    "FIXING",
    "RETESTING"
]

# Aliases for backwards compatibility with earlier prompts
STATE_ALIASES = {
    "PROPOSED": "DESIGNED",
    "IN_PROGRESS": "IMPLEMENTING",
    "TESTED": "VERIFIED"
}

ALL_TARGET_STATES = PRIMARY_TARGET_STATES + FAILURE_BRANCH_STATES + list(STATE_ALIASES.keys())
TARGET_STATES = ALL_TARGET_STATES
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
                    "note": "Target created in PLANNED state."
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
        """Enforces valid state machine transitions across primary chain and failure branch."""
        curr = current_status.upper()
        nxt = next_status.upper()

        if curr not in ALL_TARGET_STATES or nxt not in ALL_TARGET_STATES:
            return False

        # Direct transition to FAILED branch from any testing/gate state
        if nxt == "FAILED":
            return True
        if curr == "FAILED" and nxt == "DIAGNOSING":
            return True
        if curr == "DIAGNOSING" and nxt == "FIXING":
            return True
        if curr == "FIXING" and nxt == "RETESTING":
            return True
        if curr == "RETESTING" and nxt in ["TESTING", "VERIFIED", "IMPLEMENTED", "FAILED"]:
            return True

        # Normalized comparison in primary pipeline
        curr_norm = STATE_ALIASES.get(curr, curr)
        nxt_norm = STATE_ALIASES.get(nxt, nxt)

        if curr_norm in PRIMARY_TARGET_STATES and nxt_norm in PRIMARY_TARGET_STATES:
            curr_idx = PRIMARY_TARGET_STATES.index(curr_norm)
            nxt_idx = PRIMARY_TARGET_STATES.index(nxt_norm)
            # Step forward
            if nxt_idx == curr_idx + 1:
                return True
            # Rollback to IMPLEMENTING or READY on test failure
            if nxt_idx < curr_idx and nxt_norm in ["IMPLEMENTING", "READY", "DESIGNED"]:
                return True

        # Allow alias-to-alias direct transition (e.g. IN_PROGRESS -> IMPLEMENTED)
        if curr in ["IN_PROGRESS", "IMPLEMENTING"] and nxt == "IMPLEMENTED":
            return True
        if curr == "IMPLEMENTED" and nxt in ["TESTED", "TESTING"]:
            return True
        if curr in ["TESTED", "TESTING"] and nxt == "VERIFIED":
            return True
        if curr == "VERIFIED" and nxt in ["STAGED", "OBSERVED"]:
            return True
        if curr in ["PLANNED", "DESIGNED", "PROPOSED"] and nxt in ["PROPOSED", "DESIGNED", "READY", "IN_PROGRESS", "IMPLEMENTING"]:
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
                f"State progression must be sequential or follow failure recovery branch."
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
        """Calculates real-time health, coverage, and progress metrics across all targets."""
        all_targets = self.list_targets()
        counts_by_status = {state: 0 for state in PRIMARY_TARGET_STATES + FAILURE_BRANCH_STATES}

        for t in all_targets:
            s = t.get("status", "PLANNED")
            s_norm = STATE_ALIASES.get(s, s)
            if s_norm in counts_by_status:
                counts_by_status[s_norm] += 1

        total = len(all_targets)
        completed = counts_by_status.get("OBSERVED", 0)
        progress_pct = (completed / total * 100.0) if total > 0 else 0.0

        return {
            "total_targets": total,
            "completed_observed": completed,
            "progress_percentage": round(progress_pct, 2),
            "by_status": counts_by_status,
            "in_progress": [t["id"] for t in all_targets if t.get("status") in ["IN_PROGRESS", "IMPLEMENTING"]],
            "in_failure_recovery": [t["id"] for t in all_targets if t.get("status") in FAILURE_BRANCH_STATES],
            "timestamp": time.time()
        }
