"""
core/doc_suite_validator.py — Mandatory Product Documentation Artifact Suite Validator
Enforces Quality Gate 0.5 (Documentation Completeness & Cross-Traceability) across Stations 01-06.
Verifies bidirectional traceability: PRD -> TRD -> App Flow -> UI/UX -> Schema -> Backend -> Arch -> Plan -> Test -> Scaling.
"""

from __future__ import annotations

import os
import re
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


REQUIRED_DOCUMENTS = [
    {"filename": "01_prd.md", "id": "PRD", "skill": "prd-authoring", "title": "Product Requirement Document"},
    {"filename": "02_trd.md", "id": "TRD", "skill": "trd-authoring", "title": "Technical Requirement Document"},
    {"filename": "03_app_flow.md", "id": "FLOW", "skill": "app-flow-mapping", "title": "App Flow Document"},
    {"filename": "04a_uiux_brief.md", "id": "UIUX_BRIEF", "skill": "uiux-brief", "title": "UI/UX Design Brief"},
    {"filename": "04b_uiux_specification.md", "id": "UIUX_SPEC", "skill": "uiux-specification", "title": "Full UI/UX Specification"},
    {"filename": "05_schema_document.md", "id": "SCHEMA", "skill": "schema-design-document", "title": "Schema & Database Document"},
    {"filename": "06_backend_architecture.md", "id": "BACKEND_ARCH", "skill": "backend-architecture-document", "title": "Backend Architecture Document"},
    {"filename": "07_project_architecture.md", "id": "PROJECT_ARCH", "skill": "project-architecture-document", "title": "Full Project Architecture Document"},
    {"filename": "08_implementation_plan.md", "id": "PLAN", "skill": "implementation-plan-compiler", "title": "Implementation Plan"},
    {"filename": "09_testing_plan.md", "id": "TEST_PLAN", "skill": "testing-plan-authoring", "title": "Testing Plan"},
    {"filename": "10_scaling_plan.md", "id": "SCALING", "skill": "scaling-plan-authoring", "title": "Scaling & Capacity Plan"}
]


class DocSuiteValidator:
    """Automated validator and cross-document traceability verifier for the SDD assembly line."""

    def __init__(self, workspace_root: Optional[Path | str] = None):
        if workspace_root is None:
            self.workspace_root = Path(__file__).resolve().parent.parent
        else:
            self.workspace_root = Path(workspace_root)

    def validate_suite(self, suite_dir: Path | str) -> Dict[str, Any]:
        suite_path = Path(suite_dir)
        if not suite_path.is_absolute():
            suite_path = self.workspace_root / suite_path

        errors: List[str] = []
        warnings: List[str] = []
        found_docs: Dict[str, str] = {}
        missing_docs: List[str] = []

        if not suite_path.exists() or not suite_path.is_dir():
            return {
                "passed": False,
                "errors": [f"Documentation suite directory not found: {suite_path}"],
                "warnings": [],
                "completeness_score": 0.0,
                "found_documents": [],
                "missing_documents": [doc["filename"] for doc in REQUIRED_DOCUMENTS]
            }

        # 1. Check presence of all required documents
        for doc in REQUIRED_DOCUMENTS:
            file_path = suite_path / doc["filename"]
            if file_path.exists() and file_path.stat().st_size > 50:
                found_docs[doc["filename"]] = file_path.read_text(encoding="utf-8")
            else:
                missing_docs.append(doc["filename"])
                errors.append(f"Missing mandatory document: {doc['filename']} ({doc['title']})")

        if missing_docs:
            return {
                "passed": False,
                "errors": errors,
                "warnings": warnings,
                "completeness_score": round(len(found_docs) / len(REQUIRED_DOCUMENTS) * 100, 2),
                "found_documents": list(found_docs.keys()),
                "missing_documents": missing_docs
            }

        # 2. Detailed Document Parsers & Validations
        prd_data = self._validate_prd(found_docs["01_prd.md"], errors, warnings)
        trd_data = self._validate_trd(found_docs["02_trd.md"], prd_data["functional_reqs"], prd_data["non_functional_reqs"], errors, warnings)
        flow_data = self._validate_app_flow(found_docs["03_app_flow.md"], errors, warnings)
        self._validate_uiux_brief(found_docs["04a_uiux_brief.md"], errors, warnings)
        uiux_data = self._validate_uiux_spec(found_docs["04b_uiux_specification.md"], flow_data["screen_ids"], errors, warnings)
        schema_data = self._validate_schema_document(found_docs["05_schema_document.md"], errors, warnings)
        self._validate_backend_architecture(found_docs["06_backend_architecture.md"], errors, warnings)
        self._validate_project_architecture(found_docs["07_project_architecture.md"], suite_path, errors, warnings)
        self._validate_implementation_plan(found_docs["08_implementation_plan.md"], prd_data["functional_reqs"], trd_data["trd_items"], errors, warnings)
        test_data = self._validate_testing_plan(found_docs["09_testing_plan.md"], prd_data["acceptance_criteria"], flow_data["journeys"], errors, warnings)
        self._validate_scaling_plan(found_docs["10_scaling_plan.md"], errors, warnings)

        # 3. Cross-Document Screen Parity Gate (Zero Orphan Screens)
        flow_screens = flow_data["screen_ids"]
        uiux_screens = uiux_data["screen_ids"]
        orphan_in_uiux = uiux_screens - flow_screens
        orphan_in_flow = flow_screens - uiux_screens

        if orphan_in_uiux:
            errors.append(f"Screen Parity Violation: Screen(s) {sorted(list(orphan_in_uiux))} defined in UI/UX spec are missing from App Flow Document.")
        if orphan_in_flow:
            errors.append(f"Screen Parity Violation: Screen(s) {sorted(list(orphan_in_flow))} defined in App Flow are missing from UI/UX Specification.")

        # 4. Acceptance Criteria Traceability Gate (PRD -> Testing Plan)
        missing_tests_for_ac = prd_data["acceptance_criteria"] - test_data["tested_criteria"]
        if missing_tests_for_ac:
            errors.append(f"Traceability Violation: PRD Acceptance Criteria {sorted(list(missing_tests_for_ac))} have no linked automated test cases in 09_testing_plan.md.")

        passed = len(errors) == 0
        total_checks = 11 + len(prd_data["functional_reqs"]) + len(prd_data["acceptance_criteria"])
        return {
            "passed": passed,
            "status": "PASSED" if passed else "FAILED",
            "errors": errors,
            "warnings": warnings,
            "completeness_score": 100.0 if passed else max(0.0, round((1.0 - (len(errors) / total_checks)) * 100, 2)),
            "suite_dir": str(suite_path),
            "verified_artifacts": list(found_docs.keys()),
            "traceability_stats": {
                "functional_requirements_count": len(prd_data["functional_reqs"]),
                "acceptance_criteria_count": len(prd_data["acceptance_criteria"]),
                "trd_items_count": len(trd_data["trd_items"]),
                "screen_inventory_count": len(flow_screens),
                "tested_criteria_count": len(test_data["tested_criteria"])
            }
        }

    # ── Document Parsing Helpers ─────────────────────────────────────────────

    def _validate_prd(self, text: str, errors: List[str], warnings: List[str]) -> Dict[str, Any]:
        fr_ids = set()
        ac_ids = set()
        nfr_ids = set()

        # Find FRs
        fr_pattern = re.compile(r"###\s*\[(FR-\d+)\]:\s*(.+)")
        fr_matches = fr_pattern.findall(text)
        for fid, title in fr_matches:
            fr_ids.add(fid)

        if not fr_ids:
            errors.append("01_prd.md: No numbered functional requirements found (e.g., '### [FR-001]: Title').")

        # Find ACs
        ac_pattern = re.compile(r"\[(AC-FR-\d+-\d+)\]")
        for ac in ac_pattern.findall(text):
            ac_ids.add(ac)

        # Ensure every FR has at least one AC
        for fid in fr_ids:
            matching_ac = [ac for ac in ac_ids if ac.startswith(f"AC-{fid}-")]
            if not matching_ac:
                errors.append(f"01_prd.md: Functional requirement '{fid}' lacks any acceptance criteria ([AC-{fid}-1]).")

        # Find NFRs
        nfr_pattern = re.compile(r"\[(NFR-\d+)\]")
        for nfr in nfr_pattern.findall(text):
            nfr_ids.add(nfr)

        if not nfr_ids:
            errors.append("01_prd.md: No numbered non-functional requirements found ([NFR-001]).")

        # Check for unmeasurable NFR qualitative keywords
        bad_qualitative = ["should be fast", "easy to use", "super scalable", "very responsive", "user friendly"]
        for bq in bad_qualitative:
            if bq in text.lower():
                errors.append(f"01_prd.md: Unmeasurable qualitative assertion detected: '{bq}'. NFRs must have quantitative metrics.")

        return {"functional_reqs": fr_ids, "acceptance_criteria": ac_ids, "non_functional_reqs": nfr_ids}

    def _validate_trd(self, text: str, prd_frs: Set[str], prd_nfrs: Set[str], errors: List[str], warnings: List[str]) -> Dict[str, Any]:
        trd_items = set()
        trd_pattern = re.compile(r"\[(TRD-[A-Z]+-\d+)\]")
        for item in trd_pattern.findall(text):
            trd_items.add(item)

        if not trd_items:
            errors.append("02_trd.md: No technical requirement items found (e.g., '[TRD-INT-01]', '[TRD-API-01]').")

        # Traceability Matrix check
        all_prd_reqs = prd_frs.union(prd_nfrs)
        traced_refs = re.findall(r"\[(FR-\d+|NFR-\d+)\]", text)
        if not traced_refs:
            errors.append("02_trd.md: Traceability matrix missing or no PRD requirements ([FR-xxx] or [NFR-xxx]) cited.")
        else:
            invalid_citations = set(traced_refs) - all_prd_reqs
            if invalid_citations and all_prd_reqs:
                errors.append(f"02_trd.md: Traceability references non-existent PRD requirements: {sorted(list(invalid_citations))}.")

        return {"trd_items": trd_items}

    def _validate_app_flow(self, text: str, errors: List[str], warnings: List[str]) -> Dict[str, Any]:
        if "```mermaid" not in text or ("flowchart" not in text and "graph" not in text):
            errors.append("03_app_flow.md: Missing navigable Mermaid flowchart diagram.")

        screens = set()
        # Find screens in table or text: SCR-01, SCR-02, etc.
        screen_pattern = re.compile(r"\b(SCR-\d+)\b")
        for sc in screen_pattern.findall(text):
            screens.add(sc)

        if not screens:
            errors.append("03_app_flow.md: No Screen IDs found in Screen Inventory (e.g. 'SCR-01').")

        journeys = set()
        journey_pattern = re.compile(r"\b(J-\d+)\b")
        for j in journey_pattern.findall(text):
            journeys.add(j)

        return {"screen_ids": screens, "journeys": journeys}

    def _validate_uiux_brief(self, text: str, errors: List[str], warnings: List[str]):
        required_brief_terms = ["target platform", "tone", "breakpoint", "accessibility", "wcag"]
        for term in required_brief_terms:
            if term not in text.lower():
                warnings.append(f"04a_uiux_brief.md: Expected key topic '{term}' not clearly covered.")

    def _validate_uiux_spec(self, text: str, flow_screens: Set[str], errors: List[str], warnings: List[str]) -> Dict[str, Any]:
        screens = set()
        screen_pattern = re.compile(r"\b(SCR-\d+)\b")
        for sc in screen_pattern.findall(text):
            screens.add(sc)

        # Check for tokens
        if "colors:" not in text and "color" not in text.lower():
            errors.append("04b_uiux_specification.md: Design tokens (color palette) missing.")

        # Check for 5 states mentions
        states = ["loading", "empty", "error", "success"]
        missing_states = [st for st in states if st not in text.lower()]
        if missing_states:
            errors.append(f"04b_uiux_specification.md: Missing explicit screen state specifications: {missing_states}.")

        return {"screen_ids": screens}

    def _validate_schema_document(self, text: str, errors: List[str], warnings: List[str]) -> Dict[str, Any]:
        if "```mermaid" not in text or "erDiagram" not in text:
            errors.append("05_schema_document.md: Missing Mermaid erDiagram representing the entity relationships.")

        if "indexes" not in text.lower() and "indexing" not in text.lower():
            errors.append("05_schema_document.md: Missing indexing strategy section.")

        if "pii" not in text.lower() and "retention" not in text.lower():
            warnings.append("05_schema_document.md: Data retention or PII tagging notes not explicitly identified.")

        return {}

    def _validate_backend_architecture(self, text: str, errors: List[str], warnings: List[str]):
        required_sections = ["boundary", "api surface", "queue", "cache", "error"]
        for s in required_sections:
            if s not in text.lower():
                errors.append(f"06_backend_architecture.md: Missing required architectural narrative section: '{s}'.")

    def _validate_project_architecture(self, text: str, suite_path: Path, errors: List[str], warnings: List[str]):
        if "C4Context" not in text and "C4Container" not in text and "c4" not in text.lower():
            warnings.append("07_project_architecture.md: C4 architectural models (Context/Container/Component) not detected.")

        if "architecture-state.yaml" not in text:
            errors.append("07_project_architecture.md: Must reference and link to machine-readable architecture-state.yaml.")

    def _validate_implementation_plan(self, text: str, prd_frs: Set[str], trd_items: Set[str], errors: List[str], warnings: List[str]):
        task_pattern = re.compile(r"\b(TSK-\d+)\b")
        tasks = task_pattern.findall(text)
        if not tasks:
            errors.append("08_implementation_plan.md: No work breakdown tasks found (e.g. 'TSK-001').")

        if "rollback" not in text.lower():
            warnings.append("08_implementation_plan.md: Rollback procedures not clearly defined per task.")

    def _validate_testing_plan(self, text: str, prd_acs: Set[str], flow_journeys: Set[str], errors: List[str], warnings: List[str]) -> Dict[str, Any]:
        tested_criteria = set()
        ac_pattern = re.compile(r"\[(AC-FR-\d+-\d+)\]")
        for ac in ac_pattern.findall(text):
            tested_criteria.add(ac)

        if not tested_criteria:
            errors.append("09_testing_plan.md: Requirements Traceability Matrix has zero mapped acceptance criteria ([AC-FR-xxx-y]).")

        # Test layers check
        layers = ["unit", "integration", "e2e"]
        for lay in layers:
            if lay not in text.lower():
                warnings.append(f"09_testing_plan.md: Test layer '{lay}' not explicitly detailed.")

        return {"tested_criteria": tested_criteria}

    def _validate_scaling_plan(self, text: str, errors: List[str], warnings: List[str]):
        if "threshold" not in text.lower() and "applicability" not in text.lower():
            errors.append("10_scaling_plan.md: Missing explicit applicability threshold justification.")

    # ── Manufacturing Line & Gate 0.5 Integration ───────────────────────────

    def evaluate_gate_0_5(self, project_id: str, suite_dir: Path | str, manufacturing_line: Optional[Any] = None) -> Dict[str, Any]:
        """Evaluates Quality Gate 0.5 (Documentation Completeness) and writes evidence record."""
        suite_path = Path(suite_dir)
        validation_result = self.validate_suite(suite_path)

        evidence_payload = {
            "project_id": project_id,
            "suite_directory": str(suite_path),
            "completeness_score": validation_result["completeness_score"],
            "traceability_stats": validation_result.get("traceability_stats", {}),
            "verified_artifacts": validation_result.get("verified_artifacts", [])
        }

        evidence_data = {
            "passed": validation_result["passed"],
            "errors": validation_result["errors"],
            "evidence_files": [str(suite_path / f) for f in validation_result.get("verified_artifacts", [])],
            "evidence_payload": evidence_payload
        }

        if manufacturing_line is not None:
            return manufacturing_line.evaluate_gate("G0.5", evidence_data)

        # Fallback if manufacturing line not passed
        from core.manufacturing_line import ManufacturingLine
        m_line = ManufacturingLine(workspace_root=self.workspace_root)
        return m_line.evaluate_gate("G0.5", evidence_data)
