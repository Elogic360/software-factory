# Skill Supply-Chain Security Model

## 🛡️ Security Verification Pipeline
Every third-party or discovered skill must pass through the multi-stage auditor:

```
SOURCE → HASH → LICENSE → STATIC AST → PROMPT INJECTION SCAN → CREDENTIAL CHECK → TRUST LEVEL
```

## Trust Levels
- `TRUSTED_OFFICIAL`: Maintained by core project team.
- `TRUSTED_VERIFIED`: Verified open-source source with clean audit.
- `COMMUNITY_VERIFIED`: Community skill passing all static rules.
- `EXPERIMENTAL`: Sandbox-only execution.
- `QUARANTINED`: Blocked due to suspicious patterns.
- `REJECTED`: Fails safety policy (malicious payloads).
