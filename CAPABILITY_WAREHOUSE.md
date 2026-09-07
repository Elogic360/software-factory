# 🏪 Capability Warehouse & Inventory Specification

The Software Factory maintains an active inventory categorized into 15 formal warehouse stores:

| Warehouse Category | Description | Manifest Location |
| :--- | :--- | :--- |
| **skills** | Agent workflows and specialized execution patterns | `warehouse/skills/` |
| **mcp** | Model Context Protocol servers | `warehouse/mcp/` |
| **plugins** | Extensible runtime plugins (e.g. `ecc-universal`) | `warehouse/plugins/` |
| **tools** | CLIs, build engines, test runners, linters | `warehouse/tools/` |
| **agents** | Specialist role definitions and prompts | `warehouse/agents/` |
| **harnesses** | Multi-agent execution harnesses & runners | `warehouse/harnesses/` |
| **libraries** | Reusable backend & frontend libraries | `warehouse/libraries/` |
| **frameworks** | Full application frameworks | `warehouse/frameworks/` |
| **templates** | Clean architecture boilerplates & scaffolds | `warehouse/templates/` |
| **datasets** | Sample data, market fixtures, and training sets | `warehouse/datasets/` |
| **benchmarks** | Latency, throughput, and accuracy test suites | `warehouse/benchmarks/` |
| **documentation** | Architectural guides, constitutions, and ADRs | `warehouse/documentation/` |
| **patterns** | Event sourcing, CQRS, and resilience patterns | `warehouse/patterns/` |
| **raw-materials** | Plug-and-play building blocks | `warehouse/raw-materials/` |
| **domain-packs** | Curated vertical capability bundles | `warehouse/domain-packs/` |

---

## Standard Manifest Schema

```yaml
id: capability-identifier
name: Human Readable Name
category: skills | mcp | tools | plugins | raw-materials | ...
version: 1.0.0
license: MIT | Apache-2.0 | BSD-3-Clause
source: upstream-url-or-package
installation:
  method: git | npm | pip | copy
  command: install-command
  prerequisites:
    - python >= 3.11
verification:
  command: verification-command
health_check:
  command: health-check-command
uninstall:
  command: uninstall-command
rollback:
  strategy: version-pin | git-revert | git-checkout
```
