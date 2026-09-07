# Central Memory Hub — Multi-Agent & Multi-Harness Sync

| Harness | Primary Memory Path | Bridge File | Sync Protocol |
| :--- | :--- | :--- | :--- |
| **Antigravity** | `<brain>/` & `.agents/` | `antigravity-memory-bridge.md` | Auto-discovers `.agents/skills`, reads `memory/decisions/` & `memory/patterns/` |
| **Claude Code** | `~/.claude/` & `.claude/` | `claude-mem-bridge.md` | Auto-injects observations via claude-mem hook & `CLAUDE.md` |
| **Mimocode** | `.mimocode/plans/` | `distill-report.md` | Persists execution plans and step-by-step feature status |
| **Specify / SDD** | `.specify/memory/` | `constitution.md` | Maintains C4 architecture models and boundary checks |
| **Codex / Cursor** | `.cursor/rules/`, `AGENTS.md` | `AGENT_INTEGRATION.md` | Reads single-source governance files |
