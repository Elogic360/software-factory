"""
Software Factory Manufacturing Memory MCP Server (factory-memory).
Provides stdio/FastMCP interface for 12-dimensional production memory and genealogy queries.
"""

import sys
import json
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.manufacturing_memory import ManufacturingMemoryLedger

ledger = ManufacturingMemoryLedger()

def handle_rpc_call(method: str, params: dict) -> dict:
    if method == "memory.record":
        dim = params.get("dimension", "PROJECT")
        topic = params.get("topic", "")
        content = params.get("content", "")
        metadata = params.get("metadata", {})
        return ledger.record_entry(dim, topic, content, metadata)
    elif method == "memory.query":
        dim = params.get("dimension", "PROJECT")
        query = params.get("query", "")
        return {"results": ledger.query_dimension(dim, query)}
    elif method == "memory.record_genealogy":
        return ledger.record_genealogy_node(
            product=params.get("product", ""),
            release=params.get("release", "1.0.0"),
            commit_sha=params.get("commit_sha", "HEAD"),
            task_id=params.get("task_id", ""),
            agent=params.get("agent", ""),
            skill=params.get("skill", ""),
            mcp=params.get("mcp", ""),
            raw_material=params.get("raw_material", ""),
            upstream_license=params.get("upstream_license", "MIT")
        )
    elif method == "memory.trace":
        product = params.get("product", "")
        return {"genealogy": ledger.trace_genealogy(product)}
    else:
        return {"error": f"Unknown method {method}"}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        res = handle_rpc_call("memory.query", {"dimension": "PROJECT"})
        print(json.dumps(res))
    else:
        print(json.dumps({"status": "factory-memory-mcp ready", "protocol": "json-rpc-2.0"}))
