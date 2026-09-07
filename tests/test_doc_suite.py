"""
tests/test_doc_suite.py — Unit & Integration Test Suite for the Mandatory Product Documentation Suite.
Verifies templates, skills, DocSuiteValidator, Quality Gate 0.5, and SpecCompiler integration.
"""

import os
import shutil
import tempfile
from pathlib import Path
import pytest
import sys
import yaml
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from core.doc_suite_validator import DocSuiteValidator, REQUIRED_DOCUMENTS
from core.manufacturing_line import ManufacturingLine, GATES
from core.spec_compiler import SpecCompiler


def test_templates_exist_and_valid():
    """Verify all 11 canonical templates exist with valid markdown structure."""
    templates_dir = REPO_ROOT / ".factory" / "specifications" / "templates"
    assert templates_dir.exists() and templates_dir.is_dir()

    expected_templates = [
        "01_prd.template.md",
        "02_trd.template.md",
        "03_app_flow.template.md",
        "04a_uiux_brief.template.md",
        "04b_uiux_specification.template.md",
        "05_schema_document.template.md",
        "06_backend_architecture.template.md",
        "07_project_architecture.template.md",
        "08_implementation_plan.template.md",
        "09_testing_plan.template.md",
        "10_scaling_plan.template.md"
    ]

    for tmpl in expected_templates:
        p = templates_dir / tmpl
        assert p.exists(), f"Template {tmpl} does not exist"
        content = p.read_text(encoding="utf-8")
        assert len(content) > 300, f"Template {tmpl} is unexpectedly short"
        assert "# " in content, f"Template {tmpl} has no H1 header"


def test_skills_exist_and_frontmatter():
    """Verify all 11 dedicated skills exist with valid YAML frontmatter."""
    skills_dir = REPO_ROOT / "skills"
    expected_skills = [
        "prd-authoring",
        "trd-authoring",
        "app-flow-mapping",
        "uiux-brief",
        "uiux-specification",
        "schema-design-document",
        "backend-architecture-document",
        "project-architecture-document",
        "implementation-plan-compiler",
        "testing-plan-authoring",
        "scaling-plan-authoring"
    ]

    for sname in expected_skills:
        skill_file = skills_dir / sname / "SKILL.md"
        assert skill_file.exists(), f"Skill file {skill_file} does not exist"
        text = skill_file.read_text(encoding="utf-8")
        assert text.startswith("---"), f"Skill {sname} missing frontmatter opening"
        parts = text.split("---", 2)
        assert len(parts) >= 3, f"Skill {sname} invalid frontmatter format"
        metadata = yaml.safe_load(parts[1])
        assert metadata.get("name") == sname, f"Skill {sname} name mismatch in frontmatter: {metadata.get('name')}"
        assert "description" in metadata and len(metadata["description"]) > 10


def test_golden_sample_suite_passes_validator():
    """Verify that the golden sample project passes DocSuiteValidator with 100% score."""
    golden_dir = REPO_ROOT / ".factory" / "specifications" / "golden-sample"
    assert golden_dir.exists()

    validator = DocSuiteValidator(workspace_root=REPO_ROOT)
    res = validator.validate_suite(golden_dir)

    assert res["passed"] is True
    assert res["status"] == "PASSED"
    assert res["completeness_score"] == 100.0
    assert len(res["errors"]) == 0
    assert len(res["verified_artifacts"]) == len(REQUIRED_DOCUMENTS)
    stats = res["traceability_stats"]
    assert stats["functional_requirements_count"] >= 3
    assert stats["acceptance_criteria_count"] >= 6
    assert stats["trd_items_count"] >= 6
    assert stats["screen_inventory_count"] >= 4
    assert stats["tested_criteria_count"] >= 6


def test_validator_detects_missing_documents():
    """Verify validator reports errors when required documents are missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        # Only copy 2 documents
        shutil.copy(REPO_ROOT / ".factory" / "specifications" / "golden-sample" / "01_prd.md", tmp_path / "01_prd.md")
        shutil.copy(REPO_ROOT / ".factory" / "specifications" / "golden-sample" / "02_trd.md", tmp_path / "02_trd.md")

        validator = DocSuiteValidator(workspace_root=REPO_ROOT)
        res = validator.validate_suite(tmp_path)

        assert res["passed"] is False
        assert res["completeness_score"] < 50.0
        assert len(res["missing_documents"]) == 9
        assert any("Missing mandatory document: 03_app_flow.md" in e for e in res["errors"])


def test_validator_detects_orphan_screens():
    """Verify validator catches screen parity mismatch between App Flow and UI/UX spec."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        golden_dir = REPO_ROOT / ".factory" / "specifications" / "golden-sample"

        # Copy all golden docs
        for doc in REQUIRED_DOCUMENTS:
            shutil.copy(golden_dir / doc["filename"], tmp_path / doc["filename"])

        # Inject orphan screen SCR-99 into UI/UX specification
        uiux_file = tmp_path / "04b_uiux_specification.md"
        content = uiux_file.read_text(encoding="utf-8")
        content += "\n\n### Screen SCR-99: Ghost Orphan Screen\n- Purpose: Undocumented\n- State: Default\n"
        uiux_file.write_text(content, encoding="utf-8")

        validator = DocSuiteValidator(workspace_root=REPO_ROOT)
        res = validator.validate_suite(tmp_path)

        assert res["passed"] is False
        assert any("Screen Parity Violation" in e and "SCR-99" in e for e in res["errors"])


def test_validator_detects_unmeasurable_nfr():
    """Verify validator catches qualitative unmeasurable NFR statements in PRD."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        golden_dir = REPO_ROOT / ".factory" / "specifications" / "golden-sample"

        for doc in REQUIRED_DOCUMENTS:
            shutil.copy(golden_dir / doc["filename"], tmp_path / doc["filename"])

        # Inject qualitative assertion into PRD
        prd_file = tmp_path / "01_prd.md"
        content = prd_file.read_text(encoding="utf-8")
        content += "\n\nSystem should be fast and very responsive for all clients.\n"
        prd_file.write_text(content, encoding="utf-8")

        validator = DocSuiteValidator(workspace_root=REPO_ROOT)
        res = validator.validate_suite(tmp_path)

        assert res["passed"] is False
        assert any("Unmeasurable qualitative assertion detected" in e for e in res["errors"])


def test_validator_detects_unmapped_acceptance_criteria():
    """Verify validator catches PRD acceptance criteria with no corresponding test case."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        golden_dir = REPO_ROOT / ".factory" / "specifications" / "golden-sample"

        for doc in REQUIRED_DOCUMENTS:
            shutil.copy(golden_dir / doc["filename"], tmp_path / doc["filename"])

        # Add a new functional requirement with AC-FR-099-1 to PRD without adding test to test plan
        prd_file = tmp_path / "01_prd.md"
        content = prd_file.read_text(encoding="utf-8")
        content += "\n\n### [FR-099]: Unmapped Requirement\n- User Story: Test\n- Acceptance Criteria:\n  - [ ] **[AC-FR-099-1]**: Must pass\n"
        prd_file.write_text(content, encoding="utf-8")

        validator = DocSuiteValidator(workspace_root=REPO_ROOT)
        res = validator.validate_suite(tmp_path)

        assert res["passed"] is False
        assert any("Traceability Violation" in e and "AC-FR-099-1" in e for e in res["errors"])


def test_quality_gate_0_5_evaluation_and_evidence():
    """Verify Quality Gate G0.5 evaluation writes an evidence record."""
    with tempfile.TemporaryDirectory() as tmpdir:
        line = ManufacturingLine(workspace_root=tmpdir)
        golden_dir = REPO_ROOT / ".factory" / "specifications" / "golden-sample"

        validator = DocSuiteValidator(workspace_root=tmpdir)
        eval_res = validator.evaluate_gate_0_5("quantum-vault", golden_dir, line)

        assert eval_res["status"] == "PASSED"
        assert eval_res["gate_id"] == "G0.5"
        assert eval_res["gate_name"] == "Documentation Completeness"
        assert eval_res["required_artifact"] == "DOCUMENTATION_SUITE.json"

        # Check evidence ledger written
        evidence_files = list((Path(tmpdir) / "evidence" / "manufacturing_runs").glob("G0.5_*.json"))
        assert len(evidence_files) == 1
        record = yaml.safe_load(evidence_files[0].read_text(encoding="utf-8"))
        assert record["gate_id"] == "G0.5"
        assert record["status"] == "PASSED"


def test_spec_compiler_compiles_suite_to_dag():
    """Verify SpecCompiler compiles the 10-document suite into an ordered task DAG with rollback procedures."""
    golden_dir = REPO_ROOT / ".factory" / "specifications" / "golden-sample"
    plan = SpecCompiler.compile_documentation_suite_to_plan(golden_dir)

    assert plan["plan_version"] == "2.0"
    assert plan["spec_title"] == "QuantumVault Ledger Engine"
    assert plan["total_tasks"] >= 4
    assert len(plan["phases"]) == 4

    # Check tasks have rollback procedures and skills
    for t in plan["tasks"]:
        assert "task_id" in t
        assert "station" in t
        assert "assigned_agent" in t
        assert "required_skills" in t and len(t["required_skills"]) > 0
        assert "rollback_procedure" in t and len(t["rollback_procedure"]) > 10
        assert "acceptance_criteria" in t and len(t["acceptance_criteria"]) > 0
