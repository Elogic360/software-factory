# ADR: Antigravity Full Integration — 2026-09-09

**Date**: 2026-09-09  
**Author**: Antigravity (auto-generated integration checkpoint)  
**Status**: ✅ ACTIVE

---

## Context

Full integration audit and setup of Antigravity as the primary engineering agent for IntegralMarket, connected to all Software Factory memory layers, MCP servers, and skill catalogs.

---

## Integration Verification Results

### Factory Doctor (14/14 HEALTHY)
| Subsystem | Status |
|---|---|
| Registry Syntax (4 registries) | ✅ |
| Skills Catalog (68 skills) | ✅ |
| Central Memory (28 Neurons) | ✅ |
| Engineering Constitution v1.0 | ✅ |
| Context Engine & Skill Selector | ✅ |
| Capability Warehouse (15 categories) | ✅ |
| Agent Adapters (Antigravity, Claude Code, Codex, Cursor) | ✅ |
| MCP Servers (4 factory servers) | ✅ |
| Lifecycle Event Bus & Journal | ✅ |
| Scheduled Automation Engine | ✅ |

### Production Readiness: **96.7% — APPROVED**

---

## Antigravity Adapter Outputs (Written)

### `.gemini/settings.json` — MCP Servers
```json
{
  "mcpServers": {
    "codegraph": "codegraph mcp",
    "gortex": "gortex mcp",
    "context7": "npx @upstash/context7-mcp",
    "playwright": "npx @executeautomation/playwright-mcp-server",
    "github": "npx @modelcontextprotocol/server-github",
    "factory-memory-mcp": "python3 software-factory/mcp/memory_server.py",
    "factory-architecture-mcp": "python3 software-factory/mcp/architecture_mcp_server.py",
    "factory-token-optimizer-mcp": "python3 software-factory/mcp/token_optimization_server.py"
  }
}
```

### `.agents/rules/software-factory.md` — Governance Rule
- Constitution enforcement
- Central Memory cross-reference requirement
- Skill auto-discovery from `.agents/skills/`
- Context Engine routing via `skill_selector.py`

### `.agents/skills/` — Skills Symlinks
- **ECC Skills** (328+): symlinked from `software-factory/integrations/ecc/skills/`
- **IM Native Skills** (68): symlinked from `software-factory/skills/`
- Total skill surface: **328+ curated + 68 IM-native**

---

## Active Codebase State (2026-09-09)

### Git HEAD
```
9711fee9  feat(im-whatsapp): install OpenWA v0.23.4, implement WhatsAppProvider abstraction, OTP security, consent engine, and Sensei agent
```

### Active Mimocode Plan
**"Fix Metrics Display + Merge Overview/Analytics into JournalView"**

| Phase | Task | Status |
|---|---|---|
| 1 | Fix `analytics_service.py` total_pnl computation bug (line 101 stale field → computed value) | 📋 Pending |
| 2 | Merge `ExpertDashboard` (Overview) + `AnalyticsPage` into unified `JournalView.tsx` | 📋 Pending |
| 3 | Verification — backend recalculation + frontend rendering | 📋 Pending |

### Service Architecture (Constitution Art. I)
| Service | Port | DB Schema Ownership |
|---|---|---|
| Market Backend | :8000 | iam, core, academy, library, community, notifications |
| Expert Backend | :8002 | journal, copy_trading, broker_connections, imcharts |
| IMI Backend | :8003 | market_intelligence |
| Shared | — | audit, public |

### Recent Pattern Sync (2026-09-02)
Skills requiring review for touched domains:
- `backend-fastapi` (6766 files touched)
- `copytrading-engine` (165 files)
- `frontend-react` (336 files)
- `security-audit` (6601 files)
- `journal-analytics`, `mt5-integration`, `tradingview-integration`

---

## Memory Layers Active

| Layer | Path | Status |
|---|---|---|
| Factory Decisions | `software-factory/memory/decisions/` | ✅ 5 ADRs + this file |
| Factory Patterns | `software-factory/memory/patterns/` | ✅ 3 files |
| Mimocode Plans | `.mimocode/plans/` | ✅ 1 active plan |
| Mimocode Distill | `.mimocode/distill-report.md` | ✅ 2026-07-14 |
| Claude Memory | `.claude/` | ✅ Present |
| Specify Memory | `.specify/memory/` | ✅ Present |

---

## Decision

Antigravity is **fully integrated** and bootstrapped. For every new task:
1. Re-read Constitution (`software-factory/constitution/CONSTITUTION.md`)
2. Check active plans (`.mimocode/plans/`) — the Journal Metrics plan is still pending
3. Run skill router: `python3 software-factory/context-engine/skill_selector.py --query "<task>" --top 3`
4. Load relevant skills from `.agents/skills/<name>/SKILL.md`
5. Follow SDD for non-trivial features
6. Append decisions to this directory after implementation
