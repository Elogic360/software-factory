"""
Software Factory Manufacturing Line & Quality Gates (G0 - G15).
Enforces formal station inputs, outputs, validation gates, and evidence ledgers.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

GATES = [
    {"id": "G0", "name": "Product Accepted", "station": "Product Discovery", "artifact": "PRD.md"},
    {"id": "G1", "name": "Requirements Complete", "station": "Requirements", "artifact": "REQUIREMENTS.md"},
    {"id": "G2", "name": "Specification Approved", "station": "Specification", "artifact": "SYSTEM_SPEC.md"},
    {"id": "G3", "name": "Architecture Approved", "station": "Architecture", "artifact": "ARCHITECTURE.md"},
    {"id": "G4", "name": "Security Design Approved", "station": "Security Lab", "artifact": "THREAT_MODEL.md"},
    {"id": "G0.5", "name": "Documentation Completeness", "station": "Design / Station 06 Exit", "artifact": "DOCUMENTATION_SUITE.json"},
    {"id": "G5", "name": "Implementation Plan Approved", "station": "Planning", "artifact": "IMPLEMENTATION_PLAN.md"},
    {"id": "G6", "name": "Production Complete", "station": "Production Floor", "artifact": "WORK_ORDERS.json"},
    {"id": "G7", "name": "Unit Tests Passed", "station": "QA Lab", "artifact": "UNIT_TESTS.xml"},
    {"id": "G8", "name": "Integration Tests Passed", "station": "QA Lab", "artifact": "INTEGRATION_TESTS.json"},
    {"id": "G9", "name": "E2E Passed", "station": "QA Lab", "artifact": "E2E_REPORT.json"},
    {"id": "G10", "name": "Security Passed", "station": "Security Lab", "artifact": "SAST_REPORT.json"},
    {"id": "G11", "name": "Performance Passed", "station": "Performance Lab", "artifact": "LOAD_REPORT.json"},
    {"id": "G12", "name": "Staging Passed", "station": "Test Ground", "artifact": "STAGING_SIGNOFF.json"},
    {"id": "G13", "name": "Release Candidate Approved", "station": "Release Control", "artifact": "RC_VERDICT.json"},
    {"id": "G14", "name": "Production Deployment", "station": "DevOps / SRE", "artifact": "DEPLOYMENT_LOG.json"},
    {"id": "G15", "name": "Production Health Confirmed", "station": "Observability", "artifact": "HEALTH_TELEMETRY.json"}
]

class ManufacturingLine:
    """Enterprise Manufacturing Line orchestrator with G0-G15 quality gates."""

    def __init__(self, workspace_root: Optional[str] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent
        else:
            self.workspace_root = Path(workspace_root)
        self.evidence_dir = self.workspace_root / "evidence" / "manufacturing_runs"
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def list_gates(self) -> List[Dict[str, str]]:
        return GATES

    def evaluate_gate(self, gate_id: str, evidence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates a quality gate against provided evidence and validation criteria."""
        gate_meta = next((g for g in GATES if g["id"] == gate_id.upper()), None)
        if not gate_meta:
            raise ValueError(f"Unknown gate '{gate_id}'. Valid gates: {[g['id'] for g in GATES]}")

        required_passed = evidence_data.get("passed", False)
        errors = evidence_data.get("errors", [])
        evidence_files = evidence_data.get("evidence_files", [])

        status = "PASSED" if (required_passed and not errors) else "FAILED"

        result = {
            "gate_id": gate_meta["id"],
            "gate_name": gate_meta["name"],
            "station": gate_meta["station"],
            "required_artifact": gate_meta["artifact"],
            "status": status,
            "timestamp": time.time(),
            "evidence_files": evidence_files,
            "errors": errors,
            "operator_evidence": evidence_data.get("evidence_payload", {})
        }

        run_id = f"run-{int(time.time()*1000)}"
        run_file = self.evidence_dir / f"{gate_meta['id']}_{run_id}.json"
        with open(run_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return result

    def generate_work_orders(self, spec_name: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Decomposes a product specification into executable manufacturing work orders."""
        work_orders = []
        for idx, t in enumerate(tasks, 1):
            wo = {
                "work_order_id": f"WO-{idx:03d}",
                "spec": spec_name,
                "station": t.get("station", "Production Floor"),
                "assigned_agent": t.get("agent", "General Developer"),
                "task_title": t.get("title", f"Task {idx}"),
                "required_skills": t.get("skills", []),
                "required_mcp": t.get("mcp", []),
                "inputs": t.get("inputs", []),
                "acceptance_criteria": t.get("acceptance_criteria", []),
                "status": "QUEUED"
            }
            work_orders.append(wo)

        return {
            "product_spec": spec_name,
            "total_orders": len(work_orders),
            "created_at": time.time(),
            "work_orders": work_orders
        }
