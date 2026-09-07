"""
Software Factory Spec-Driven Development MCP Server (factory-sdd).
Provides spec-to-plan compilation, work order generation, and gate evaluation over stdio JSON-RPC.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.spec_compiler import SpecCompiler
from core.manufacturing_line import ManufacturingLine

mfg_line = ManufacturingLine()

def handle_rpc_call(method: str, params: dict) -> dict:
    if method == "sdd.compile_plan":
        return SpecCompiler.compile_spec_to_plan(params.get("spec", {}))
    elif method == "sdd.work_orders":
        return mfg_line.generate_work_orders(
            spec_name=params.get("spec_name", "Spec"),
            tasks=params.get("tasks", [])
        )
    elif method == "sdd.evaluate_gate":
        return mfg_line.evaluate_gate(
            gate_id=params.get("gate_id", "G7"),
            evidence_data=params.get("evidence", {})
        )
    else:
        return {"error": f"Unknown method {method}"}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_rpc_call("sdd.work_orders", {"spec_name": "Test", "tasks": []})))
    else:
        print(json.dumps({"status": "factory-sdd-mcp ready", "protocol": "json-rpc-2.0"}))
