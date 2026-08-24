# Software Factory — Agent Integration Guide

> How every AI agent (Claude Code, Codex, Cursor, Gemini, Mercury, CodeWhale, etc.)
> should interact with the software-factory.

---

## Quick Start for Any Agent

```bash
# 1. Read the constitution
cat software-factory/constitution/CONSTITUTION.md

# 2. Select relevant skills
python3 software-factory/context-engine/skill_selector.py --query "<your task>"

# 3. Load the top skills
cat software-factory/skills/<skill-name>/SKILL.md

# 4. Check memory for prior decisions
grep -r "<topic>" software-factory/memory/decisions/

# 5. Use CodeGraph for codebase navigation
codegraph explore "<question>"

# 6. Use RTK for token-efficient commands
rtk git status
rtk git diff
rtk pytest
```

---

## Agent-Specific Setup

### Grok Build (xAI) — Primary integrated harness (2026-07)

```bash
# Entry points (auto-loaded / must-read):
#   CLAUDE.md                          — project skill routing + platform rules
#   software-factory/AGENTS.md         — universal agent bootstrap
#   software-factory/CLAUDE.md         — full orchestrator OS
#   software-factory/constitution/     — supreme law

# Bootstrap every task:
python3 software-factory/context-engine/skill_selector.py --query "<task>" --top 3
# then: Read software-factory/skills/<match>/SKILL.md

# Code intelligence
codegraph status
codegraph query "<symbol>"
codegraph context "<task description>"

# MCP: project .mcp.json (codegraph, context7, github, playwright, …)
# gstack skills: .claude/skills/ + ~/.claude/skills/ for /ship /qa /review /autoplan
# Domain skills also under .claude/skills/ (drawio, k8s, snippe, roles, …)

# Memory
#   software-factory/memory/decisions/
#   software-factory/memory/patterns/

# Ready checklist: software-factory/AGENTS.md → "Grok pre-build checklist"
```

### Claude Code

```bash
# Already configured via CLAUDE.md
# Skills auto-loaded from software-factory/skills/
# Memory auto-injected via claude-mem hooks
# CodeGraph auto-syncs on file changes
```

### Codex CLI

```bash
# Skills via AGENTS.md
# Prefer: software-factory/AGENTS.md as the single source (do not duplicate drift)

# Memory via claude-mem (if installed)
npx claude-mem install
```

### Cursor IDE

```bash
# Rules via .cursor/rules/
cp -r software-factory/skills/* .cursor/skills/

# Memory via OpenWolf
openwolf init
```

### Mercury Agent (24/7)

```bash
# Install and start
npm i -g @cosmicstack/mercury-agent
mercury up

# Load software-factory skills
mercury skills install ai-ml/prompt-engineering
mercury skills install devops/docker
```

### CodeWhale (Multi-Provider)

```bash
# Install
npm i -g codewhale

# Configure provider
codewhale auth set --provider deepseek

# Start
codewhale
```

---

## Skill Loading Protocol

Every agent should follow this protocol when starting work:

```
1. Read constitution: software-factory/constitution/CONSTITUTION.md
2. Run skill selector: python3 software-factory/context-engine/skill_selector.py --query "<task>"
3. Load top 2-3 skills from software-factory/skills/
4. Check memory: software-factory/memory/decisions/ and software-factory/memory/patterns/
5. Use CodeGraph: codegraph explore "<codebase question>"
6. Use RTK: rtk <command> for token-efficient operations
```

---

## Memory Protocol

```
Before work:
  - Check software-factory/memory/ for prior decisions
  - Check .specify/memory/ for architecture context

During work:
  - claude-mem auto-captures observations
  - OpenWolf tracks file reads and token usage

After work:
  - Write decisions to software-factory/memory/decisions/
  - Write patterns to software-factory/memory/patterns/
  - Update knowledge graph: graphify software-factory/ --update
```

---

## MCP Server Protocol

When an agent needs code intelligence:

```bash
# CodeGraph MCP (auto-configured)
codegraph explore "how does the auth flow work?"

# Gortex MCP (if installed)
gortex search "UserService"
gortex impact "AuthService"
```

---

## Security Protocol

```
Before any deployment:
  - prowler aws --compliance cis_2.0_aws
  - npx ecc-agentshield scan
  - Check software-factory/recovery/ for known issues
```

---

*Every agent that works on this project MUST follow these protocols.*
*Last updated: 2026-06-14*
