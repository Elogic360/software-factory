"""
Software Factory API Testing Plane & Contract Verification Engine.
Enforces contract-first API development, OpenAPI 3.x schema validation,
runtime drift detection, and UI-to-API interaction tracing.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

class APITestingEngine:
    """Automated API contract testing, schema validation, and drift analysis."""

    def __init__(self, evidence_dir: Optional[str] = None):
        if evidence_dir is None:
            self.evidence_dir = Path(__file__).resolve().parent.parent / "evidence" / "api"
        else:
            self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def load_spec(self, spec_source: Any) -> Dict[str, Any]:
        """Loads an OpenAPI specification from file path, JSON string, or dict."""
        if isinstance(spec_source, dict):
            return spec_source
        if isinstance(spec_source, (str, Path)):
            p = Path(spec_source)
            if p.exists() and p.is_file():
                content = p.read_text(encoding="utf-8")
                try:
                    return json.loads(content)
                except Exception:
                    return yaml.safe_load(content)
            else:
                # Try parsing as raw JSON string
                try:
                    return json.loads(str(spec_source))
                except Exception:
                    return yaml.safe_load(str(spec_source))
        return {}

    def validate_spec_structure(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Validates fundamental structural requirements of an OpenAPI 3.x specification."""
        errors = []
        if not isinstance(spec, dict):
            return {"valid": False, "errors": ["Specification root must be an object."]}

        if "openapi" not in spec and "swagger" not in spec:
            errors.append("Missing 'openapi' or 'swagger' version declaration.")

        if "info" not in spec or not isinstance(spec.get("info"), dict):
            errors.append("Missing or invalid 'info' metadata object.")
        else:
            if "title" not in spec["info"]:
                errors.append("Missing 'info.title'.")
            if "version" not in spec["info"]:
                errors.append("Missing 'info.version'.")

        if "paths" not in spec or not isinstance(spec.get("paths"), dict):
            errors.append("Missing or invalid 'paths' object.")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "title": spec.get("info", {}).get("title", "Unknown API"),
            "version": spec.get("info", {}).get("version", "0.0.0"),
            "total_paths": len(spec.get("paths", {}))
        }

    def generate_contract_test_suite(self, spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compiles contract test cases for every endpoint, method, and expected status."""
        test_cases = []
        paths = spec.get("paths", {})

        for path, methods in paths.items():
            if not isinstance(methods, dict):
                continue
            for method, operation in methods.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch", "options", "head"]:
                    continue
                op_id = operation.get("operationId", f"{method.lower()}_{path.replace('/', '_')}")
                responses = operation.get("responses", {})

                for status_code, resp_def in responses.items():
                    test_cases.append({
                        "test_id": f"test_{op_id}_{status_code}",
                        "operation_id": op_id,
                        "path": path,
                        "method": method.upper(),
                        "expected_status": int(status_code) if status_code.isdigit() else status_code,
                        "description": resp_def.get("description", ""),
                        "parameters": operation.get("parameters", []),
                        "request_body_schema": operation.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {}),
                        "response_schema": resp_def.get("content", {}).get("application/json", {}).get("schema", {})
                    })

        return test_cases

    def verify_response_against_contract(
        self,
        path: str,
        method: str,
        status_code: int,
        response_data: Any,
        spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validates a live or simulated HTTP response against the OpenAPI contract."""
        paths = spec.get("paths", {})
        method_lower = method.lower()

        # Find matching path template (handling path variables like /items/{id})
        matched_path = None
        for p in paths:
            if p == path:
                matched_path = p
                break
        if not matched_path:
            # Simple path variable matching
            p_parts = [seg for seg in path.strip("/").split("/") if seg]
            for candidate in paths:
                c_parts = [seg for seg in candidate.strip("/").split("/") if seg]
                if len(p_parts) == len(c_parts):
                    match = True
                    for pp, cp in zip(p_parts, c_parts):
                        if cp.startswith("{") and cp.endswith("}"):
                            continue
                        if pp != cp:
                            match = False
                            break
                    if match:
                        matched_path = candidate
                        break

        if not matched_path:
            return {
                "verdict": "FAILED",
                "reason": f"Path '{path}' not found in OpenAPI specification."
            }

        operation = paths[matched_path].get(method_lower)
        if not operation:
            return {
                "verdict": "FAILED",
                "reason": f"Method '{method.upper()}' not defined for path '{matched_path}'."
            }

        responses = operation.get("responses", {})
        status_str = str(status_code)
        if status_str not in responses and "default" not in responses:
            return {
                "verdict": "FAILED",
                "reason": f"Status code '{status_code}' not defined for '{method.upper()} {matched_path}'."
            }

        expected_resp = responses.get(status_str) or responses.get("default")
        schema = expected_resp.get("content", {}).get("application/json", {}).get("schema")

        mismatches = []
        if schema and isinstance(response_data, dict):
            expected_props = schema.get("properties", {})
            required_props = schema.get("required", [])

            for req in required_props:
                if req not in response_data:
                    mismatches.append(f"Missing required response property: '{req}'.")

            for prop, val in response_data.items():
                if prop in expected_props:
                    expected_type = expected_props[prop].get("type")
                    if expected_type == "string" and not isinstance(val, str):
                        mismatches.append(f"Field '{prop}' expected string, got {type(val).__name__}.")
                    elif expected_type == "integer" and not isinstance(val, int):
                        mismatches.append(f"Field '{prop}' expected integer, got {type(val).__name__}.")
                    elif expected_type == "boolean" and not isinstance(val, bool):
                        mismatches.append(f"Field '{prop}' expected boolean, got {type(val).__name__}.")
                    elif expected_type == "array" and not isinstance(val, list):
                        mismatches.append(f"Field '{prop}' expected array, got {type(val).__name__}.")
                    elif expected_type == "object" and not isinstance(val, dict):
                        mismatches.append(f"Field '{prop}' expected object, got {type(val).__name__}.")

        verdict = "PASSED" if not mismatches else "FAILED"
        return {
            "verdict": verdict,
            "path": matched_path,
            "method": method.upper(),
            "status_code": status_code,
            "schema_mismatches": mismatches
        }

    def detect_contract_drift(self, traffic_logs: List[Dict[str, Any]], spec: Dict[str, Any]) -> Dict[str, Any]:
        """Compares recorded network traffic or mock calls against OpenAPI spec to catch drift."""
        undocumented_endpoints = []
        undocumented_statuses = []
        schema_failures = []

        for log in traffic_logs:
            path = log.get("path", "")
            method = log.get("method", "GET")
            status = log.get("status", 200)
            res_body = log.get("body", {})

            result = self.verify_response_against_contract(path, method, status, res_body, spec)
            if result["verdict"] == "FAILED":
                reason = result.get("reason", "")
                if "Path" in reason:
                    undocumented_endpoints.append(f"{method} {path}")
                elif "Status code" in reason:
                    undocumented_statuses.append(f"{method} {path} -> {status}")
                elif result.get("schema_mismatches"):
                    schema_failures.append({
                        "endpoint": f"{method} {path}",
                        "mismatches": result["schema_mismatches"]
                    })

        drift_detected = bool(undocumented_endpoints or undocumented_statuses or schema_failures)
        report = {
            "drift_detected": drift_detected,
            "total_inspected": len(traffic_logs),
            "undocumented_endpoints": list(set(undocumented_endpoints)),
            "undocumented_statuses": list(set(undocumented_statuses)),
            "schema_failures": schema_failures,
            "timestamp": time.time()
        }

        artifact_path = self.evidence_dir / f"contract_drift_{int(time.time()*1000)}.json"
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        report["evidence_file"] = str(artifact_path)
        return report

    def trace_ui_to_api(self, trace_event: Dict[str, Any], spec: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Traces and validates a single UI interaction to its resulting API call."""
        ui_element = trace_event.get("ui_element", "unknown_trigger")
        endpoint = trace_event.get("endpoint", "")
        method = trace_event.get("method", "GET")
        status = trace_event.get("status", 200)
        latency_ms = trace_event.get("latency_ms", 0.0)
        body = trace_event.get("response_body", {})

        trace_result = {
            "trace_id": f"trace_{int(time.time()*1000)}",
            "ui_element": ui_element,
            "api_endpoint": endpoint,
            "method": method,
            "status": status,
            "latency_ms": latency_ms,
            "latency_acceptable": latency_ms < 500.0,
            "contract_valid": True
        }

        if spec:
            check = self.verify_response_against_contract(endpoint, method, status, body, spec)
            trace_result["contract_valid"] = check["verdict"] == "PASSED"
            trace_result["contract_details"] = check

        return trace_result
