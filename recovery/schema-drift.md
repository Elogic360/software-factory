# Recovery Playbook: Schema Drift

## What Is Schema Drift?

Schema drift occurs when the SQLAlchemy model definition diverges from the
actual PostgreSQL database schema. Causes:
- Migration ran partially
- Migration was skipped
- Manual DB changes were made without a migration
- Production DB has different state than development DB

---

## Detecting Schema Drift

```bash
# Method 1: Check alembic status
cd integral-expert-backend && source venv/bin/activate
alembic current          # what revision is the DB at?
alembic heads            # what revision does code expect?
# If these differ → schema drift

# Method 2: Alembic auto-detect
alembic check            # reports if DB matches current models
# If output: "Target database is not up to date" → drift detected

# Method 3: Generate diff migration to see what's missing
alembic revision --autogenerate -m "detect_drift"
# Open the generated file — it shows what alembic would change
# If it shows ALTER TABLE / ADD COLUMN → drift confirmed
# Delete this migration if you don't want to apply it yet
```

---

## Diagnosis Tree

```
Schema drift detected?
  │
  ├── App raises: "column <name> does not exist"
  │     → Migration exists in codebase but was never applied
  │     → alembic upgrade head
  │
  ├── App raises: "column <name> of relation <table> does not exist"
  │     (but model and migration both look correct)
  │     → Wrong schema prefix
  │     → Check __table_args__ = {"schema": "journal"} matches migration schema
  │
  ├── alembic upgrade head fails with "column already exists"
  │     → Migration was applied manually but not recorded in alembic_version
  │     → Mark it as applied: alembic stamp <revision_id>
  │
  ├── Model has new field but DB doesn't
  │     → Generate migration: alembic revision --autogenerate -m "add_<field>"
  │     → Review generated migration carefully before applying
  │     → alembic upgrade head
  │
  └── DB has column that model doesn't (orphaned column)
        → Model was simplified but migration to remove column was never written
        → Create manual migration: op.drop_column('table', 'column', schema='schema')
        → Note: only do this after confirming no code references the column
```

---

## Inspect DB Schema Directly

```bash
# Connect to DB
psql -h localhost -U postgres integral_market

# List schemas
\dn

# List tables in a schema
\dt journal.*
\dt copy_trading.*
\dt iam.*

# Inspect a table's columns
\d journal.trades
\d copy_trading.subscriptions

# Check alembic history
SELECT version_num FROM alembic_version;
```

---

## Prevention

```python
# In CI pipeline, add schema validation step:
# Run alembic check — fails if DB is not at head revision
# This catches drift before it reaches production

# .github/workflows/ci.yml
- name: Validate schema sync
  run: |
    cd integral-expert-backend
    source venv/bin/activate
    alembic upgrade head
    alembic check   # exits non-zero if drift detected
```

---

## Nuclear Reset (Dev Only)

```bash
# Drop and recreate DB from scratch (NEVER on production)
psql -U postgres -c "DROP DATABASE IF EXISTS integral_market;"
psql -U postgres -c "CREATE DATABASE integral_market;"
cd integral-expert-backend && source venv/bin/activate
alembic upgrade head
python3 scripts/seed_data.py   # reseed required reference data
```
