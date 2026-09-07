"""
Software Factory Enterprise SDD Specification-to-Plan Compiler.
Transforms Product Discovery -> Requirements -> System Spec -> Implementation Plan -> Work Orders.
"""

import json
import time
from typing import Dict, List, Any, Optional

class SpecCompiler:
    """Compiles specifications into actionable engineering work plans and dependency graphs."""

    @staticmethod
    def compile_spec_to_plan(spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compiles product specification into structured implementation plan with task graph.
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
                "required_skills": ["database-postgresql"],
                "required_mcp": ["factory-context-mcp", "factory-memory-mcp"],
                "dependencies": [],
                "acceptance_criteria": ["All models defined with constraints", "Alembic / SQL migrations pass cleanly"],
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
                "required_skills": ["fastapi-patterns", "api-design"],
                "required_mcp": ["factory-context-mcp"],
                "dependencies": list(prev_dep),
                "acceptance_criteria": [f"Endpoint satisfies requirement '{r}'", "Type checking and unit tests pass"],
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
            "required_skills": ["e2e-testing", "security-review"],
            "required_mcp": ["playwright"],
            "dependencies": list(prev_dep),
            "acceptance_criteria": ["SAST scan clean", "E2E journey tests 100% passing"],
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
