#!/usr/bin/env python3
"""
Software Factory Token Optimization MCP Server.
Exposes standard Model Context Protocol (MCP) tools:
- optimize_context
- compress_tool_output
- measure_token_savings
"""

import json
import sys
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent
if str(SF_ROOT) not in sys.path:
    sys.path.insert(0, str(SF_ROOT))

from core.context_optimizer import ContextOptimizer

def main():
    optimizer = ContextOptimizer()

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
                        "serverInfo": {"name": "factory-token-optimizer-mcp", "version": "2.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "optimize_context",
                                "description": "Deduplicate and compress context to fit token budget.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "text": {"type": "string"},
                                        "max_tokens": {"type": "integer", "default": 2000}
                                    },
                                    "required": ["text"]
                                }
                            },
                            {
                                "name": "compress_tool_output",
                                "description": "Compress verbose terminal and tool outputs (logs, stacktraces).",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "tool_output": {"type": "string"},
                                        "max_lines": {"type": "integer", "default": 25}
                                    },
                                    "required": ["tool_output"]
                                }
                            },
                            {
                                "name": "measure_token_savings",
                                "description": "Calculate token reduction and cost savings metrics.",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "original_text": {"type": "string"},
                                        "optimized_text": {"type": "string"}
                                    },
                                    "required": ["original_text", "optimized_text"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "optimize_context":
                    txt = args.get("text", "")
                    max_t = args.get("max_tokens", 2000)
                    opt = optimizer.compress_text(txt, max_tokens=max_t)
                    tokens_before = optimizer.estimate_tokens(txt)
                    tokens_after = optimizer.estimate_tokens(opt)
                    m = optimizer.calculate_metrics(tokens_before=tokens_before, tokens_after=tokens_after)
                    res_content = json.dumps({
                        "optimized_text": opt,
                        "tokens_before": m.tokens_before,
                        "tokens_after": m.tokens_after,
                        "tokens_saved": m.tokens_before - m.tokens_after,
                        "compression_ratio": f"{(1.0 - m.compression_ratio) * 100:.1f}% reduction"
                    }, indent=2)
                elif name == "compress_tool_output":
                    out = args.get("tool_output", "")
                    max_l = args.get("max_lines", 25)
                    lines = out.splitlines()
                    if len(lines) > max_l:
                        half = max_l // 2
                        omitted = len(lines) - max_l
                        comp_lines = lines[:half] + [f"... [{omitted} lines omitted] ..."] + lines[-half:]
                    else:
                        comp_lines = lines
                    comp = "\n".join(comp_lines)
                    res_content = json.dumps({
                        "compressed_output": comp,
                        "lines_before": len(lines),
                        "lines_after": len(comp_lines)
                    }, indent=2)
                elif name == "measure_token_savings":
                    t1 = optimizer.estimate_tokens(args.get("original_text", ""))
                    t2 = optimizer.estimate_tokens(args.get("optimized_text", ""))
                    m = optimizer.calculate_metrics(tokens_before=t1, tokens_after=t2)
                    res_content = json.dumps({
                        "tokens_before": m.tokens_before,
                        "tokens_after": m.tokens_after,
                        "saved_tokens": m.tokens_before - m.tokens_after,
                        "cost_saved_usd": m.cost_saved_usd
                    }, indent=2)
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
