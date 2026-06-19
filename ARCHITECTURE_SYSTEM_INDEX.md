# Architecture Discovery System Index

**Version:** 1.0  
**Status:** Ready for Production  
**Last Updated:** 2026-06-03

---

## What You've Built

A **complete, agent-agnostic architecture discovery and documentation system** that works with any AI coding agent (Claude, Copilot, Gemini, Cursor, etc.) to automatically understand, map, and document any software repository.

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│  ARCHITECTURE DISCOVERY SYSTEM                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input: Repository (any code structure)                    │
│     ↓                                                        │
│  Process: 13-Phase Automated Analysis (ARCHITECTURE_...)   │
│     ↓                                                        │
│  Output: Complete Living Architecture Documentation         │
│     ↓                                                        │
│  Result: docs/architecture/* + .specify/memory/*           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Files Created

### 1. **ARCHITECTURE_DISCOVERY.md** (Master Prompt)
- **Purpose:** Core 13-phase workflow that all agents follow
- **Length:** ~2000 lines
- **Contains:**
  - PHASE 1: Repository scan & tree generation
  - PHASE 2: Architecture pattern detection
  - PHASE 3: DDD model mapping
  - PHASE 4: C4 model generation (all levels)
  - PHASE 5: Dependency analysis
  - PHASE 6: Data flow & sequences
  - PHASE 7: Infrastructure discovery
  - PHASE 8: Test coverage mapping
  - PHASE 9: Security architecture
  - PHASE 10: Performance review
  - PHASE 11: ADR generation
  - PHASE 12: Documentation creation
  - PHASE 13: Living mode setup
- **Use:** Load this into any AI agent to enable architecture discovery

### 2. **skills/architect-discovery/SKILL.md** (Executable Skill)
- **Purpose:** Packaged, reusable skill for Claude ecosystem
- **Includes:**
  - Activation commands for all agents
  - Detailed phase workflows
  - Output examples & templates
  - Success criteria & checklists
  - Anti-pattern warnings
- **Use:** Reference in .claude/skills or load directly

### 3. **AGENT_INTEGRATION.md** (Multi-Agent Setup)
- **Purpose:** Integration instructions for 8+ different agents
- **Covers:**
  - Claude Code / Claude API
  - GitHub Copilot (VSCode, GitHub.com)
  - Cursor
  - Windsurf
  - Google Gemini (Colab, Notebooks)
  - Kimi (Ant AI)
  - Qwen (Alibaba)
  - Generic agent pattern
- **Includes:** Code examples, configuration templates
- **Use:** Choose your agent(s), follow setup instructions

### 4. **MEMORY_ARCHITECTURE.md** (Cross-Session State)
- **Purpose:** Enable agents to remember discoveries across sessions
- **Structure:**
  - `.specify/memory/architecture/` (discovered patterns)
  - `.specify/memory/agent-logs/` (per-agent records)
  - `.specify/memory/cache/` (performance optimization)
- **Files:**
  - `discovered-patterns.md` - What architecture you use
  - `bounded-contexts.md` - DDD model
  - `data-flows.md` - Request sequences
  - `decisions.md` - ADRs & rationale
  - `violations.md` - Architecture issues
  - `c4-definitions.json` - Cache for speed
  - `dependency-graph.json` - Dependency matrix
- **Use:** Automatically populated; enables cross-session awareness

### 5. **ARCHITECTURE_QUICKSTART.md** (Getting Started)
- **Purpose:** 15-minute guide to first discovery run
- **Steps:**
  1. Prerequisites (2 min)
  2. Load architecture discovery (1 min)
  3. Run quick discovery (5 min)
  4. Review generated docs (5 min)
  5. Set up living architecture (2 min)
  6. Integrate with team
- **Commands:** Quick reference for all major operations
- **Troubleshooting:** Common issues & solutions
- **Use:** Start here for first-time users

### 6. **This File: ARCHITECTURE_SYSTEM_INDEX.md**
- **Purpose:** Map the entire system, show connections
- **Contents:**
  - File inventory
  - Workflow diagram
  - Integration checklist
  - Success criteria

---

## File Relationships

```
ARCHITECTURE_QUICKSTART.md ← Start here (Day 1)
    ↓
    ├─ ARCHITECTURE_DISCOVERY.md (Load this)
    │   ├─ skills/architect-discovery/SKILL.md
    │   └─ Memory system (below)
    │
    └─ AGENT_INTEGRATION.md (Pick your agent)
        ├─ Claude Code setup
        ├─ Copilot setup
        ├─ Cursor setup
        ├─ Gemini setup
        └─ Other agents...

MEMORY_ARCHITECTURE.md (Persistent state)
    └─ .specify/memory/architecture/
        ├─ discovered-patterns.md
        ├─ bounded-contexts.md
        ├─ decisions.md
        ├─ violations.md
        └─ ...
```

---

## Output Artifacts

Every discovery run generates:

```
docs/architecture/                     (Committed to git)
├── REPOSITORY_MAP.md                  # Full directory tree
├── ARCHITECTURE_ANALYSIS.md           # Pattern detection
├── DDD_MODEL.md                       # Contexts & aggregates
├── C4_CONTEXT.md                      # System level
├── C4_CONTAINER.md                    # Services level
├── C4_COMPONENT.md                    # Component level
├── C4_CODE.md                         # UML classes
├── DEPENDENCY_ANALYSIS.md             # Coupling analysis
├── DATA_FLOW.md                       # Sequences
├── DEPLOYMENT.md                      # Infrastructure
├── TEST_COVERAGE.md                   # Coverage gaps
├── SECURITY.md                        # Auth & encryption
├── PERFORMANCE.md                     # Hotspots
├── VIOLATIONS.md                      # Issues to fix
├── adr/                               # Architecture decisions
│   └── ADR-*.md
└── diagrams/                          # Visual assets
    ├── c4-context.puml / .mmd
    ├── c4-container.puml / .mmd
    ├── uml-*.puml / .mmd
    └── dependency-graph.mmd

.specify/memory/                       (Cross-session state)
├── architecture/
│   ├── discovered-patterns.md
│   ├── bounded-contexts.md
│   ├── decisions.md
│   ├── violations.md
│   └── cache/
└── agent-logs/
    ├── claude-2026-06.md
    ├── copilot-2026-06.md
    └── ...
```

---

## Workflow Diagram

```
Day 1: Initial Discovery
├─ Run ARCHITECTURE_QUICKSTART.md (15 min)
├─ Choose agent from AGENT_INTEGRATION.md
├─ Load ARCHITECTURE_DISCOVERY.md
├─ Execute /architect-discovery --full
└─ Review docs/architecture/ (15 min)

Week 1: Team Onboarding
├─ Share REPOSITORY_MAP.md with team
├─ Share C4 diagrams in Confluence/Slack
├─ Use for onboarding docs
└─ Create first ADRs

Ongoing: Living Architecture
├─ Enable watch mode (/architect-discovery --watch .)
├─ Integrate into CI/CD (.github/workflows/architecture.yml)
├─ Monthly: Full re-discovery
├─ Quarterly: Architecture review
└─ Update ADRs after major changes
```

---

## Integration Checklist

### Phase 0: Setup (Day 0)
- [ ] Clone or open your repository
- [ ] Read ARCHITECTURE_QUICKSTART.md
- [ ] Choose primary agent (Claude, Copilot, Cursor, etc.)

### Phase 1: First Discovery (Day 1)
- [ ] Follow ARCHITECTURE_QUICKSTART.md steps 1-5
- [ ] Run discovery
- [ ] Review generated documentation
- [ ] Note any major findings

### Phase 2: Team Onboarding (Week 1)
- [ ] Share REPOSITORY_MAP.md with team
- [ ] Share C4 diagrams
- [ ] Discuss findings in team meeting
- [ ] Create initial ADRs if needed

### Phase 3: Continuous Integration (Week 2)
- [ ] Set up living mode
- [ ] Add to CI/CD pipeline
- [ ] Configure auto-updates on commits
- [ ] Set up monitoring for violations

### Phase 4: Operational (Ongoing)
- [ ] Monthly: Full discovery re-run
- [ ] Quarterly: Architecture review
- [ ] On major refactors: Update ADRs
- [ ] On violations: Create spike tickets

---

## Success Metrics

✅ **Knowledge**
- New team members understand architecture in 1 hour (vs 1 week)
- Architecture patterns clearly identified
- Bounded contexts mapped
- Data flows documented

✅ **Quality**
- Architectural violations detected automatically
- Cyclic dependencies identified
- Tight coupling visible
- Test coverage gaps known

✅ **Governance**
- All decisions recorded in ADRs
- Architecture changes tracked
- Living documentation in sync with code
- Compliance with enterprise patterns

✅ **Agility**
- Refactoring decisions informed by actual architecture
- New features planned with context awareness
- Cross-team impacts visible
- Technology choices justified

---

## Advanced Features

### Multi-Agent Coordination
Run discovery with multiple agents and merge results:
```bash
# Agent 1: Full discovery
claude /architect-discovery --full

# Agent 2: Validate & enhance
copilot /architecture-discovery --validate

# Result: Richer, multi-perspective analysis
```

### Custom Architecture Rules
Define your org's architecture constraints:
```
.specify/architecture-rules.yaml
├── no-cyclic-dependencies: true
├── no-domain-db-imports: true
├── require-tests-per-layer: true
└── ...
```

### Integration with SDD Pipeline
```bash
# When creating specs, check architecture impact
/architect-discovery --check-impact @spec.md

# Flag affected contexts and aggregates
# Recommend architecture changes
# Create ADR if needed
```

### Living Documentation Modes

1. **Watch Mode** (every 60 seconds)
   ```bash
   /architect-discovery --watch . --interval 60
   ```

2. **CI/CD Integration** (every commit)
   ```yaml
   # .github/workflows/architecture.yml
   on: [push]
   ```

3. **Scheduled** (daily)
   ```bash
   cron: '0 9 * * *'  # Daily at 9 AM
   ```

---

## Common Scenarios

### Scenario 1: New Team Member Joins
```
1. New person runs: /architect-discovery --quick
2. Reads: docs/architecture/REPOSITORY_MAP.md (15 min)
3. Reviews: docs/architecture/C4_CONTAINER.md (15 min)
4. Discusses: docs/architecture/VIOLATIONS.md (15 min)
5. Onboarded in 1 hour instead of 1 week ✓
```

### Scenario 2: Planning Major Refactor
```
1. Team runs: /architect-discovery --full
2. Identifies: Current architecture in ARCHITECTURE_ANALYSIS.md
3. Finds: Violations in VIOLATIONS.md
4. Creates: New ADR for refactor direction
5. Proceeds with full context ✓
```

### Scenario 3: Cross-Team Integration
```
1. Team A discovers: Their architecture
2. Team B discovers: Their architecture
3. Compare: Dependency graphs
4. Resolve: Service boundaries and contracts
5. Design: Clean integration points ✓
```

### Scenario 4: Security Audit
```
1. Run: /architect-discovery --full
2. Review: docs/architecture/SECURITY.md
3. Identify: Encryption gaps, auth flows
4. Create: Security ADRs
5. Track: Remediation in violations.md ✓
```

---

## Key Principles

### 1. Agent-Agnostic
Works with Claude, Copilot, Gemini, Cursor, or any AI that can read prompts.

### 2. Automated Yet Flexible
Phases 1-13 are automatic, but you can focus on subsets (--focus ddd, --focus security).

### 3. Living Documentation
Not a one-time report. Stays in sync with code via watch mode & CI/CD.

### 4. Memory Enabled
Agents remember prior discoveries. Cross-session and cross-agent awareness.

### 5. Enterprise-Ready
Supports C4 Model, DDD, Microservices, Event-Driven, CQRS, and more.

---

## Troubleshooting Decision Tree

```
Issue: Can't run discovery?
  ├─ No .git directory → git init
  ├─ Wrong agent → Switch via AGENT_INTEGRATION.md
  ├─ Missing files → Clone software-factory repo
  └─ PlantUML not found → brew install plantuml

Issue: Documentation looks wrong?
  ├─ Old cache → Delete .specify/cache/
  ├─ Changed code → Re-run discovery
  ├─ Wrong output → Check VIOLATIONS.md
  └─ Pattern misdetected → Use --focus flag

Issue: Living mode not working?
  ├─ Watch not enabled → /architect-discovery --watch .
  ├─ CI/CD not set up → Add .github/workflows/architecture.yml
  ├─ Memory stale → Delete .specify/memory/ and re-run
  └─ File permissions → chmod +x software-factory/scripts/*

Issue: Violations not showing?
  ├─ Not running full discovery → Use --full flag
  ├─ Violations.md not created → Check output
  ├─ Cache interference → Clear cache and re-run
  └─ Pattern not recognized → Verify code structure
```

---

## What's Included

| Component | File | Purpose | Size |
|-----------|------|---------|------|
| Master Prompt | ARCHITECTURE_DISCOVERY.md | Core 13-phase workflow | ~2000 lines |
| Skill | skills/architect-discovery/SKILL.md | Packaged skill | ~1500 lines |
| Integration | AGENT_INTEGRATION.md | Multi-agent setup | ~1000 lines |
| Memory | MEMORY_ARCHITECTURE.md | Cross-session state | ~1000 lines |
| Quick Start | ARCHITECTURE_QUICKSTART.md | Getting started | ~400 lines |
| Index | This file | System overview | ~500 lines |
| **Total** | | | **~6400 lines** |

---

## What's NOT Included (By Design)

❌ **Vendor Lock-in**
- Works with any agent, not specific to Claude

❌ **Rigid Templates**
- Adapts to your architecture, not vice versa

❌ **Over-Automation**
- Phases 1-12 are automatic, Phase 13 (living) is optional

❌ **Hidden Magic**
- All prompts are readable, modifiable, understandable

---

## Next Steps

### For You (Day 0-1)
1. ✅ **Understand the system** (read this file) — 10 min
2. ✅ **Choose your agent** (read AGENT_INTEGRATION.md) — 10 min
3. ✅ **Run first discovery** (follow ARCHITECTURE_QUICKSTART.md) — 15 min
4. ✅ **Review output** (open docs/architecture/) — 15 min

### For Your Team (Week 1)
1. **Share REPOSITORY_MAP.md** - Help everyone understand structure
2. **Share C4 diagrams** - Visual representation
3. **Discuss VIOLATIONS.md** - What needs fixing
4. **Create ADRs** - Document architectural decisions

### For Your Organization (Week 2+)
1. **Integrate into CI/CD** - Auto-update on every commit
2. **Use for onboarding** - New hires read docs/architecture/ first
3. **Use for planning** - Check architecture before major changes
4. **Use for compliance** - Audit architecture against rules

---

## Support & Resources

- **Quick Start:** ARCHITECTURE_QUICKSTART.md
- **Full Details:** ARCHITECTURE_DISCOVERY.md
- **Agent Setup:** AGENT_INTEGRATION.md
- **Memory System:** MEMORY_ARCHITECTURE.md
- **Examples:** software-factory/skills/architect-discovery/examples/
- **Troubleshooting:** Grep ARCHITECTURE_DISCOVERY.md for your issue

---

## License & Attribution

This system is part of the **Software Factory** at Integral Market.

Built as an enterprise-grade, AI-powered architecture discovery system.

---

**You're now ready to build a reusable, autonomous architecture discovery system.** 🚀

Start with: `ARCHITECTURE_QUICKSTART.md` → 15 minutes to your first architecture map

