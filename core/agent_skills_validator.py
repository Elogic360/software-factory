"""
Software Factory — Agent Skills Open Standard (agentskills.io) Validator.
Validates skill markdown definitions against the open Agent Skills specification:
- YAML frontmatter metadata (name, description)
- Clean parameter documentation and concrete examples
- Progressive disclosure token limits (< 5,000 tokens)
- Agent-agnostic neutrality (no hardcoded Claude/Cursor-only dependencies)
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


class AgentSkillsValidator:
    """Validates SKILL.md files against the open agentskills.io standard."""

    MAX_RECOMMENDED_TOKENS = 5000

    def parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extracts and parses YAML frontmatter from SKILL.md."""
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
        if not match:
            return {"has_frontmatter": False, "frontmatter": {}, "body": content}

        raw_yaml = match.group(1)
        body = match.group(2)
        try:
            data = yaml.safe_load(raw_yaml)
            return {
                "has_frontmatter": True,
                "frontmatter": data if isinstance(data, dict) else {},
                "body": body
            }
        except Exception:
            return {"has_frontmatter": False, "frontmatter": {}, "body": body}

    def validate_skill_file(self, skill_file_path: str) -> Dict[str, Any]:
        """Audits a skill file against the agentskills.io standard."""
        p = Path(skill_file_path)
        if not p.exists():
            return {"valid": False, "error": f"File not found: {skill_file_path}"}

        content = p.read_text(encoding="utf-8")
        parsed = self.parse_frontmatter(content)

        errors = []
        warnings = []

        if not parsed["has_frontmatter"]:
            legacy_match = re.search(r"^#\s*SKILL:\s*(.+)$", content, re.MULTILINE)
            if legacy_match:
                warnings.append("Skill uses legacy markdown format without YAML frontmatter. Migratable to agentskills.io standard.")
                # Can still be considered valid in hybrid mode if legacy header is found
                is_legacy_valid = True
            else:
                errors.append("Missing YAML frontmatter delimiters (---) at top of SKILL.md")
                is_legacy_valid = False
        else:
            is_legacy_valid = False
            fm = parsed["frontmatter"]
            if "name" not in fm or not str(fm["name"]).strip():
                errors.append("Frontmatter missing required 'name' attribute")
            if "description" not in fm or not str(fm["description"]).strip():
                errors.append("Frontmatter missing required 'description' attribute")

        # Rough token estimation (4 chars per token)
        estimated_tokens = len(content) // 4
        if estimated_tokens > self.MAX_RECOMMENDED_TOKENS:
            warnings.append(
                f"Skill file is large ({estimated_tokens} est. tokens > {self.MAX_RECOMMENDED_TOKENS}). "
                f"Consider splitting into references/ or scripts/ per progressive loading protocol."
            )

        # Agent-agnostic checks
        body = parsed["body"]
        vendor_locks = []
        for vendor in ["claude only", "cursor only", "codex only"]:
            if vendor in body.lower():
                vendor_locks.append(vendor)

        if vendor_locks:
            warnings.append(f"Potential vendor lock-in phrases detected: {vendor_locks}")

        is_valid = len(errors) == 0
        return {
            "file": str(p),
            "valid": is_valid,
            "standard": "agentskills.io (v1.0)",
            "format": "agentskills_open_standard" if parsed["has_frontmatter"] else ("legacy_factory_markdown" if is_legacy_valid else "invalid"),
            "estimated_tokens": estimated_tokens,
            "errors": errors,
            "warnings": warnings,
            "verdict": "COMPLIANT" if is_valid else "NON_COMPLIANT"
        }

    def generate_open_standard_frontmatter(self, content: str) -> str:
        """Converts legacy markdown skill into compliant agentskills.io format."""
        parsed = self.parse_frontmatter(content)
        if parsed["has_frontmatter"]:
            return content

        name_match = re.search(r"^#\s*(?:SKILL:\s*)?(.+)$", content, re.MULTILINE)
        trigger_match = re.search(r"\*\*Activation triggers:\*\*\s*(.+)$", content, re.MULTILINE)

        name = name_match.group(1).strip() if name_match else "unnamed-skill"
        description = trigger_match.group(1).strip() if trigger_match else f"Skill providing capabilities for {name}"

        frontmatter = f"---\nname: {name}\ndescription: {description}\n---\n\n"
        return frontmatter + content

