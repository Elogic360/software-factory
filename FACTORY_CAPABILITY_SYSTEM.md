# 📦 Software Factory Capability System

## Warehouse Manifest Specification
All capabilities in `warehouse/` are indexed with machine-readable manifests:
```yaml
id: capability-id
name: Capability Name
category: skills | mcp | tools | plugins | raw-materials | ...
version: 1.0.0
license: MIT | Apache-2.0
installation:
  method: pip | npm | git | copy
  command: install-command
verification:
  command: verification-command
health_check:
  command: health-command
rollback:
  strategy: version-pin | git-revert
```
