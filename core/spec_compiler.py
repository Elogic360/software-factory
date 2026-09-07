"""
Software Factory Enterprise SDD Specification-to-Plan Compiler.
Transforms Product Discovery -> Requirements -> System Spec -> Implementation Plan -> Work Orders.
Consumes multi-document SDD suites (PRD, TRD, App Flow, UI/UX, Schema, Backend Arch, Project Arch, Testing Plan, Scaling Plan).
"""

import os
import re
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Set

class SpecCompiler:
    """Compiles specifications into actionable engineering work plans and dependency graphs."""

    @staticmethod
    def compile_spec_to_plan(spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compiles product specification into structured implementation plan with task graph.
        Legacy/simple dictionary input compatibility.
        """
        title = spec.get("title", "Software Product")
        reqs = spec.get("functional_requirements", [])
        arch = spec.get("architecture", {})

        tasks = []
        task_id_counter = 1

        # Phase 1: Database & Data Schema Tasks
        if "database" in arch or any("data" in r.lower() or "db" in r.lower() for r in reqs):
            tasks.append({
                "task_id": f"TSK-{task_id_counter:03d}",
                "phase": "Phase 1 - Data & Persistence",
                "title": f"Design Database Schemas & Migrations for {title}",
                "station": "Data Architecture",
                "assigned_agent": "Database Architect",
                "required_skills": ["database-postgresql", "schema-design-document"],
                "required_mcp": ["factory-context-mcp", "factory-memory-mcp"],
                "dependencies": [],
                "acceptance_criteria": ["All models defined with constraints", "Alembic / SQL migrations pass cleanly"],
                "rollback_procedure": "Revert database migrations down to prior revision.",
                "status": "QUEUED"
            })
            task_id_counter += 1

        # Phase 2: Core Domain & Backend APIs
        prev_dep = [tasks[-1]["task_id"]] if tasks else []
        for r in reqs:
            tasks.append({
                "task_id": f"TSK-{task_id_counter:03d}",
                "phase": "Phase 2 - Core Backend API",
                "title": f"Implement API for: {r}",
                "station": "Production Floor",
                "assigned_agent": "Backend Engineer",
                "required_skills": ["fastapi-patterns", "api-design", "backend-architecture-document"],
                "required_mcp": ["factory-context-mcp"],
                "dependencies": list(prev_dep),
                "acceptance_criteria": [f"Endpoint satisfies requirement '{r}'", "Type checking and unit tests pass"],
                "rollback_procedure": "Revert API routing and disable feature flag.",
                "status": "QUEUED"
            })
            prev_dep = [f"TSK-{task_id_counter:03d}"]
            task_id_counter += 1

        # Phase 3: Verification & Security
        tasks.append({
            "task_id": f"TSK-{task_id_counter:03d}",
            "phase": "Phase 3 - Security & QA",
            "title": f"Security Audit & E2E Validation for {title}",
            "station": "Security Lab / QA Lab",
            "assigned_agent": "QA Engineer",
            "required_skills": ["e2e-testing", "security-review", "testing-plan-authoring"],
            "required_mcp": ["playwright"],
            "dependencies": list(prev_dep),
            "acceptance_criteria": ["SAST scan clean", "E2E journey tests 100% passing"],
            "rollback_procedure": "Block release candidate promotion.",
            "status": "QUEUED"
        })

        return {
            "plan_version": "1.0",
            "spec_title": title,
            "compiled_at": time.time(),
            "total_tasks": len(tasks),
            "phases": ["Data & Persistence", "Core Backend API", "Security & QA"],
            "tasks": tasks
        }

    @classmethod
    def compile_documentation_suite_to_plan(cls, suite_dir: Path | str) -> Dict[str, Any]:
        """
        Compiles a complete 10-document SDD specification suite into an ordered
        implementation plan and dependency DAG.
        """
        suite_path = Path(suite_dir)
        prd_file = suite_path / "01_prd.md"
        trd_file = suite_path / "02_trd.md"
        flow_file = suite_path / "03_app_flow.md"
        uiux_file = suite_path / "04b_uiux_specification.md"
        schema_file = suite_path / "05_schema_document.md"
        backend_file = suite_path / "06_backend_architecture.md"
        arch_file = suite_path / "07_project_architecture.md"
        test_file = suite_path / "09_testing_plan.md"
        scaling_file = suite_path / "10_scaling_plan.md"

        prd_text = prd_file.read_text(encoding="utf-8") if prd_file.exists() else ""
        flow_text = flow_file.read_text(encoding="utf-8") if flow_file.exists() else ""
        schema_text = schema_file.read_text(encoding="utf-8") if schema_file.exists() else ""

        # Extract title
        title_match = re.search(r"#\s*Product Requirement Document \(PRD\):\s*(.+)", prd_text)
        title = title_match.group(1).strip() if title_match else "Enterprise Product"

        # Extract FRs
        fr_matches = re.findall(r"###\s*\[(FR-\d+)\]:\s*(.+)", prd_text)

        # Extract screens from flow
        screen_matches = re.findall(r"\| (SCR-\d+) \| ([^\|]+) \|", flow_text)

        tasks = []
        task_id_counter = 1

        # Phase 1: Data Architecture & Persistence
        db_task_id = f"TSK-{task_id_counter:03d}"
        tasks.append({
            "task_id": db_task_id,
            "phase": "Phase 1 - Data Architecture & Schema Migrations",
            "title": f"Implement Database Schemas & Migrations for {title}",
            "station": "Station 04 (Data Architecture)",
            "assigned_agent": "Database Architect",
            "traceability": ["SCH-001", "TRD-DAT-01"],
            "required_skills": ["database-postgresql", "schema-design-document"],
            "required_mcp": ["postgres", "factory-memory-mcp"],
            "required_raw_materials": ["alembic-migrations", "docker-compose-db"],
            "dependencies": [],
            "complexity": "Medium",
            "risk": "High",
            "acceptance_criteria": ["All models defined with constraints", "SQL migrations pass cleanly"],
            "rollback_procedure": "Execute reverse SQL migration script.",
            "status": "QUEUED"
        })
        task_id_counter += 1

        # Phase 2: Core Backend Services & APIs
        backend_task_ids = []
        for fid, ftitle in fr_matches:
            tid = f"TSK-{task_id_counter:03d}"
            tasks.append({
                "task_id": tid,
                "phase": "Phase 2 - Core Backend Services & Domain Logic",
                "title": f"Implement Service & API for [{fid}] {ftitle}",
                "station": "Station 08 (Backend Engineering)",
                "assigned_agent": "Backend Engineer",
                "traceability": [fid, "TRD-API-01", "ARC-BE-001"],
                "required_skills": ["fastapi-patterns", "backend-architecture-document", "api-design"],
                "required_mcp": ["factory-context-mcp"],
                "required_raw_materials": ["fastapi-enterprise-scaffold"],
                "dependencies": [db_task_id],
                "complexity": "High",
                "risk": "Medium",
                "acceptance_criteria": [f"API satisfying requirement [{fid}] returns valid contracts"],
                "rollback_procedure": "Disable feature flag; revert service container revision.",
                "status": "QUEUED"
            })
            backend_task_ids.append(tid)
            task_id_counter += 1

        # Phase 3: Frontend Primitives & Screens
        frontend_task_ids = []
        for sid, sname in screen_matches[:4]: # Top screens
            tid = f"TSK-{task_id_counter:03d}"
            tasks.append({
                "task_id": tid,
                "phase": "Phase 3 - Frontend Views & Component Assembly",
                "title": f"Implement Screen [{sid}] {sname.strip()}",
                "station": "Station 09 (Frontend Engineering)",
                "assigned_agent": "Frontend Engineer",
                "traceability": [sid, "UIX-001", "FLW-001"],
                "required_skills": ["frontend-react", "uiux-specification", "accessibility"],
                "required_mcp": ["playwright"],
                "required_raw_materials": ["tailwind-design-tokens", "ui-primitives"],
                "dependencies": backend_task_ids[:1] if backend_task_ids else [db_task_id],
                "complexity": "Medium",
                "risk": "Low",
                "acceptance_criteria": [f"Screen [{sid}] renders all 5 states (default, loading, empty, error, success)"],
                "rollback_procedure": "Revert frontend bundle release.",
                "status": "QUEUED"
            })
            frontend_task_ids.append(tid)
            task_id_counter += 1

        # Phase 4: Quality Assurance, Security & Release Signoff
        all_deps = list(set([db_task_id] + backend_task_ids + frontend_task_ids))
        tasks.append({
            "task_id": f"TSK-{task_id_counter:03d}",
            "phase": "Phase 4 - Verification, Security & Release Signoff",
            "title": f"Execute Full Multi-Layer Test Suite & Gate Signoff for {title}",
            "station": "Station 12 (QA & Release Control)",
            "assigned_agent": "QA Lead",
            "traceability": ["TST-001", "NFR-001", "NFR-003"],
            "required_skills": ["testing-plan-authoring", "security-audit", "e2e-testing"],
            "required_mcp": ["playwright", "factory-context-mcp"],
            "required_raw_materials": ["testcontainers", "axe-core"],
            "dependencies": all_deps,
            "complexity": "High",
            "risk": "High",
            "acceptance_criteria": [
                "100% of PRD acceptance criteria verified by automated tests",
                "SAST scan clean (0 High/Critical)",
                "Gate G0.5 and G7-G13 signoff completed"
            ],
            "rollback_procedure": "Halt release candidate signoff.",
            "status": "QUEUED"
        })

        return {
            "plan_version": "2.0",
            "spec_title": title,
            "suite_directory": str(suite_path),
            "compiled_at": time.time(),
            "total_tasks": len(tasks),
            "phases": [
                "Phase 1 - Data Architecture & Schema Migrations",
                "Phase 2 - Core Backend Services & Domain Logic",
                "Phase 3 - Frontend Views & Component Assembly",
                "Phase 4 - Verification, Security & Release Signoff"
            ],
            "tasks": tasks
        }
