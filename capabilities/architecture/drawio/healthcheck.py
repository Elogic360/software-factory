"""
Healthcheck script for Official draw.io MCP capability.
"""

import sys
import json
import shutil
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from core.architecture_engine import ArchitectureEngine


def run_healthcheck():
    checks = []
    errors = []

    node_bin = shutil.which("node")
    npx_bin = shutil.which("npx")
    if node_bin:
        checks.append(f"Node runtime located at {node_bin}")
    else:
        errors.append("Node.js runtime not found in PATH")

    if npx_bin:
        checks.append(f"npx package runner located at {npx_bin}")
    else:
        errors.append("npx runner not found in PATH")

    try:
        engine = ArchitectureEngine()
        c4_stub = {
            "product": "ValidationSystem",
            "c2_containers": [
                {"name": "Frontend", "tech": "React", "description": "Web UI"},
                {"name": "Backend", "tech": "FastAPI", "description": "API"}
            ]
        }
        xml_out = engine.generate_drawio_architecture(c4_stub)
        assert "<mxGraphModel" in xml_out
        assert "ValidationSystem" in xml_out
        checks.append("Draw.io XML generation operational")

        validation = engine.validate_diagram_layout(xml_out)
        assert validation["valid"] is True
        checks.append("Diagram collision & boundary validation operational")

        mermaid_sample = """graph TD
Frontend --> Backend
"""
        converted_xml = engine.convert_mermaid_to_drawio_xml(mermaid_sample)
        assert "<mxGraphModel" in converted_xml
        checks.append("Mermaid.js to Draw.io conversion operational")

    except Exception as e:
        errors.append(str(e))

    status = "HEALTHY" if not errors else "DEGRADED"
    return {
        "capability": "drawio-official-mcp",
        "status": status,
        "checks": checks,
        "errors": errors
    }


if __name__ == "__main__":
    res = run_healthcheck()
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["status"] == "HEALTHY" else 1)
