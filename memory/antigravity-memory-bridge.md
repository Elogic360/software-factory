# Antigravity Central Memory Bridge

## Overview
This bridge unifies Antigravity agent sessions with the Software Factory Central Memory, Mimocode execution plans, Claude-mem semantic storage, and Specify architectural logs.

## 🧠 Synchronized Memory Layers

```
                     ANTIGRAVITY AGENT
                             │
     ┌───────────────────────┼───────────────────────┐
     │                       │                       │
1. Factory Central      2. Mimocode & Plans     3. Claude & Specify
   `software-factory/`     `.mimocode/plans/`      `.claude/`
   - decisions/            - distill-report.md     - claude-mem
   - patterns/             - active plans          - .specify/memory/
   - api-evolution/
```

### 1. Software Factory Memory
- **Decisions (`software-factory/memory/decisions/`)**: Canonical architectural decisions (ADRs) regarding schema ownership, MT5 isolation, auth issuance, and microservice boundaries.
- **Patterns (`software-factory/memory/patterns/`)**: Established design patterns, data flow conventions, and runtime preload status.
- **API Evolution (`software-factory/memory/api-evolution/`)**: Versioning rules and route deprecation logs.

### 2. Mimocode & Execution Plans
- **Location**: `.mimocode/plans/` and `.mimocode/distill-report.md`.
- **Purpose**: Tracks long-running feature refactoring plans, distillation reports, and multi-file task status.

### 3. Claude & Specify Memory
- **Location**: `.claude/`, `~/.claude/history.jsonl`, and `.specify/memory/`.
- **Purpose**: Preserves session observations, cross-harness token efficiency heuristics, and C4 level model specifications.

## 🔄 Antigravity Bootstrap Sequence
Before starting any development task on Integral Market, Antigravity executes:
1. **Read Constitution**: `software-factory/constitution/CONSTITUTION.md`
2. **Inspect Memory Decisions**: `grep -r "<keyword>" software-factory/memory/decisions/`
3. **Inspect Active Patterns**: Read `software-factory/memory/patterns/`
4. **Inspect Mimocode Plans**: Check `.mimocode/plans/` for active feature roadmaps
5. **Select Skills**: Run `python3 software-factory/context-engine/skill_selector.py --query "<task>"`
