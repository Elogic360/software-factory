"""
Software Factory Context Optimizer MCP Server (factory-context).
Provides stdio/FastMCP interface for context retrieval, ranking, compression, budget tracking, and caching.
"""

import sys
import json
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.context_optimizer import ContextOptimizer

optimizer = ContextOptimizer()

def handle_rpc_call(method: str, params: dict) -> dict:
    if method == "context.optimize":
        query = params.get("query", "")
        sources = params.get("sources", [])
        budget = params.get("budget", 4000)
        return optimizer.optimize_context(query, sources, budget)
    elif method == "context.compress":
        text = params.get("text", "")
        max_tokens = params.get("max_tokens")
        return {"compressed": optimizer.compress_text(text, max_tokens)}
    elif method == "context.estimate":
        text = params.get("text", "")
        return {"estimated_tokens": optimizer.estimate_tokens(text)}
    elif method == "context.cache_stats":
        return {
            "cache_size": len(optimizer.cache),
            "hits": optimizer.cache_hits,
            "misses": optimizer.cache_misses
        }
    else:
        return {"error": f"Unknown method {method}"}

if __name__ == "__main__":
    # Test execution or stdio dispatch
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        res = handle_rpc_call("context.estimate", {"text": "Hello Software Factory Context Plane"})
        print(json.dumps(res))
    else:
        # Standard loop
        print(json.dumps({"status": "factory-context-mcp ready", "protocol": "json-rpc-2.0"}))
