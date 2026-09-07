# Software Factory Baseline Report
**Target Date**: 2026-09-03
**Ecosystem**: Integral Market & IM-Sensei Capability Layer
**Author**: Principal Tooling Architect & Software Factory Engine

---

## 1. System Inventory

### Application Roots & Ports
- **Integral Market Main Platform**: `/home/elogic360/Desktop/little QUANTUM/IntegralMarket/app` (Port `5173`)
- **IM-Sensei AI Platform**: `/home/elogic360/Desktop/little QUANTUM/IntegralMarket/im-sensei` (Port `5177`)
- **Market Backend Core**: `/home/elogic360/Desktop/little QUANTUM/IntegralMarket/integral-market-backend` (Port `8000`)
- **Expert Backend Core**: `/home/elogic360/Desktop/little QUANTUM/IntegralMarket/integral-expert-backend` (Port `8001`)
- **Intelligence Backend Core**: `/home/elogic360/Desktop/little QUANTUM/IntegralMarket/integral-market-intelligence` (Port `8002`)
- **Sensei Backend Gateway**: `/home/elogic360/Desktop/little QUANTUM/IntegralMarket/integral-sensei-backend` (Port `8010`)
- **PostgreSQL Database**: `localhost:5432/integral_market_db` (`iam.*`, `sensei.*`, `market.*`, `public.*`)
- **Valkey / Redis Cache**: `localhost:6379/0-4` (Db 4 = Sensei)

---

## 2. Capability Architecture & Ground Truth

### Discovery Configuration
- **Agent Discovery**: `.mcp.json`, `CLAUDE.md`, and `.claude/` root settings.
- **Tool-Risk Boundaries**:
  - `READ`: Safe by default (Database SELECT, logs, market quotes, file inspection).
  - `WRITE_BENIGN`: Supervised development actions (code creation, branch testing, report generation).
  - `WRITE_SENSITIVE`: Requiring explicit confirmation (migrations, infra deployments, auth keys).
  - `FINANCIAL_EXECUTION`: Strictly disabled by default (MT4/MT5 live trading, broker execution, fund movements).

### MCP & Skill Tiering
- **Core Tier (Active)**: Universal substrate (Filesystem, Git, GitHub, Fetch, Memory, Sequential Thinking, Time, Context7).
- **Stack Tier (Standby/Active on demand)**: Database inspectors (3x Postgres), Container ops (Docker), AI Observability (Langfuse, Qdrant), Market Data (Alpha Vantage, Yahoo Finance, FRED, CoinGecko), Paper Brokers (Alpaca, MT5 build-only).
- **Extended Tier (Standby)**: Communications, cloud hosting, CI/CD, QA automation.
