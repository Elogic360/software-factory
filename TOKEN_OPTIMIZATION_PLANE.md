# 🧠 Context & Token Optimization Plane

## Architecture
The Software Factory operates an active token and context optimization plane (`core/context_optimizer.py` and `custom-mcp/factory_context_server.py`) to reduce LLM token overhead, avoid repetitive trial-and-error, and enforce strict token budgets.

```text
Agent
  │
  ▼
Context Broker (Task + Architecture + Memory + Skills + MCP)
  │
  ▼
Context Optimizer
  ├── Relevance Ranking (Keyword & Semantic overlap)
  ├── Exact & Fuzzy Deduplication (SHA-256 block hashing)
  ├── Semantic Compression & Whitespace Normalization
  ├── In-Memory LRU Context Caching
  └── Hard Token Budget Enforcement
  │
  ▼
Optimized Context Payload -> LLM Execution
```

## Tracked Metrics
- `tokens_before`: Raw input token volume across all sources.
- `tokens_after`: Final token volume delivered to LLM.
- `compression_ratio`: Ratio of compressed tokens to raw tokens.
- `cache_hit_rate`: Frequency of cached context blocks reused.
- `tool_output_reduction`: Percentage of redundant tool output eliminated.
- `cost_saved_usd`: Estimated monetary savings in USD.
