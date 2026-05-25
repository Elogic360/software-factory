# Recovery Playbook: Database Migration Failure

## Diagnosis Tree

```
Migration fails?
  │
  ├── alembic upgrade head → ERROR
  │     ├── "column already exists"
  │     │     → migration ran partially; DB is inconsistent
  │     │     → psql: SELECT * FROM alembic_version;
  │     │     → manually mark migration complete if column was added:
  │     │         alembic stamp <revision_id>
  │     │     → OR: fix migration to use IF NOT EXISTS
  │     │
  │     ├── "relation does not exist"
  │     │     → schema not created before table creation
  │     │     → add: op.execute("CREATE SCHEMA IF NOT EXISTS <schema>")
  │     │     → at the TOP of the migration upgrade() function
  │     │
  │     ├── "violates not-null constraint"
  │     │     → adding NOT NULL column to table with existing rows
  │     │     → migration must add with DEFAULT first, then set NOT NULL:
  │     │         op.add_column('table', sa.Column('col', sa.String(), server_default=''))
  │     │         op.alter_column('table', 'col', server_default=None)
  │     │
  │     ├── "multiple heads" in alembic
  │     │     → two branches created conflicting migrations
  │     │     → alembic merge heads -m "merge_heads"
  │     │     → alembic upgrade head
  │     │
  │     └── "Can't locate revision"
  │           → revision in alembic_version not found in migrations/
  │           → alembic history --verbose to see all known revisions
  │           → alembic stamp <known-good-revision>
  │           → alembic upgrade head
  │
  └── Migration succeeds but app still errors
        → Model doesn't match DB schema
        → Run: python3 -c "from app.models import *" (check for errors)
        → Compare model definition with: \d <schema>.<table> in psql
```

---

## Safe Migration Checklist (Before Running)

```bash
# 1. BACKUP production DB before any migration
pg_dump -h localhost -U postgres integral_market > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Test migration on a copy first
createdb integral_market_test
pg_restore -d integral_market_test backup_*.sql
DATABASE_URL=postgresql+asyncpg://postgres:pass@localhost/integral_market_test \
  alembic upgrade head

# 3. Verify rollback works
alembic downgrade -1
alembic upgrade head   # apply again to confirm idempotency

# 4. Check migration is non-destructive for running app
# → Adding columns: safe (existing app ignores unknown columns)
# → Removing columns: DANGEROUS (app crashes reading removed column)
# → Renaming columns: DANGEROUS (two-step: add new, deploy app, remove old)
```

---

## Destructive Migration Protocol (2-Step)

```
Step 1 — Deploy migration that adds new structure (backward-compatible)
  → Add new column / table
  → Keep old column (app still reads it)
  → Deploy: app reads BOTH old and new

Step 2 — Deploy migration that removes old structure
  → Remove old column only after ALL app instances use new column
  → Deploy: single cutover

Never remove a column and deploy app in the same release.
```

---

## Emergency Rollback

```bash
# Roll back last migration
alembic downgrade -1

# Roll back to specific revision
alembic downgrade <revision_id>

# Nuclear option: restore from backup
psql -h localhost -U postgres -c "DROP DATABASE integral_market;"
psql -h localhost -U postgres -c "CREATE DATABASE integral_market;"
psql -h localhost -U postgres integral_market < backup_YYYYMMDD_HHMMSS.sql
```
