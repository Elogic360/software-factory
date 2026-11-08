# Central Memory Hub — Multi-Agent & Multi-Harness Sync

| Harness | Primary Memory Path | Bridge File | Sync Protocol |
| :--- | :--- | :--- | :--- |
| **Antigravity** | `<brain>/` & `.agents/` | `antigravity-memory-bridge.md` | Auto-discovers `.agents/skills`, reads `memory/decisions/` & `memory/patterns/` |
| **Claude Code** | `~/.claude/` & `.claude/` | `claude-mem-bridge.md` | Auto-injects observations via claude-mem hook & `CLAUDE.md` |
| **Mimocode** | `.mimocode/plans/` | `distill-report.md` | Persists execution plans and step-by-step feature status |
| **Specify / SDD** | `.specify/memory/` | `constitution.md` | Maintains C4 architecture models and boundary checks |
| **Codex / Cursor** | `.cursor/rules/`, `AGENTS.md` | `AGENT_INTEGRATION.md` | Reads single-source governance files |

---

## Active Memory Ledger (2026-11)

### Key Architectural Decisions (ADRs)
- [`ADR-010-mt5-gateway-ctrader-journal-analytics.md`](decisions/ADR-010-mt5-gateway-ctrader-journal-analytics.md): MT5 Multi-Node Gateway, cTrader Integration, Broker Brand Identity, imJournal 2-Decimal Analytics & R2 Streaming.
- [`ADR-009-mcp-memory-context-token-candidates.md`](decisions/ADR-009-mcp-memory-context-token-candidates.md): MCP Memory, Context, and Token Optimization Canonical Stack.
- [`2026-09-antigravity-integration.md`](decisions/2026-09-antigravity-integration.md): Antigravity Harness Integration & 269 Skills Symlinking.

### Active Design Patterns
- [`2026-11.md`](patterns/2026-11.md): Microservice Boundary, Local Runtime Topology, Multi-Broker Capability Normalization, 2-Decimal Precision Invariants, and R2 Contextual Fallback Generators.
- [`2026-09.md`](patterns/2026-09.md): Academy R2 Cover Art Synchronization & Orphan Repair.

### Central 28-Neuron Engine
- Managed via `software-factory/mcp/memory_server.py` and `software-factory/custom-mcp/factory_memory_server.py`.
- Verified live stdio JSON-RPC 2.0 protocol available to all autonomous agents.

