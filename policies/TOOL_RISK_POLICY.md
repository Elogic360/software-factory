# Integral Market — Tool Risk Classification & Governance Policy

## 1. Classification Tiers

### READ (Safe by Default)
- **Permissions**: Read-only filesystem access within designated workspace, read-only database queries (SELECT only), web research, market data fetching, documentation reading.
- **Default State**: `ACTIVE`

### WRITE_BENIGN (Normal Supervision)
- **Permissions**: Creating test files, adding documentation, drafting migration scripts, generating reports, branch creation.
- **Default State**: `ACTIVE` / `STANDBY`

### WRITE_SENSITIVE (Explicit Confirmation)
- **Permissions**: Running production database migrations, modifying auth/JWT secret configs, changing Kubernetes/Docker deployment manifests, rotating API keys.
- **Default State**: `STANDBY` (Requires explicit confirmation prompt)

### FINANCIAL_EXECUTION (Disabled by Default)
- **Permissions**: Live broker order placement, MetaTrader 5 order execution, Binance mainnet trades, fund withdrawals, copy-trading order mirroring.
- **Default State**: `DISABLED` (Requires dual-key sign-off and explicit manual unlock).
