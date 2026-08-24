# Software Factory — MCP Market Integration
# Curated MCP servers from mcpmarket.com for the Integral Market platform
# Updated: 2026-06-17

## Top MCP Servers by Category

### 🏆 Top 10 (Must-Have)

| Rank | Name | Stars | Category | Use Case |
|---|---|---|---|---|
| 1 | **Superpowers** | 229k | Developer | TDD-driven software development workflow |
| 2 | **Ruflo** | 60k | Developer | Multi-agent swarm orchestration |
| 3 | **TrendRadar** | 59k | Analytics | Trending topics from 35+ platforms |
| 4 | **Context7** | 57k | Documentation | Up-to-date docs for LLMs |
| 5 | **OpenSpec** | 55k | Developer | Spec-driven development |
| 6 | **Penpot** | 50k | Design | Open-source design platform |
| 7 | **Chrome DevTools** | 44k | Browser | Browser control and debugging |
| 8 | **MindsDB** | 39k | Database | Federated data queries |
| 9 | **Playwright** | 34k | Testing | Browser automation for LLMs |
| 10 | **Next AI Draw.io** | 32k | Design | AI-powered diagram creation |

### 🔧 Developer Tools (24k+ servers)

| Name | Stars | Use Case |
|---|---|---|
| **Task Master** | 28k | Task management with Claude |
| **Serena** | 25k | Semantic code retrieval and editing |
| **FastMCP** | 23k | Create MCP servers with Python |
| **N8n** | 22k | Workflow automation nodes |
| **Beads** | 20k | Graph-based issue tracker memory |
| **Archon** | 22k | Autonomous agent building |
| **GitHub** | 31k | GitHub API automation |
| **Code2Prompt** | 7.4k | Convert codebase to LLM prompts |
| **Desktop Commander** | 6.2k | Terminal and filesystem control |

### 📊 Data Science & ML

| Name | Stars | Use Case |
|---|---|---|
| **GPT Researcher** | 28k | Deep web research with citations |
| **Cognee** | 18k | Memory layer for AI agents |
| **Graphiti** | 27k | Temporal knowledge graphs |
| **Praison AI** | 8.1k | Multi-AI agent systems |
| **LanceDB** | 11k | Embedded retrieval engine |

### 🔒 Security & Testing

| Name | Stars | Use Case |
|---|---|---|
| **Playwright** | 34k | Browser automation |
| **Kubeshark** | 12k | Kubernetes network analysis |
| **HexStrike AI** | 9.6k | Offensive cybersecurity tools |
| **MISP** | 6.4k | Cybersecurity threat intelligence |

### 📈 Analytics & Monitoring

| Name | Stars | Use Case |
|---|---|---|
| **TrendRadar** | 59k | Trending topics aggregation |
| **OpenMetadata** | 14k | Data discovery and governance |
| **Phoenix** | 10k | AI observability platform |

### 🗄️ Database Management

| Name | Stars | Use Case |
|---|---|---|
| **MindsDB** | 39k | Federated data queries |
| **Graphiti** | 27k | Temporal knowledge graphs |
| **GreptimeDB** | 6.4k | Observability database |

### 🎨 Design Tools

| Name | Stars | Use Case |
|---|---|---|
| **Penpot** | 50k | Open-source design platform |
| **Next AI Draw.io** | 32k | AI diagram creation |
| **Figma Context** | 15k | Figma layout for AI |

### 🌐 Browser Automation

| Name | Stars | Use Case |
|---|---|---|
| **Chrome DevTools** | 44k | Browser control |
| **Playwright** | 34k | Browser automation |
| **Browserbase** | 3.4k | Cloud browser control |

### 📱 Collaboration Tools

| Name | Stars | Use Case |
|---|---|---|
| **WhatsApp** | 5.8k | WhatsApp integration |
| **Klavis AI** | 5.7k | Slack/Discord MCP |
| **Excalidraw** | 4.7k | Hand-drawn diagrams |

---

## Priority Installation List

### Tier 1: Install Now (Critical for Software Factory)

1. **Context7** — Documentation lookup (already configured in .mcp.json)
2. **CodeGraph** — Code intelligence (already installed)
3. **GitHub** — PR/issue automation
4. **Playwright** — Browser automation for testing
5. **N8n** — Workflow automation

### Tier 2: Install Next (High Value)

6. **Superpowers** — TDD development workflow
7. **Task Master** — Task management
8. **OpenSpec** — Spec-driven development
9. **Graphiti** — Knowledge graphs
10. **Firecrawl** — Web scraping

### Tier 3: Install Later (Nice to Have)

11. **Penpot** — Design platform
12. **MindsDB** — Database queries
13. **Phoenix** — AI observability
14. **TrendRadar** — Trending topics
15. **WhatsApp** — Messaging integration

---

## MCP Server Installation Commands

```bash
# Context7 (already configured)
# In .mcp.json:
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}

# GitHub MCP
# Via Claude Code plugin:
/plugin marketplace add github/mcp-server-github

# Playwright
# Via Claude Code:
npx -y @playwright/mcp

# N8n
npx n8n-mcp-server

# Superpowers
npm install -g @obra/superpowers-mcp

# Task Master
npm install -g @anthropic-ai/task-master-mcp

# Firecrawl
npm install -g firecrawl-mcp

# Graphiti
pip install graphiti-core
```

---

*Last updated: 2026-06-17*
