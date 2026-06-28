# Claude-mem v13.4.0 Integration Guide
## Integral Market Software-Factory Memory Layer

### Status
✅ Installed — Bun 1.3.14 + uv 0.11.15 runtime
✅ Active at: http://localhost:37702

---

## How It Works

claude-mem provides persistent semantic memory across Claude Code sessions.
The software-factory's context-engine queries it automatically at session start.

### Memory Injection Flow
```
Session Start
  → claude-mem auto-injects relevant observations (previous sessions)
  → skill_selector.py routes to domain-specific SKILL.md files
  → Constitution + architecture docs loaded
  → Agent has full context without re-asking
```

---

## What Gets Remembered

The system remembers (persisted across sessions):

### Architecture Decisions
- Schema ownership boundaries (journal/copy_trading → expert backend)
- JWT issuance rule: ONLY integral-market-backend (:8000)
- Multi-account MT5 pool: max 20 accounts, port 9100, Wine Python 3.12
- Never OAuth/register on imsensei or expert backends

### Active Services
| Service | Port | Status |
|---------|------|--------|
| integral-market-backend | 8000 | ✅ Healthy |
| integral-expert-backend | 8002 | ✅ Healthy |
| MT5 Gateway (Wine) | 9100 | ✅ Running |
| Redis | 6379 | ✅ Running |
| Celery Worker | — | ✅ Running (4 queues) |
| Frontend (Vite) | 5173 | ✅ Running |

### Key Implementation Decisions
- Blog tables: `community.blog_posts` (NOT articles — articles is the community module)
- Webinars extended with: event_type, location, whatsapp_group_url, webinar_external_participants
- Design system: Dark glassmorphism, Fira Code + Fira Sans, cyan #22D3EE primary
- Logo: `rounded-xl object-contain` with dark backing (not `rounded-full object-cover`)

---

## Usage in Context-Engine

```bash
# Query claude-mem for relevant context
# (done automatically via session start hook)

# Manual query
curl -s http://localhost:37702/api/search?q="jwt+auth" 2>/dev/null

# Add a memory observation
# Use the claude-mem MCP tool: mcp__plugin_claude-mem_mcp-search__memory_add
```

---

## Integration Points

### 1. Session Start (Automatic)
The claude-mem plugin auto-injects observations when a session starts.
See live activity: http://localhost:37702

### 2. Post-Implementation Memory Update
After any significant implementation:
```bash
# Document the decision in software-factory memory
echo "## $(date -I) — <feature>" >> software-factory/memory/decisions/<domain>.md
# claude-mem indexes this automatically on next session
```

### 3. Context Retrieval for Agents
```python
# In skill_selector.py — auto-enriches queries with memory context
# Agents receive injected context without needing to re-ask
```

---

## Memory Categories

| Category | Path | Examples |
|----------|------|---------|
| Architecture | memory/decisions/ | schema ownership, service boundaries |
| Patterns | memory/patterns/ | error recovery, retry logic |
| API Evolution | memory/api-evolution/ | endpoint changes, deprecations |
| User Preferences | (claude-mem auto) | working style, code patterns preferred |

---

*This file is read by context-engine/skill_selector.py at startup.*
*claude-mem v13.4.0 — Bun runtime — Live at http://localhost:37702*
