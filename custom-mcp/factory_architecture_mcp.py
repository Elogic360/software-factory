"""
Software Factory Architecture MCP Server (factory-architecture).
Provides C4 modeling, Mermaid rendering, and architecture drift detection over stdio JSON-RPC.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.architecture_engine import ArchitectureEngine

engine = ArchitectureEngine()

def handle_rpc_call(method: str, params: dict) -> dict:
    if method == "architecture.c4":
        return engine.generate_c4_model(
            product_name=params.get("product", "System"),
            containers=params.get("containers", []),
            components=params.get("components", [])
        )
    elif method == "architecture.mermaid":
        c4_model = params.get("c4_model", {})
        return {"mermaid": engine.generate_mermaid_c4(c4_model)}
    elif method == "architecture.drift":
        return engine.detect_drift(
            expected_graph=params.get("expected_graph", {}),
            live_endpoints=params.get("live_endpoints", [])
        )
    else:
        return {"error": f"Unknown method {method}"}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_rpc_call("architecture.c4", {"product": "Test"})))
    else:
        print(json.dumps({"status": "factory-architecture-mcp ready", "protocol": "json-rpc-2.0"}))
