"""
Software Factory SDD MCP Server (factory-sdd-mcp).
Full stdio JSON-RPC 2.0 interactive server.
Tools: compile_plan, generate_work_orders, evaluate_gate
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.spec_compiler import SpecCompiler
from core.manufacturing_line import ManufacturingLine

TOOLS = [
    {"name": "compile_plan",
     "description": "Compile a product spec into an ordered implementation plan.",
     "inputSchema": {"type": "object", "properties": {"spec": {"type": "object"}}, "required": ["spec"]}},
    {"name": "generate_work_orders",
     "description": "Generate factory work orders from a spec name and task list.",
     "inputSchema": {"type": "object", "properties": {
         "spec_name": {"type": "string"}, "tasks": {"type": "array"}},
     "required": ["spec_name", "tasks"]}},
    {"name": "evaluate_gate",
     "description": "Evaluate a quality gate against provided evidence data.",
     "inputSchema": {"type": "object", "properties": {
         "gate_id": {"type": "string"}, "evidence": {"type": "object"}},
     "required": ["gate_id"]}},
]

def main():
    mfg_line = ManufacturingLine()
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            continue
        method = msg.get("method", "")
        params = msg.get("params") or {}
        msg_id = msg.get("id")

        try:
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "factory-sdd-mcp", "version": "2.0.0"},
                    "capabilities": {"tools": {}}}}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "compile_plan":
                    result = SpecCompiler.compile_spec_to_plan(args.get("spec", {}))
                    res_content = json.dumps(result, indent=2)
                elif name == "generate_work_orders":
                    result = mfg_line.generate_work_orders(
                        spec_name=args.get("spec_name", "Spec"),
                        tasks=args.get("tasks", []))
                    res_content = json.dumps(result, indent=2)
                elif name == "evaluate_gate":
                    result = mfg_line.evaluate_gate(
                        gate_id=args.get("gate_id", "G7"),
                        evidence_data=args.get("evidence", {}))
                    res_content = json.dumps(result, indent=2)
                else:
                    res_content = json.dumps({"error": f"Unknown tool: {name}"})
                resp = {"jsonrpc": "2.0", "id": msg_id,
                        "result": {"content": [{"type": "text", "text": res_content}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
        except Exception as e:
            resp = {"jsonrpc": "2.0", "id": msg_id,
                    "error": {"code": -32603, "message": str(e)}}

        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
