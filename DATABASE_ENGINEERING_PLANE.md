# Software Factory — Database Engineering Plane

## 1. Overview
The **Database Engineering Plane** (`core/database_engine.py`) provides automated schema discovery, visual ERD diagram synthesis (Mermaid & Draw.io XML), migration safety analysis, and schema-to-model drift detection.

---

## 2. Key Subsystems

### A. SQL DDL Parser & Schema Introspector
Extracts tables, columns, primary keys, foreign key references, and indexes from standard SQL DDL declarations.

### B. Automated ERD Generation
Transforms relational schemas into:
- **Mermaid `erDiagram`** for markdown documentation and PR reviews.
- **Draw.io XML (`mxGraphModel`)** for visual architecture models.

### C. Migration Safety Verification
Scans SQL migration scripts prior to execution to prevent production outages:
- **`DROP TABLE`**: Flagged as critical hazard (irreversible data loss).
- **`DROP COLUMN`**: Flagged as high hazard (violates zero-downtime rolling deployment).
- **`ADD COLUMN NOT NULL without DEFAULT`**: Flagged as high hazard (fails on populated tables).
- **`RENAME COLUMN / TABLE`**: Flagged as medium hazard (breaks existing running queries).
- **`LOCK TABLE`**: Flagged as concurrency bottleneck.

### D. Schema Drift Detection
Compares expected application ORM models against live database tables, flagging missing tables, missing columns, and incompatible column types.

---

## 3. CLI Commands

```bash
# Parse SQL DDL and inspect tables/columns
python3 factory.py database inspect-ddl

# Generate Mermaid ERD diagram
python3 factory.py database erd

# Verify safety of a proposed SQL migration
python3 factory.py database migration-safety --sql "ALTER TABLE accounts ADD COLUMN tier VARCHAR(20);"

# Detect drift between expected models and database
python3 factory.py database drift
```
