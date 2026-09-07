"""
Software Factory Cross-Layer Debugging & Error Correlation Engine.
Correlates errors across the full stack:
UI Event -> Frontend Handler -> HTTP Request -> API Endpoint -> Backend Service -> Database Query.
Eliminates hallucinated fixes by locating the precise root cause layer.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

LAYER_PRIORITY = [
    "DATABASE_LAYER",
    "BACKEND_SERVICE_LAYER",
    "API_CONTRACT_LAYER",
    "NETWORK_INFRASTRUCTURE_LAYER",
    "FRONTEND_UI_LAYER"
]

class CrossLayerDebugger:
    """End-to-end full-stack log and telemetry correlation engine."""

    def __init__(self, evidence_dir: Optional[str] = None):
        if evidence_dir is None:
            self.evidence_dir = Path(__file__).resolve().parent.parent / "evidence" / "incidents"
        else:
            self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def correlate_incident(
        self,
        incident_id: str,
        browser_logs: Optional[List[Dict[str, Any]]] = None,
        network_logs: Optional[List[Dict[str, Any]]] = None,
        backend_logs: Optional[List[Dict[str, Any]]] = None,
        db_logs: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Correlates logs from all layers to deduce root cause and prescribe fix."""
        b_logs = browser_logs or []
        n_logs = network_logs or []
        bk_logs = backend_logs or []
        d_logs = db_logs or []

        root_layer = None
        root_cause_message = ""
        remediation_action = ""

        # 1. Inspect Database Layer
        db_errors = [l for l in d_logs if l.get("level") in ["error", "fatal", "ERROR", "FATAL"] or "error" in str(l).lower()]
        for de in db_errors:
            text = str(de.get("message", de.get("error", "")))
            if "relation" in text and "does not exist" in text:
                root_layer = "DATABASE_LAYER"
                root_cause_message = f"Missing database table or unapplied migration: {text}"
                remediation_action = "Run database migrations or schema synchronization before changing frontend/backend code."
                break
            elif "column" in text and "does not exist" in text:
                root_layer = "DATABASE_LAYER"
                root_cause_message = f"Schema drift: missing column in database: {text}"
                remediation_action = "Execute schema migration to add the missing column."
                break
            elif "violates not-null" in text or "violates foreign key" in text:
                root_layer = "DATABASE_LAYER"
                root_cause_message = f"Database constraint violation: {text}"
                remediation_action = "Verify payload integrity against database constraints."
                break
            elif "connection refused" in text or "could not connect" in text:
                root_layer = "DATABASE_LAYER"
                root_cause_message = f"Database service unreachable: {text}"
                remediation_action = "Check database container / service health and connection string."
                break

        # 2. Inspect Backend Service Layer (if root not found)
        if not root_layer:
            bk_errors = [l for l in bk_logs if l.get("level") in ["error", "fatal", "ERROR", "FATAL"] or "traceback" in str(l).lower()]
            if bk_errors:
                first_err = bk_errors[0]
                msg = str(first_err.get("message", first_err.get("error", "")))
                root_layer = "BACKEND_SERVICE_LAYER"
                root_cause_message = f"Backend unhandled exception or crash: {msg}"
                remediation_action = "Inspect backend stacktrace and add proper error handling/validation in service layer."

        # 3. Inspect Network / API Contract Layer
        if not root_layer:
            failed_reqs = [r for r in n_logs if r.get("status", 200) >= 400]
            for fr in failed_reqs:
                st = fr.get("status", 400)
                url = fr.get("url", "")
                if st == 404:
                    root_layer = "API_CONTRACT_LAYER"
                    root_cause_message = f"Endpoint not found (404) at '{url}'."
                    remediation_action = "Check route registration in API router or check frontend request URL."
                    break
                elif st in [400, 422]:
                    root_layer = "API_CONTRACT_LAYER"
                    root_cause_message = f"Request validation failed ({st}) for '{url}'."
                    remediation_action = "Align frontend request payload with OpenAPI contract schema."
                    break
                elif st == 500:
                    root_layer = "BACKEND_SERVICE_LAYER"
                    root_cause_message = f"Internal server error (500) for '{url}'."
                    remediation_action = "Inspect backend application logs for unhandled exception."
                    break
                elif st in [401, 403]:
                    root_layer = "API_CONTRACT_LAYER"
                    root_cause_message = f"Authentication/Authorization failure ({st}) for '{url}'."
                    remediation_action = "Verify token injection and user role permissions."
                    break

        # 4. Inspect Network Infrastructure Layer (CORS, Connection Errors)
        if not root_layer:
            cors_errors = [l for l in b_logs if "cors" in str(l.get("text", "")).lower() or "access-control-allow-origin" in str(l.get("text", "")).lower()]
            if cors_errors:
                root_layer = "NETWORK_INFRASTRUCTURE_LAYER"
                root_cause_message = "Cross-Origin Resource Sharing (CORS) policy blocking requests."
                remediation_action = "Configure CORS middleware on the API backend to allow frontend origin."

        # 5. Inspect Frontend UI Layer
        if not root_layer:
            ui_errors = [l for l in b_logs if l.get("level") in ["error", "fatal", "ERROR", "FATAL"]]
            if ui_errors:
                first_ui = ui_errors[0]
                text = str(first_ui.get("text", first_ui.get("message", "")))
                root_layer = "FRONTEND_UI_LAYER"
                root_cause_message = f"Frontend JavaScript runtime exception: {text}"
                remediation_action = "Fix null safety or component lifecycle in frontend code."

        # Default fallback
        if not root_layer:
            root_layer = "UNKNOWN"
            root_cause_message = "No clear errors detected across layers."
            remediation_action = "Enable verbose debug logging and re-run scenario."

        incident_report = {
            "incident_id": incident_id,
            "root_layer": root_layer,
            "root_cause_message": root_cause_message,
            "remediation_action": remediation_action,
            "evidence_counts": {
                "browser_logs": len(b_logs),
                "network_logs": len(n_logs),
                "backend_logs": len(bk_logs),
                "db_logs": len(d_logs)
            },
            "timestamp": time.time()
        }

        # Persist incident evidence
        artifact_path = self.evidence_dir / f"{incident_id}.json"
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(incident_report, f, indent=2)

        incident_report["evidence_file"] = str(artifact_path)
        return incident_report
