# Software Factory — Security & Vulnerability Policy

## 1. Zero Secrets in Version Control
- **Forbidden**: API keys, OAuth client secrets, private keys, database credentials, MT5 passwords, JWT secret seeds.
- **Enforcement**: CI secret scanner (`git-secrets` / `ecc-agentshield` / `trufflehog`) runs pre-commit and on PRs.
- **Environment**: All secrets must be provided via encrypted `.env` files (gitignored) or runtime secret managers.

## 2. Capability Sandboxing & Risk Classification
- **Tier 0/1 Tools**: Read-only AST analysis and token optimization (low risk).
- **Red-Team Tools**: Bug hunting, fuzzing, and penetration testing tools MUST be isolated to designated test environments. Never execute active attacks against production endpoints.
- **Network Boundaries**: AI agents are restricted from executing unapproved outbound payment transactions or unverified third-party binaries.

## 3. Supply Chain Security
- All external dependencies (npm, PyPI, Cargo) must have verified provenance.
- Regular security audits executed via `npx ecc-agentshield scan` and `prowler`.
