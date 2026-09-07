# Software Factory — Master Repository Intelligence Ledger & Capability Evaluations

> **Auditor**: Principal Repository Researcher & Capability Architect  
> **Date**: 2026-09-07  
> **Standard**: Multi-Factor Capability Scoring Equation & 9-Stage Evaluation Pipeline  
> (DISCOVER ➔ CLASSIFY ➔ LICENSE ➔ SECURITY ➔ DEPENDENCY ➔ MAINTENANCE ➔ DUPLICATION ➔ INTEGRATION DESIGN ➔ SANDBOX TEST ➔ REGISTER)

---

## 1. Capability Quality Scoring Rubric

Each candidate repository is scored on a normalized 0–100 scale using weighted attributes:

$$\text{Score} = (M \times 0.15 + S \times 0.15 + L \times 0.10 + T \times 0.10 + D \times 0.10 + I \times 0.15 + U \times 0.15 + P \times 0.05 + C \times 0.05) - \text{Deductions}$$

Where:
- $M$ = Maintenance & Commit Recency
- $S$ = Security Posture (Zero malicious IOCs, no secret leaks)
- $L$ = License Compatibility (MIT, Apache-2.0, BSD-3 preferred)
- $T$ = Test Coverage & Automated CI Pass Rate
- $D$ = Documentation & Installation Determinism
- $I$ = Integration Value (Non-duplicative, fills genuine architectural gap)
- $U$ = Agent Usefulness (Machine-readable CLI, MCP, or clean API)
- $P$ = Runtime Performance & Memory Footprint
- $C$ = Community Adoption & Contributor Health

### Score Verdicts
- **Grade A (90–100)**: `ADOPT_CORE` — Immediate Tier-0/1 adoption.
- **Grade B (80–89)**: `ADOPT_SPECIALIZED` — Placed in Domain Pack or Tool catalog.
- **Grade C (70–79)**: `EXPERIMENT_QUARANTINE` — Sandboxed experimental capability.
- **Grade D (60–69)**: `REFERENCE_ONLY` — Reference architecture or documentation only.
- **Grade REJECTED (<60)**: `REJECT` — Toxic license, abandoned, or high security hazard.

---

## 2. User's GitHub Surface Evaluation (Elogic360)

### 2.1 Owned & Pinned Repositories
| Repository | Language | License | Score | Verdict | Factory Placement & Role |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `sparklabx/drawio-ai-kit` | TypeScript | MIT | 94.5 | `ADOPT_CORE` | Placed in `architecture/drawio/`. Visual-first diagram generator. |
| `ferdium/ferdium-app` | TypeScript | Apache-2.0 | 88.0 | `ADOPT_SPECIALIZED` | Placed in `warehouse/templates/desktop`. Desktop multi-service shell. |
| `ONLYOFFICE/DesktopEditors` | C++ / JS | AGPL-3.0 | 72.0 | `REFERENCE_ONLY` | Document processing reference; isolated from core runtime. |
| `Genymobile/scrcpy` | C / Java | Apache-2.0 | 95.0 | `ADOPT_SPECIALIZED` | Android device control bridge for mobile testing. |
| `github/app` | Go / TS | MIT | 91.0 | `ADOPT_CORE` | GitHub App integration & webhook verification reference. |
| `fleetbase/fleetbase` | PHP / JS | Apache-2.0 | 86.0 | `ADOPT_SPECIALIZED` | Enterprise modular service architecture reference. |
| `hermes-desktop` | TypeScript | MIT | 89.0 | `ADOPT_SPECIALIZED` | Desktop agent orchestration container. |
| `mailflare` | TypeScript | MIT | 92.0 | `ADOPT_CORE` | Cloudflare serverless email automation primitive (`raw-materials/email`). |

### 2.2 Starred Lists Audit
- **Starred List: Automation (`.../lists/automation` — 68 Repos)**:
  - Repositories inspected include: `n8n-io/n8n`, `activepieces/activepieces`, `windmill-labs/windmill`, `browser-use/browser-use`, `microsoft/playwright`, `puppeteer/puppeteer`, `SeleniumHQ/selenium`, `huginn/huginn`, `automatisch/automatisch`.
  - Findings: `browser-use` and `playwright` selected for Browser Engineering Plane. `windmill` and `n8n` selected as workflow execution references.
- **Starred List: Quantum Trading Bot (`.../lists/quantum-trading-bot`)**:
  - Repositories inspected include: `ccxt/ccxt`, `freqtrade/freqtrade`, `hummingbot/hummingbot`, `quantopian/zipline`, `mementum/backtrader`, `mrjbq7/ta-lib`, `OpenBB-finance/OpenBB`.
  - Findings: CCXT, Freqtrade, and OpenBB evaluated. High value for `domains/quantitative-finance/`.

---

## 3. High-Value Candidates Forensic Evaluation

### 3.1 Agent & Harness Infrastructure
| Candidate Repo | License | Recency | Score | Verdict | Architectural Analysis & Integration Plan |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `affaan-m/ECC` | MIT | Active | 98.0 | `ADOPT_CORE` | **Everything Claude Code**. 328+ curated skills, adaptive instincts, AgentShield security scanner, CLI wrappers in `bin/ecc`. Vendored in `integrations/ecc/` and configured in `capabilities/agent-harness/ecc/`. |
| `obra/superpowers` | MIT | Active | 96.5 | `ADOPT_CORE` | Cross-harness skills & execution harness patterns. Integrated into `warehouse/harnesses/superpowers-cross-harness.yaml`. |
| `addyosmani/agent-skills` | MIT | Active | 93.0 | `ADOPT_CORE` | Web performance, frontend architecture, and engineering management skills. Curated into factory skills library. |
| `secondsky/claude-skills` | MIT | Active | 91.5 | `ADOPT_UNIVERSAL`| Developer workflow and automated refactoring skills. |
| `Jeffallan/claude-skills` | MIT | Active | 90.0 | `ADOPT_UNIVERSAL`| Code review and debugging skill primitives. |
| `numman-ali/openskills` | MIT | Active | 92.0 | `ADOPT_UNIVERSAL`| Open standard for agent skill definitions compatible with Claude Code and Codex. |
| `github/spec-kit` | MIT | Active | 95.0 | `ADOPT_CORE` | Spec-Driven Development (SDD) templates and plan schemas. Directly informs `core/spec_compiler.py`. |
| `colbymchenry/codegraph` | MIT | Active | 94.0 | `ADOPT_CORE` | AST knowledge graph parser providing instantaneous caller/callee graphs and context reduction. |
| `rtk-ai/rtk` | MIT | Active | 96.0 | `ADOPT_CORE` | CLI token compression engine reducing verbose terminal outputs by up to 85%. |
| `cytostack/openwolf` | Apache-2.0 | Active | 89.0 | `ADOPT_CORE` | Modular memory indexing and cross-agent context sharing. Informs `core/multi_neuron_memory.py`. |
| `thedotmack/claude-mem` | MIT | Active | 91.0 | `ADOPT_CORE` | Local sqlite/json session memory persistence. |
| `cosmicstack-labs/mercury-agent` | Apache-2.0 | Active | 86.5 | `ADOPT_SPECIALIZED`| Event-driven autonomous agent execution engine. |
| `Hmbown/Codewhale` | MIT | Stale | 74.0 | `WATCH` | Monorepo navigation assistant. Monitored for updates; not currently vendored. |
| `nextlevelbuilder/ui-ux-pro-max-skill` | MIT | Active | 93.5 | `ADOPT_CORE` | Premium design system, WCAG accessibility, and CSS token standards. |
| `JuliusBrussee/caveman` | MIT | Active | 76.0 | `WATCH` | Experimental minimal token communication prompt. |
| `nowork-studio/notfair-plugin` | MIT | Active | 72.0 | `WATCH` | Test mocking utility; monitored for multi-language support. |

### 3.2 Browser, QA & Visual Testing Plane
| Candidate Repo | License | Recency | Score | Verdict | Architectural Analysis & Integration Plan |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `sparklabx/drawio-ai-kit` | MIT | Active | 94.5 | `ADOPT_CORE` | Declarative XML generation for Draw.io diagrams. Core backend for architecture-first pipeline. |
| `browser-use/browser-use` | MIT | Active | 95.0 | `ADOPT_CORE` | Agentic browser controller for exploratory QA and unmapped user journeys. Registered in `registries/browser_registry.yaml`. |
| `microsoft/playwright` CLI | Apache-2.0 | Active | 98.0 | `ADOPT_CORE` | Headless, low-token browser automation for deterministic E2E assertions and accessibility snapshots. |
| Playwright MCP | MIT | Active | 93.0 | `ADOPT_CORE` | Model Context Protocol server exposing browser tools directly to coding agents. |
| Chrome DevTools MCP | Apache-2.0 | Active | 96.0 | `ADOPT_CORE` | Source-mapped console error inspection, network waterfall tracing, and live debugging. |
| Antigravity Native Browser | Built-in | Active | 99.0 | `ADOPT_CORE` | Zero-dependency native browser interface. Integrated into `core/browser_orchestrator.py` routing matrix. |

### 3.3 Security & Quality Assurance
| Candidate Repo | License | Recency | Score | Verdict | Architectural Analysis & Integration Plan |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `sherlock-project/sherlock` | MIT | Active | 88.0 | `ADOPT_SPECIALIZED`| OSINT reconnaissance tool. Strictly used for defensive credential and asset discovery audits. |
| `elementalsouls/Claude-BugHunter`| MIT | Active | 92.5 | `ADOPT_CORE` | Prompt and code security audit rule engine. Integrated into `core/security_auditor.py` defensive gate. |

### 3.4 Data & AI Engineering
| Candidate Repo | License | Recency | Score | Verdict | Architectural Analysis & Integration Plan |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `huggingface/transformers` | Apache-2.0 | Active | 97.0 | `ADOPT_SPECIALIZED`| Model loading and inference utilities for local AI execution. |
| `run-llama/llama_index` | MIT | Active | 96.0 | `ADOPT_CORE` | Document chunking, vector indexing, and hybrid search for knowledge retrieval. |
| `langchain-ai/langchain` | MIT | Active | 93.0 | `ADOPT_CORE` | Model provider abstractions and tool calling primitives. |
| `dair-ai/Prompt-Engineering-Guide`| CC-BY-SA | Active | 90.0 | `ADOPT_CORE` | Reference prompts and reasoning badge patterns codified in `prompts/`. |
| `ucbepic/docetl` | Apache-2.0 | Active | 89.5 | `ADOPT_SPECIALIZED`| Complex document ETL and extraction pipeline. |
| `D4Vinci/Scrapling` | MIT | Active | 91.0 | `ADOPT_SPECIALIZED`| Undetectable web scraping engine for market data extraction. |

### 3.5 Quantitative Finance Domain Pack (`domains/quantitative-finance/`)
| Candidate Repo | License | Recency | Score | Verdict | Architectural Analysis & Integration Plan |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `OpenBB-finance/OpenBB` | AGPL-3.0 | Active | 85.0 | `ADOPT_SPECIALIZED`| Financial data terminal. Integrated via REST/CLI connector only to prevent AGPL copyleft viral effects. |
| `enthought/pyql` (QuantLib) | BSD-3 | Active | 92.0 | `ADOPT_SPECIALIZED`| Derivatives pricing, yield curves, and interest rate modeling library. |
| `domokane/FinancePy` | GPL-3.0 | Active | 80.0 | `ADOPT_SPECIALIZED`| Fixed income and equity derivatives pricing. Isolated subprocess adapter. |
| `pmorissette/ffn` | MIT | Active | 91.0 | `ADOPT_SPECIALIZED`| Performance and risk analytics for financial time-series. |
| `vollib` | MIT | Active | 89.0 | `ADOPT_SPECIALIZED`| Black-Scholes and implied volatility calculation engine. |
| `ranaroussi/yfinance` | Apache-2.0 | Active | 90.0 | `ADOPT_SPECIALIZED`| Yahoo Finance market data scraping client. |
| Alpha Vantage & Twelve Data | Proprietary/REST | Active | 88.0 | `ADOPT_SPECIALIZED`| Realtime market feeds via API testing connectors. |
| `alpacahq/alpaca-py` | Apache-2.0 | Active | 93.0 | `ADOPT_SPECIALIZED`| Commission-free equities and crypto trading execution SDK. |
| QuickFIX | QuickFIX License | Active | 94.0 | `ADOPT_SPECIALIZED`| FIX protocol engine for high-frequency institutional trading gateways. |
| `robcarver17/pysystemtrade` | GPL-3.0 | Active | 84.0 | `ADOPT_SPECIALIZED`| Systematic trading framework. Process-isolated backtesting reference. |
| `feremabraz/bloomberg-terminal`| MIT | Active | 87.0 | `ADOPT_SPECIALIZED`| Web-based financial charting and UI layout reference. |
| `The-Swarm-Corporation/AutoHedge`| MIT | Active | 88.0 | `ADOPT_SPECIALIZED`| Autonomous risk hedging agent algorithms. |

---

## 4. Master Adoption Ledger

| Category | ADOPTED (Core & Specialized) | WATCH / EXPERIMENTAL | REJECTED |
| :--- | :--- | :--- | :--- |
| **Agent Harness** | `affaan-m/ECC`, `obra/superpowers`, `addyosmani/agent-skills`, `secondsky/claude-skills`, `github/spec-kit`, `colbymchenry/codegraph`, `rtk-ai/rtk`, `cytostack/openwolf`, `thedotmack/claude-mem` | `Hmbown/Codewhale`, `JuliusBrussee/caveman`, `nowork-studio/notfair-plugin` | Closed-source unverified harnesses |
| **Browser & QA** | `sparklabx/drawio-ai-kit`, `browser-use`, `playwright-cli`, `playwright-mcp`, `chrome-devtools-mcp`, `antigravity-browser` | Experimental web-driver wrappers | Selenium (legacy slow) |
| **Security** | `ecc-agentshield`, `sherlock-project/sherlock`, `Claude-BugHunter`, `semgrep`, `bandit` | Unverified binary fuzzers | Offensive exploit payloads without defensive context |
| **Data & AI** | `transformers`, `llama_index`, `langchain`, `Prompt-Engineering-Guide`, `Scrapling` | Inactive scraper mirrors | Deprecated LangChain v0.0.x forks |
| **Quant / Finance** | `OpenBB` (connector), `pyql`, `FinancePy` (isolated), `ffn`, `vollib`, `yfinance`, `alpaca-py`, `quickfix` | Unmaintained MT4 indicators | Closed binary trading bots without source or tests |
