#!/usr/bin/env python3
"""
Software Factory Central Memory MCP Server.
Exposes standard Model Context Protocol (MCP) tools:
- memory_search
- memory_recall
- memory_remember
- memory_link
- memory_promote
- memory_route
"""

import json
import sys
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from core.multi_neuron_memory import CentralEngineeringMemory

def main():
    memory = CentralEngineeringMemory()

    # Simple JSON-RPC loop for stdio MCP protocol
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
                        "serverInfo": {"name": "factory-memory-mcp", "version": "2.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "memory_search",
                                "description": "Search across multi-neuron central engineering memory.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"},
                                        "project_id": {"type": "string", "default": "default"}
                                    },
                                    "required": ["query"]
                                }
                            },
                            {
                                "name": "memory_remember",
                                "description": "Store verified knowledge into target neuron.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "neuron": {"type": "string"},
                                        "topic": {"type": "string"},
                                        "content": {"type": "string"},
                                        "project_id": {"type": "string", "default": "default"}
                                    },
                                    "required": ["neuron", "topic", "content"]
                                }
                            },
                            {
                                "name": "memory_recall",
                                "description": "Recall memory record by ID or topic.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "neuron": {"type": "string"},
                                        "topic_or_id": {"type": "string"},
                                        "project_id": {"type": "string", "default": "default"}
                                    },
                                    "required": ["neuron", "topic_or_id"]
                                }
                            },
                            {
                                "name": "memory_route",
                                "description": "Route question to minimal sufficient context.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "query": {"type": "string"},
                                        "project_id": {"type": "string", "default": "default"}
                                    },
                                    "required": ["query"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "memory_search":
                    data = memory.search(args.get("query", ""), project_id=args.get("project_id", "default"))
                    res_content = json.dumps(data, indent=2)
                elif name == "memory_remember":
                    data = memory.remember(
                        neuron_type=args.get("neuron", "Factory"),
                        topic=args.get("topic", ""),
                        content=args.get("content", ""),
                        project_id=args.get("project_id", "default")
                    )
                    res_content = json.dumps(data, indent=2)
                elif name == "memory_recall":
                    data = memory.recall(
                        neuron_type=args.get("neuron", "Factory"),
                        topic_or_id=args.get("topic_or_id", ""),
                        project_id=args.get("project_id", "default")
                    )
                    res_content = json.dumps(data, indent=2)
                elif name == "memory_route":
                    data = memory.route_query(args.get("query", ""), project_id=args.get("project_id", "default"))
                    res_content = json.dumps(data, indent=2)
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
