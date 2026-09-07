# ADR-009 — MCP Layer: Memory / Context / Token-Optimization Candidate Selection

**Date**: 2026-09-07  
**Status**: Accepted  
**Deciders**: Antigravity (Engineering Agent), Elogic360  
**Context Source**: Live MCP ecosystem research + Forensic Audit `MCP_FORENSIC_INVENTORY.md` (dc9294f0)

---

## 1. Problem Statement

The Software Factory's MCP layer had three documented gaps as of the forensic audit:

1. **Token Optimization MCP: BLOCKED** — `mcp/token_optimization_server.py` crashed on every `tools/call` because it invoked `optimizer.compress_tool_output()`, a method that does not exist on `ContextOptimizer`.
2. **Path portability: BROKEN** — `FACTORY.yaml` hardcoded absolute paths under `/home/elogic360/...`, making the factory non-portable across machines or clone locations.
3. **Registry gap** — No Memory MCP or Context-compression MCP candidates were registered, despite these being explicitly required by the factory's Central Memory and Token Optimization planes.

Additionally, a 2026 security scan of the wider MCP ecosystem found **36.7% of public MCP servers carry SSRF vulnerabilities, 41% have zero authentication**. The factory's Capability Evaluation Pipeline (security scan → sandbox → functional test → register) is non-negotiable for all candidates.

---

## 2. Decisions Made

### 2.1 Immediate Bug Fixes (Applied)

| Fix | File | Root Cause | Resolution |
|---|---|---|---|
| `compress_tool_output` crash | `mcp/token_optimization_server.py` | Called non-existent method on `ContextOptimizer` | Replaced with inline head/tail line-trimming logic |
| `compression_ratio` display | `mcp/token_optimization_server.py` | Showed raw ratio (~1.0) instead of % reduction | Fixed to `(1.0 - ratio) * 100` format |
| Absolute paths | `FACTORY.yaml` | Hardcoded `/home/elogic360/...` paths | Replaced with relative paths `./mcp`, `./custom-mcp`, etc. |

### 2.2 Registry Additions (Candidates Registered — NOT Yet Production-Activated)

All entries below are tagged `evaluation_status: CANDIDATE` and require the full Capability Evaluation Pipeline before activation.

#### Memory Candidates

| ID | Source | Why Selected | Deduplication Note |
|---|---|---|---|
| `mcp-memory-service` | `doobidoo/mcp-memory-service` | Autonomous consolidation matches factory Central Memory quality-control design. Integrates with LangGraph/CrewAI/AutoGen/Claude. | Primary memory candidate. |
| `mcp-memory-fellowgeek` | `fellowgeek/mcp-memory` | Explicitly targets Antigravity. Local SQLite + Markdown/YAML — strong provenance/auditability fit. No telemetry. | Fallback/complement to doobidoo (provenance layer). |

**Deferred (duplication decision needed before activating):**
- `cytostack/openwolf` — overlaps memory AND token-accounting; evaluate against both categories before registering.
- Graphiti (self-hosted OSS engine) — evaluate only if temporal memory with validity windows is needed.
- Mem0 OSS core — evaluate only if 30+ ingestion sources are required.

**Rejected:**
- Hjarni, Supermemory, Letta — commercial-first products with MCP as access layer. Not open-source-first.

#### Context-Engineering Candidates

| ID | Source | Why Selected |
|---|---|---|
| `smart-context-mcp` | `arrayo/smart-context-mcp` | MIT license, read-only tools (low SSRF surface), addresses "targeted retrieval over full dumps" principle. Reports 46x compression — validate with factory corpus. |

**Already registered (production):** `codegraph`, `gortex` (both code-intelligence context servers).

**Design reference (not a dependency):** Cloudflare MCP Portal `optimize_context` pattern — strip tool schemas by default, expose `query` for on-demand definition retrieval. Implement as factory MCP gateway design, not as an installed server.

**Field-projection wrapper pattern** — implement as an architectural wrapper across all factory MCPs, not as a standalone registered server.

#### Token-Optimization Candidates

| ID | Source | Layer | Why Selected |
|---|---|---|---|
| `headroom-mcp` | Ecosystem (paired with RTK) | MCP-layer | Complements `rtk-ai/rtk` (CLI-layer). Different token-bloat sources: RTK = shell commands, Headroom = logs/traces/RAG chunks/handoff notes. |
| `toon-parse-mcp` | PyPI / official MCP Registry | MCP-layer | Narrow scope (data-format conversion). In official registry. Register as specialized optimizer only. |

**Already installed (CLI layer):** `rtk-ai/rtk` (Rust binary, 60–90% reduction on git/docker/kubectl outputs). Keep alongside MCP-layer tools.

**Deferred (consolidation decision needed):**
- `ooples/token-optimizer-mcp` — 74 tools is too broad to trust blindly. Sample-test ≥10 representative tools in sandbox before bulk registration.
- `LeanCTX` — 76 MCP tools, overlaps Memory + Token + Context categories. Evaluate as a potential umbrella replacement for several narrower tools rather than installing alongside all of them.

**Already registered (skill, not MCP):** `JuliusBrussee/caveman` — register as a skill using terse output conventions (~65% token cut). Do not stack redundantly with RTK + Headroom on the same task.

---

## 3. Evaluation Pipeline — Sequenced Order

Run the Capability Evaluation Pipeline for candidates in this sequence:

```
Round 1 (Memory — highest impact gap):
  1. doobidoo/mcp-memory-service
  2. fellowgeek/mcp-memory

Round 2 (Context — codegraph already approved):
  3. arrayo/smart-context-mcp

Round 3 (Token — token optimizer now fixed):
  4. headroom-mcp (confirm exact npm package name first)
  5. toon-parse-mcp

Round 4 (Deferred consolidation decision):
  6. LeanCTX — benchmark against items 1–5 combined; replace if it covers all
  7. ooples/token-optimizer-mcp — sample-test 10+ tools before bulk activation
  8. cytostack/openwolf — decide: memory-only, token-only, or both roles
```

For each: **license check → security scan (SSRF/auth audit per 2026 findings) → sandbox execution → functional test → update evaluation_status → register if approved.**

---

## 4. Discovery Cadence

Per Phase J of the renovation roadmap: schedule a weekly Radar job querying **at minimum three directories**:
- **Breadth**: Glama (~22,000+ listed) or mcp.so
- **Freshness**: PulseMCP (weekly editorial picks)
- **Security signal**: Apigene (~251 OWASP-scanned verified servers)

Run: `python3 software-factory/factory.py radar --period weekly`

---

## 5. Consequences

- `token_optimization_server.py` is unblocked and production-approved. Status changed from `BLOCKED` to `PRODUCTION_APPROVED` in registry.
- `FACTORY.yaml` is now portable across machines and clone locations.
- 5 new candidates are registered with evaluation metadata — none are activated until the pipeline passes.
- The duplication-detection law is explicitly applied: openwolf, LeanCTX, and ooples/token-optimizer are deferred until the primary candidates are evaluated.
- GitHub stars enumeration (207 repos) requires authenticated GitHub API access — not yet done. Cross-check candidates against actual stars list using `factory github list-stars` once `GITHUB_TOKEN` is configured.
