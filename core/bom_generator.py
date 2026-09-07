"""
Software Factory Capability Bill of Materials (CBOM & SBOM) Generator.
Traces every manufactured artifact to its raw materials, tools, MCPs, skills, and upstream licenses.
"""

import json
import time
from typing import Dict, List, Any, Optional

class BillOfMaterialsGenerator:
    """Generates formal Capability Bill of Materials (CBOM)."""

    @staticmethod
    def generate_cbom(
        product_name: str,
        version: str,
        raw_materials: List[Dict[str, str]],
        tools: List[Dict[str, str]],
        mcp_servers: List[Dict[str, str]],
        skills: List[Dict[str, str]],
        agents: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Creates a standardized CBOM dictionary."""
        cbom = {
            "bom_version": "1.0",
            "product": product_name,
            "product_version": version,
            "generated_at": time.time(),
            "raw_materials": [
                {
                    "name": rm.get("name", "unknown"),
                    "category": rm.get("category", "library"),
                    "version": rm.get("version", "latest"),
                    "license": rm.get("license", "MIT"),
                    "source": rm.get("source", "registry")
                }
                for rm in raw_materials
            ],
            "machinery_tools": [
                {
                    "name": t.get("name", "unknown"),
                    "type": t.get("type", "cli"),
                    "version": t.get("version", "latest"),
                    "license": t.get("license", "Apache-2.0")
                }
                for t in tools
            ],
            "mcp_servers": [
                {
                    "name": m.get("name", "unknown"),
                    "transport": m.get("transport", "stdio"),
                    "permission_tier": m.get("tier", "T2_WORKSPACE_READ")
                }
                for m in mcp_servers
            ],
            "skills": [
                {
                    "name": s.get("name", "unknown"),
                    "domain": s.get("domain", "general"),
                    "verified": s.get("verified", True)
                }
                for s in skills
            ],
            "agents": [
                {
                    "role": a.get("role", "developer"),
                    "model": a.get("model", "default")
                }
                for a in agents
            ]
        }
        return cbom
