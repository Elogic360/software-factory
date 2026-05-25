# Recovery Playbook: API Contract Break

## What Is an API Contract Break?

A contract break occurs when:
- Frontend expects a field that the backend removed
- Backend changes a field type (e.g., `string` → `number`)
- Backend changes a route URL
- Backend adds a required field to a request body
- Backend changes response status codes

---

## Diagnosis Tree

```
Frontend shows "undefined" / crashes on API response?
  │
  ├── Network tab shows 404 on API call
  │     → Route URL changed in backend
  │     → Check git log -- integral-<backend>/app/api/v1/endpoints/
  │     → Either: revert route change, OR update frontend to new URL
  │
  ├── Network tab shows 422 Unprocessable Entity
  │     → Request body or query params don't match Pydantic schema
  │     → Check the response body — it lists exactly which field failed
  │     → Fix: update frontend to send correct fields
  │     → OR: add Optional[...] to backend schema (if field is new)
  │
  ├── Network tab shows 200 but data is wrong/missing
  │     → Backend changed response shape (field renamed, removed, nested)
  │     → Compare TypeScript type definition with actual API response
  │     → Fix options:
  │         A) Update TypeScript type + usage
  │         B) Add backward-compat alias in backend response
  │
  └── Type error in TypeScript on build
        → TypeScript type is out of sync with actual backend response
        → Run: pnpm type-check for full error list
        → Update the relevant type in app/src/shared/api/types/
```

---

## API Versioning Rules

```python
# NEVER change a response field that frontend already uses
# Instead: ADD the new field, keep the old one, deprecate gradually

# WRONG — breaks frontend immediately:
class AccountResponse(BaseModel):
    # Old: balance: float
    account_balance: float   # renamed field → frontend breaks

# CORRECT — backward compatible:
class AccountResponse(BaseModel):
    balance: float            # keep original (frontend uses this)
    account_balance: float    # add new name too

# After frontend is updated → remove old field in next version

# Route versioning: if you must break the contract, use a new version:
# /api/v1/brokers/accounts  → keep for existing clients
# /api/v2/brokers/accounts  → new contract for new clients
```

---

## Sync TypeScript Types with Backend

```bash
# Option A: Manual sync (current approach)
# 1. Check the FastAPI schema at http://localhost:8000/docs (Swagger)
# 2. Look at the Pydantic model Response class
# 3. Update TypeScript type in app/src/shared/api/types/<domain>.ts

# Option B: Generate types automatically from OpenAPI schema
# Install: pnpm add -D openapi-typescript
npx openapi-typescript http://localhost:8000/openapi.json -o src/shared/api/types/market-api.d.ts
npx openapi-typescript http://localhost:8002/openapi.json -o src/shared/api/types/expert-api.d.ts
```

---

## Breaking Change Process

```
When a breaking API change is unavoidable:

1. Communicate: notify all consumers before deploying
2. Version: deploy new route (/v2/) alongside old (/v1/)
3. Migrate: update frontend to use new route
4. Monitor: confirm zero traffic on old route
5. Deprecate: add deprecation warning header to old route
6. Remove: delete old route after 2 sprint cycles
```
