# Software Factory — MCP Market Deep Integration

> Complete mapping of MCP servers to software-factory skills with installation, configuration, and use cases.

---

## MCP-to-Skill Mapping Matrix

| MCP Server | Stars | Primary Skill | Secondary Skills | Use Case |
|---|---|---|---|---|
| **Superpowers** | 230k | software-developer | testing-e2e, testing-load | TDD workflow, design refinement |
| **Context7** | 58k | context-engineering | prompt-engineering | Live documentation lookup |
| **Task Master** | 28k | software-product-architect | change-detective | Task management, PRD parsing |
| **OpenSpec** | 55k | software-product-architect | architect-principal | Spec-driven development |
| **GitHub** | 31k | change-detective | devops-engineer | PR/issue automation |
| **Playwright** | 34k | testing-e2e | software-product-tester | Browser automation |
| **Firecrawl** | 6.6k | context-engineering | quant-research | Web scraping for data |
| **N8n** | 22k | event-driven-architecture | microservices | Workflow automation |
| **Chrome DevTools** | 44k | interactive-dev | frontend-react | Browser debugging |
| **Graphiti** | 27k | context-engineering | ai-optimization | Knowledge graphs |
| **MindsDB** | 39k | quant-research | ai-optimization | Data federation |
| **TrendRadar** | 59k | market-intelligence | prompt-engineering | Trending topics |
| **FastAPI MCP** | 12k | backend-fastapi | microservices | FastAPI endpoint exposure |
| **Penpot** | 50k | ui-ux-premium | frontend-react | Design platform |
| **Phoenix** | 10k | observability | ai-optimization | AI observability |

---

## Installation Commands

### Tier 1: Critical (Install Now)

```bash
# 1. Context7 — Documentation Lookup
npx -y @upstash/context7-mcp@latest

# 2. GitHub — PR/Issue Automation
# Already configured in .mcp.json

# 3. Playwright — Browser Automation
npx -y @anthropic-ai/mcp-server-playwright

# 4. Firecrawl — Web Scraping
npm install -g @mendableai/firecrawl-mcp

# 5. N8n — Workflow Automation
npm install -g n8n-mcp-server
```

### Tier 2: High Value (Install Next)

```bash
# 6. Superpowers — TDD Workflow
npm install -g @obra/superpowers-mcp

# 7. Task Master — Task Management
npm install -g task-master-ai

# 8. OpenSpec — Spec Development
npm install -g @fission-ai/openspec-mcp

# 9. Graphiti — Knowledge Graphs
pip install graphiti-core

# 10. FastAPI MCP
pip install fastapi-mcp
```

---

## Skill Integration Details

### software-developer + Superpowers

```yaml
skill: software-developer
mcp: superpowers
workflow:
  1. Design refinement (interactive)
  2. Specification generation
  3. Implementation planning (TDD)
  4. Subagent-driven development
  5. Automated code review
  6. Quality gates
trigger: "implement a new feature"
```

### context-engineering + Context7

```yaml
skill: context-engineering
mcp: context7
workflow:
  1. Add "use context7" to prompt
  2. Fetch version-specific docs
  3. Get accurate code examples
  4. Prevent hallucinated APIs
trigger: "need up-to-date documentation"
```

### software-product-architect + Task Master + OpenSpec

```yaml
skill: software-product-architect
mcp: [task-master, openspec]
workflow:
  1. Parse PRD into tasks (Task Master)
  2. Generate spec (OpenSpec)
  3. Create implementation plan
  4. Assign to subagents
trigger: "plan a new feature from PRD"
```

### change-detective + GitHub

```yaml
skill: change-detective
mcp: github
workflow:
  1. Detect code changes
  2. Create GitHub issue
  3. Open pull request
  4. Run CI checks
trigger: "detect and document changes"
```

### testing-e2e + Playwright

```yaml
skill: testing-e2e
mcp: playwright
workflow:
  1. Write E2E tests
  2. Run browser automation
  3. Capture screenshots
  4. Generate test reports
trigger: "run end-to-end tests"
```

---

## Updated MCP Configuration

```json
{
  "mcpServers": {
    "codegraph": {
      "command": "codegraph",
      "args": ["serve"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-playwright"]
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendableai/firecrawl-mcp"],
      "env": { "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}" }
    },
    "fastapi": {
      "command": "python3",
      "args": ["-m", "fastapi_mcp"],
      "env": {}
    },
    "prowler": {
      "command": "python3",
      "args": ["-m", "prowler.mcp_server"],
      "env": {
        "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
        "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}"
      }
    },
    "linux-mcp": {
      "command": "python3",
      "args": ["-m", "linux_mcp_server"]
    }
  }
}
```

---

*Last updated: 2026-06-17*
