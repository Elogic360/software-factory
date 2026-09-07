"""
Software Factory — Constitution Guard & Operational Safety Hook.
Implements the athola/claude-night-market enforcement pattern:
1. Constitutional override of conflicting tools/agents.
2. TDD Gate blocking production code writes without failing/passing test correlation.
3. Destructive Command Blocker (rm -rf, git push --force, DROP SCHEMA CASCADE).
4. Structural Architectural Invariant Verification.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class ConstitutionGuard:
    """Protects the repository from destructive operations, TDD violations, and architectural drift."""

    DESTRUCTIVE_COMMAND_PATTERNS = [
        (r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\s+[/~.*]", "Recursive destructive delete of root, home, or wildcard target"),
        (r"\bgit\s+push\s+.*(-f|--force)\b", "Forced git push is prohibited; branch history must remain immutable"),
        (r"\b(DROP\s+DATABASE|DROP\s+SCHEMA\s+.*CASCADE|TRUNCATE\s+TABLE)\b", "Unsafe destructive database query outside migration sandbox"),
        (r"\bmkfs\b|\bdd\s+if=.*of=/dev/", "Block-level device wipe operation"),
        (r"\b(chmod\s+-R\s+777|chown\s+-R)\s+/", "Destructive root permission alteration")
    ]

    CONSTITUTIONAL_INVARIANTS = [
        (r"(localhost:800[0-9]|127\.0\.0\.1:800[0-9])", "Hardcoded local port reference violates universal environment portability"),
        (r"""(SECRET_KEY|API_KEY|PASSWORD)\s*=\s*['"][a-zA-Z0-9_!@#$%^&*]{8,}['"]""", "Hardcoded plaintext credential violates Security Law"),
        (r"\b(DROP\s+TABLE\s+IF\s+EXISTS)\b", "Direct DROP TABLE without versioned migration history violates Database Law")
    ]

    def __init__(self, constitution_path: Optional[str] = None):
        if constitution_path is None:
            self.constitution_path = Path(__file__).resolve().parent.parent / "CONSTITUTION.md"
        else:
            self.constitution_path = Path(constitution_path)

    def verify_command_safety(self, command: str) -> Dict[str, Any]:
        """Audits command before shell execution against destructive command rules."""
        for pattern, explanation in self.DESTRUCTIVE_COMMAND_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    "allowed": False,
                    "verdict": "BLOCKED",
                    "matched_pattern": pattern,
                    "reason": explanation,
                    "remediation": "Refactor command to use safe scoped paths or standard non-destructive tooling."
                }

        return {
            "allowed": True,
            "verdict": "PERMITTED",
            "reason": "Command passed non-destructive safety filter."
        }

    def evaluate_tdd_gate(
        self,
        modified_impl_files: List[str],
        test_files: List[str],
        test_run_passed: bool = False
    ) -> Dict[str, Any]:
        """Enforces TDD gate: code implementation requires verified test coverage."""
        if not modified_impl_files:
            return {"status": "PASSED", "gate": "TDD_GATE", "details": "No implementation files modified."}

        # Filter out non-code docs/configs
        code_impls = [
            f for f in modified_impl_files
            if f.endswith((".py", ".ts", ".tsx", ".js", ".go", ".rs"))
            and not any(p in f for p in ["tests/", "test_", ".test.", ".spec."])
        ]

        if not code_impls:
            return {"status": "PASSED", "gate": "TDD_GATE", "details": "Only configuration or docs touched."}

        if not test_files:
            return {
                "status": "BLOCKED",
                "gate": "TDD_GATE",
                "reason": "TDD Violation: Implementation code modified without accompanying test files.",
                "uncovered_files": code_impls,
                "remediation": "Author failing test in tests/ covering the new behavior before writing implementation."
            }

        if not test_run_passed:
            return {
                "status": "FAILED",
                "gate": "TDD_GATE",
                "reason": "TDD Verification Failed: Tests have not passed with green status.",
                "remediation": "Run test suite and ensure all assertions pass before moving target to VERIFIED."
            }

        return {
            "status": "PASSED",
            "gate": "TDD_GATE",
            "verified_files": code_impls,
            "test_coverage_files": test_files
        }

    def scan_code_invariants(self, file_path: str, file_content: str) -> List[Dict[str, Any]]:
        """Scans single file for constitutional invariant violations."""
        violations = []
        # Exclude documentation files and tests from strict hardcoded warnings
        if file_path.endswith((".md", ".txt", ".log", ".example")):
            return []

        for pattern, explanation in self.CONSTITUTIONAL_INVARIANTS:
            match = re.search(pattern, file_content)
            if match:
                violations.append({
                    "file": file_path,
                    "matched": match.group(0),
                    "reason": explanation
                })

        return violations
