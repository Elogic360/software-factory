# 📜 Software & Capability Bill of Materials (SBOM & CBOM)

The Software Factory automatically generates a comprehensive **Capability Bill of Materials (CBOM)** for any manufactured release:

```yaml
bom_version: "1.0"
product: "Integral Market"
product_version: "2.0.0"
generated_at: 1788776171.27
raw_materials:
  - name: "fastapi-enterprise-scaffold"
    category: "scaffold"
    license: "MIT"
    source: "registry"
  - name: "postgresql-timescaledb"
    category: "database"
    license: "Apache-2.0"
    source: "registry"
machinery_tools:
  - name: "playwright"
    type: "e2e-testing"
    license: "Apache-2.0"
mcp_servers:
  - name: "factory-context-mcp"
    permission_tier: "T1_READ"
skills:
  - name: "fastapi-patterns"
    domain: "backend"
    verified: true
agents:
  - role: "Principal Architect"
    model: "inherit"
```
