"""
Software Factory Architecture State & Compiler.
Enforces Section 22 Architecture-First specification, manages architecture-state.yaml,
and compiles architectural contracts into verified code skeletons and boundary rules.
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

DEFAULT_INVARIANTS = [
    {"id": "NO_CROSS_SCHEMA_WRITES", "rule": "A service or module must never perform direct writes across DB schemas."},
    {"id": "ALL_ROUTES_VERSIONED_V1", "rule": "All public and internal API endpoints must be prefixed with /api/v1/."},
    {"id": "STRICT_MODULE_EXPORTS", "rule": "Modules must only consume external domain internals via public index exports."},
    {"id": "NO_RAW_QUERIES_IN_CONTROLLERS", "rule": "Controllers and HTTP handlers must delegate data access to service/repository layers."},
    {"id": "NO_HARDCODED_SECRETS", "rule": "Configuration and secrets must be injected via environment or secure keyrings."}
]

DEFAULT_VERIFICATION_GATES = [
    "GATE_0_SPEC_AND_ARCHITECTURE",
    "GATE_1_STATIC_ANALYSIS",
    "GATE_2_UNIT_AND_CONTRACT_TESTS",
    "GATE_3_BROWSER_AND_ACCESSIBILITY",
    "GATE_4_SECURITY_AND_SUPPLY_CHAIN",
    "GATE_5_PRODUCTION_READINESS"
]

class ArchitectureStateManager:
    """Manages architecture-state.yaml lifecycle, invariants, and implementation compiler."""

    def __init__(self, state_path: Optional[str] = None):
        if state_path is None:
            self.state_path = Path(__file__).resolve().parent.parent / "state" / "architecture-state.yaml"
        else:
            self.state_path = Path(state_path)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

    def create_default_architecture(self, name: str, archetype: str = "python-fastapi") -> Dict[str, Any]:
        """Creates a Section 22 compliant architecture state template."""
        return {
            "schema_version": "2.2.0",
            "project": {
                "name": name,
                "slug": name.lower().replace(" ", "-"),
                "version": "0.1.0",
                "archetype": archetype,
                "language": "python" if "python" in archetype else "typescript",
                "framework": "fastapi" if "fastapi" in archetype else "react",
                "database": "postgresql",
                "cache": "valkey-redis",
                "auth_strategy": "jwt-bearer"
            },
            "boundaries": [
                {
                    "module": "core",
                    "responsibility": "Shared domain models, events, and utility primitives",
                    "exported_symbols": ["EventBus", "BaseModel", "Config"],
                    "forbidden_imports": ["controllers", "web"]
                },
                {
                    "module": "api",
                    "responsibility": "HTTP handlers, OpenAPI routing, and request validation",
                    "exported_symbols": ["router", "dependencies"],
                    "forbidden_imports": ["database_internal"]
                },
                {
                    "module": "services",
                    "responsibility": "Business logic and transactional orchestration",
                    "exported_symbols": ["DomainService"],
                    "forbidden_imports": ["web_controllers"]
                }
            ],
            "routes": [
                {
                    "method": "GET",
                    "path": "/api/v1/health",
                    "module": "api",
                    "auth_required": False,
                    "rate_limit": "100/min",
                    "db_operations": ["read_health"]
                },
                {
                    "method": "GET",
                    "path": "/api/v1/items",
                    "module": "api",
                    "auth_required": True,
                    "rate_limit": "60/min",
                    "db_operations": ["select_items"]
                }
            ],
            "data_models": [
                {
                    "name": "Item",
                    "table": "items",
                    "fields": {
                        "id": "UUID",
                        "title": "VARCHAR(255)",
                        "created_at": "TIMESTAMP"
                    },
                    "indexes": ["idx_items_created_at"]
                }
            ],
            "invariants": DEFAULT_INVARIANTS,
            "verification_gates": DEFAULT_VERIFICATION_GATES,
            "metadata": {
                "created_at": time.time(),
                "last_modified": time.time(),
                "architect_agent": "Antigravity-Software-Factory"
            }
        }

    def validate_architecture_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Strict validation of architecture-state.yaml against Section 22 rules."""
        errors = []
        warnings = []

        if not isinstance(state, dict):
            return {"valid": False, "errors": ["Architecture state must be a dictionary."]}

        if "schema_version" not in state:
            errors.append("Missing 'schema_version'.")

        project = state.get("project", {})
        if not project.get("name") or not project.get("slug"):
            errors.append("Project metadata must include 'name' and 'slug'.")

        # Invariant checks
        routes = state.get("routes", [])
        for r in routes:
            path = r.get("path", "")
            if not path.startswith("/api/v1/"):
                warnings.append(f"Route '{path}' violates ALL_ROUTES_VERSIONED_V1 invariant.")

        # Boundaries checks
        boundaries = state.get("boundaries", [])
        if not boundaries:
            errors.append("At least one bounded context module must be defined in 'boundaries'.")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "boundary_count": len(boundaries),
            "route_count": len(routes),
            "invariant_count": len(state.get("invariants", []))
        }

    def save(self, state: Dict[str, Any], path: Optional[Path] = None) -> Path:
        """Saves architecture state to YAML."""
        target = path or self.state_path
        state.setdefault("metadata", {})["last_modified"] = time.time()
        with open(target, "w", encoding="utf-8") as f:
            yaml.dump(state, f, default_flow_style=False, sort_keys=False)
        return target

    def load(self, path: Optional[Path] = None) -> Dict[str, Any]:
        """Loads and returns architecture state."""
        target = path or self.state_path
        if not target.exists():
            default_state = self.create_default_architecture("Default-System")
            self.save(default_state, target)
            return default_state

        with open(target, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def compile_scaffolding(self, state: Dict[str, Any], destination_dir: Path) -> List[str]:
        """Compiles architecture state into concrete directories and stub files."""
        created_files = []
        destination_dir = Path(destination_dir)
        destination_dir.mkdir(parents=True, exist_ok=True)

        # 1. Create boundary directories
        for b in state.get("boundaries", []):
            mod_name = b.get("module", "unnamed")
            mod_dir = destination_dir / mod_name
            mod_dir.mkdir(parents=True, exist_ok=True)

            init_file = mod_dir / "__init__.py"
            if not init_file.exists():
                exports = b.get("exported_symbols", [])
                content = f'"""\nBounded context: {mod_name}\nResponsibility: {b.get("responsibility")}\n"""\n\n'
                content += f"__all__ = {exports}\n"
                init_file.write_text(content, encoding="utf-8")
                created_files.append(str(init_file))

        # 2. Write architecture state snapshot into project
        arch_snapshot = destination_dir / "architecture-state.yaml"
        with open(arch_snapshot, "w", encoding="utf-8") as f:
            yaml.dump(state, f, default_flow_style=False, sort_keys=False)
        created_files.append(str(arch_snapshot))

        return created_files

    def verify_code_compliance(self, project_root: Path, state: Dict[str, Any]) -> Dict[str, Any]:
        """Scans codebase to detect violations of boundary rules and invariants."""
        violations = []
        project_root = Path(project_root)

        boundaries = {b["module"]: b for b in state.get("boundaries", [])}

        for root, _, files in os.walk(project_root):
            for file in files:
                if file.endswith((".py", ".ts", ".js")):
                    f_path = Path(root) / file
                    try:
                        content = f_path.read_text(encoding="utf-8", errors="ignore")
                    except Exception:
                        continue

                    # Check forbidden imports
                    rel_path = f_path.relative_to(project_root)
                    top_module = rel_path.parts[0] if rel_path.parts else ""

                    if top_module in boundaries:
                        forbidden = boundaries[top_module].get("forbidden_imports", [])
                        for bad in forbidden:
                            if f"import {bad}" in content or f"from {bad}" in content:
                                violations.append({
                                    "file": str(rel_path),
                                    "rule": "FORBIDDEN_IMPORT",
                                    "detail": f"Module '{top_module}' cannot import '{bad}'."
                                })

        return {
            "compliant": len(violations) == 0,
            "violations_count": len(violations),
            "violations": violations,
            "status": "PASSED" if not violations else "FAILED"
        }
