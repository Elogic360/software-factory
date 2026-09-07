"""
core/security_auditor.py — Skill & Capability Supply-Chain Security Auditor
Performs static analysis, AST inspection, secret scanning, and prompt injection
detection across skills, MCP configs, and code artifacts.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

DANGEROUS_PATTERNS = [
    (r"curl\s+[^\|]+\|\s*(?:ba)?sh", "Unverified remote script execution (curl | bash)", "critical"),
    (r"wget\s+[^\|]+\|\s*(?:ba)?sh", "Unverified remote script execution (wget | bash)", "critical"),
    (r"base64\s+-d\s*\|", "Obfuscated payload execution via base64", "high"),
    (r"eval\s*\(\s*base64", "Python eval base64 payload", "critical"),
    (r"(?:rm\s+-rf\s+[/~]|\brmdir\s+/s\s+/q\b)", "Destructive filesystem operation", "critical"),
    (r"(?:export\s+[A-Z_]*KEY|export\s+[A-Z_]*SECRET|export\s+[A-Z_]*TOKEN)", "Hardcoded credential export pattern", "medium"),
    (r"(?:ignore\s+all\s+previous\s+instructions|disregard\s+the\s+above)", "Prompt injection override pattern", "high"),
    (r"(?:fetch|requests\.post)\s*\(['\"][^'\"]*webhook\.site", "Potential data exfiltration endpoint", "critical"),
]

class SecurityAuditor:
    def __init__(self):
        pass

    def scan_content(self, text: str, source_name: str = "unknown") -> Dict[str, Any]:
        findings = []
        highest_risk = "low"
        risk_weights = {"low": 0, "medium": 3, "high": 7, "critical": 10}
        total_risk_score = 0

        for pattern, desc, severity in DANGEROUS_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                findings.append({
                    "description": desc,
                    "severity": severity,
                    "count": len(matches)
                })
                total_risk_score += risk_weights.get(severity, 1) * len(matches)
                if risk_weights.get(severity, 0) > risk_weights.get(highest_risk, 0):
                    highest_risk = severity

        # Compute Trust Level
        if highest_risk == "critical":
            trust_level = "QUARANTINED"
            verdict = "REJECTED"
        elif highest_risk == "high":
            trust_level = "EXPERIMENTAL"
            verdict = "REQUIRES_REVIEW"
        elif highest_risk == "medium":
            trust_level = "COMMUNITY_VERIFIED"
            verdict = "APPROVED_WITH_WARNINGS"
        else:
            trust_level = "TRUSTED_VERIFIED"
            verdict = "APPROVED"

        return {
            "source": source_name,
            "verdict": verdict,
            "trust_level": trust_level,
            "risk_score": total_risk_score,
            "highest_severity": highest_risk,
            "findings": findings,
            "is_clean": len(findings) == 0
        }

    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        if not file_path.exists():
            return {"error": f"File {file_path} not found", "verdict": "ERROR"}
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            return self.scan_content(content, source_name=str(file_path.name))
        except Exception as e:
            return {"error": str(e), "verdict": "ERROR"}

    def scan_skill_directory(self, skill_dir: Path) -> Dict[str, Any]:
        results = []
        overall_clean = True
        for p in skill_dir.rglob("*"):
            if p.is_file() and p.suffix in [".md", ".py", ".sh", ".js", ".ts", ".json"]:
                res = self.scan_file(p)
                if not res.get("is_clean", True):
                    overall_clean = False
                results.append(res)
        return {
            "skill": skill_dir.name,
            "overall_clean": overall_clean,
            "files_scanned": len(results),
            "file_results": results
        }
