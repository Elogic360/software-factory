#!/usr/bin/env python3
"""
Software Factory Architecture-as-Code MCP Server.
Exposes standard Model Context Protocol (MCP) tools:
- generate_c4_model
- render_mermaid_diagram
- render_drawio_diagram
- detect_architecture_drift
"""

import json
import sys
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from core.architecture_engine import ArchitectureEngine

def main():
    arch_engine = ArchitectureEngine()

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            params = req.get("params", {})

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "factory-architecture-mcp", "version": "2.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "generate_c4_model",
                                "description": "Generate C1-C4 architecture model representation.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "product_name": {"type": "string"},
                                        "containers": {"type": "array"},
                                        "components": {"type": "array"}
                                    },
                                    "required": ["product_name"]
                                }
                            },
                            {
                                "name": "render_mermaid_diagram",
                                "description": "Render Mermaid C4 diagram from architecture model.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "c4_model": {"type": "object"}
                                    },
                                    "required": ["c4_model"]
                                }
                            },
                            {
                                "name": "render_drawio_diagram",
                                "description": "Render Draw.io XML (mxGraphModel) from architecture model.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "c4_model": {"type": "object"}
                                    },
                                    "required": ["c4_model"]
                                }
                            },
                            {
                                "name": "detect_architecture_drift",
                                "description": "Compare expected architecture graph against detected live endpoints.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "expected_graph": {"type": "object"},
                                        "live_endpoints": {"type": "array"}
                                    },
                                    "required": ["expected_graph", "live_endpoints"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "generate_c4_model":
                    model = arch_engine.generate_c4_model(
                        product_name=args.get("product_name", "System"),
                        containers=args.get("containers", []),
                        components=args.get("components", [])
                    )
                    res_content = json.dumps(model, indent=2)
                elif name == "render_mermaid_diagram":
                    res_content = arch_engine.generate_mermaid_c4(args.get("c4_model", {}))
                elif name == "render_drawio_diagram":
                    res_content = arch_engine.generate_drawio_architecture(args.get("c4_model", {}))
                elif name == "detect_architecture_drift":
                    drift = arch_engine.detect_drift(args.get("expected_graph", {}), args.get("live_endpoints", []))
                    res_content = json.dumps(drift, indent=2)
                else:
                    res_content = f"Unknown tool: {name}"

                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": res_content}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
