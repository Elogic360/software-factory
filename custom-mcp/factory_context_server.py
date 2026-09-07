"""
Software Factory Context Optimizer MCP Server (factory-context-mcp).
Full stdio JSON-RPC 2.0 interactive server.
Tools: optimize_context, compress_text, estimate_tokens, cache_stats
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.context_optimizer import ContextOptimizer

TOOLS = [
    {"name": "optimize_context",
     "description": "Rank, deduplicate, compress, and pack context sources into a token budget.",
     "inputSchema": {"type": "object", "properties": {
         "query": {"type": "string"}, "sources": {"type": "array"}, "token_budget": {"type": "integer"}},
     "required": ["query", "sources"]}},
    {"name": "compress_text",
     "description": "Compress verbose text, stripping whitespace noise and truncating to token budget.",
     "inputSchema": {"type": "object", "properties": {
         "text": {"type": "string"}, "max_tokens": {"type": "integer"}},
     "required": ["text"]}},
    {"name": "estimate_tokens",
     "description": "Estimate token count of text (~4 chars/token heuristic).",
     "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}},
    {"name": "cache_stats",
     "description": "Return current deduplication cache hit/miss statistics.",
     "inputSchema": {"type": "object", "properties": {}}},
]

def main():
    optimizer = ContextOptimizer()
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
                    "serverInfo": {"name": "factory-context-mcp", "version": "2.0.0"},
                    "capabilities": {"tools": {}}}}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments", {})
                if name == "optimize_context":
                    result = optimizer.optimize_context(
                        args.get("query", ""), args.get("sources", []), args.get("token_budget", 4000))
                    res_content = json.dumps(result, indent=2)
                elif name == "compress_text":
                    compressed = optimizer.compress_text(args.get("text", ""), args.get("max_tokens"))
                    res_content = json.dumps({"compressed_text": compressed,
                                               "tokens": optimizer.estimate_tokens(compressed)}, indent=2)
                elif name == "estimate_tokens":
                    res_content = json.dumps({"estimated_tokens": optimizer.estimate_tokens(args.get("text", ""))})
                elif name == "cache_stats":
                    res_content = json.dumps({"cache_size": len(optimizer.cache),
                                               "hits": optimizer.cache_hits, "misses": optimizer.cache_misses})
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
