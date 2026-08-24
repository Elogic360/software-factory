# 2026-07-17 — Grok Build integrated with Software Factory

## Decision

Grok Build (xAI) is a first-class agent harness for Integral Market and must follow the same Software Factory protocols as Claude Code / Codex / Cursor.

## Artifacts

| Artifact | Purpose |
|----------|---------|
| `software-factory/AGENTS.md` | Universal agent bootstrap (Grok-primary entry) |
| `software-factory/AGENT_INTEGRATION.md` | Per-harness setup (includes Grok section) |
| Root `CLAUDE.md` | Project-level routing already active for all agents |
| `software-factory/CLAUDE.md` | Full orchestration OS |

## Runtime ports (canonical — `app/vite.config.ts`)

| Service | Port |
|---------|------|
| Frontend | 5173 |
| Market backend | 8000 |
| Expert backend | 8001 |
| Intelligence backend | 8002 |

Note: older docs in `software-factory/CLAUDE.md` may list Expert :8002 / IMI :8003 — **prefer vite proxy** for runtime truth.

## Verified tooling (session)

- CodeGraph CLI: installed; index ~832 files / 13k nodes
- skill_selector.py: operational
- RTK + graphify: on PATH
- Project MCP (`.mcp.json`): codegraph, context7, github, playwright, firecrawl, chrome-devtools, cloudflare, drawio, etc.
- Domain skills: 32+ under `software-factory/skills/`
- External skill packs: `software-factory/integrations/*`

## Agent protocol (non-negotiable)

1. Constitution first  
2. skill_selector → load top skills  
3. Memory check  
4. CodeGraph before structural edits  
5. SDD for features  
6. Schema ownership  
7. Validate incrementally  
8. Write durable decisions to memory  

## Ready state

**READY FOR BUILD INSTRUCTIONS** — classify → skill → SDD → implement → validate.
