# Software Factory — Dependency Governance & Quality Policy

## 1. Single Reusable Standard Over Sprawl
- Prefer one high-quality, maintained capability over multiple overlapping dependencies.
- Example: `codegraph` + `gortex` for AST graph intelligence; `rtk` for token optimization.

## 2. Upstream Health Metrics
- Every integrated library must pass maintenance checks: active maintainers, compatible runtime (Python 3.10+, Node 18+), zero open critical CVEs.
