# Everything Claude Code (ECC) Agent Harness Integration

## Overview
**Everything Claude Code (ECC)** (`affaan-m/ECC`) is integrated into the Software Factory as a Tier-0 Core capability. It provides:
- 328+ curated agent skills
- Adaptive instincts and operator control-plane patterns
- Multi-harness support: Claude Code, Cursor, Codex, OpenCode, Gemini CLI, Copilot, Antigravity
- Security governance via `ecc-agentshield`
- Work-items and session state tracking via SQLite

## Architecture
- **Location**: `capabilities/agent-harness/ecc/`
- **Vendored Reference**: `integrations/ecc/`
- **CLI Executable**: `bin/ecc`
- **Health Check**: `capabilities/agent-harness/ecc/healthcheck.py`
- **Functional Tests**: `tests/test_ecc_capability.py`

## Installation
```bash
bash capabilities/agent-harness/ecc/install.sh
```

## Verification
```bash
python3 capabilities/agent-harness/ecc/healthcheck.py
pytest tests/test_ecc_capability.py -v
```

## Usage
```bash
# Discover install profiles
bin/ecc catalog profiles

# Consult skills for a task
bin/ecc consult "high-frequency market data websocket"

# Run security IOC scan
bin/ecc security-ioc-scan
```
