# Software Factory — Cross-Layer Debugging & Root Cause Correlation

## 1. The Multi-Layer Problem
AI coding agents frequently fail or hallucinate when diagnosing errors because they treat UI symptoms as UI bugs. For example:
- A user clicks **"Place Order"**.
- A red banner appears saying *"Order failed"*.
- An agent inspects the React component, assumes state handling is broken, and writes redundant frontend null-checks.
- **The actual root cause** was an unapplied database migration where column `status` was missing in table `orders`.

The **Cross-Layer Debugger** (`core/cross_layer_debugger.py`) eliminates this issue by evaluating the entire transmission path before prescribing a code change.

---

## 2. Correlation Pipeline

```text
[ UI Click / Event ]
        │
        ▼
[ Frontend React Handler ]  ──► (Console Error Check)
        │
        ▼
[ HTTP Request / Payload ]  ──► (Network Status / Payload Check)
        │
        ▼
[ API Route / Endpoint ]    ──► (Validation / Auth Check)
        │
        ▼
[ Backend Service Layer ]   ──► (Application Traceback Check)
        │
        ▼
[ Database Query / Schema ] ──► (DDL / Table / Constraint Check)
```

---

## 3. Layer Evaluation Priority
The debugger checks from the **bottom-up**:
1. **DATABASE_LAYER**:
   - `relation "xyz" does not exist` ➔ Missing table / pending migration.
   - `column "xyz" does not exist` ➔ Schema drift.
   - `violates not-null constraint` / `violates foreign key` ➔ Payload integrity violation.
   - `could not connect` ➔ Database daemon down.
2. **BACKEND_SERVICE_LAYER**:
   - Python/Java/Node runtime tracebacks, null pointers, unhandled exceptions.
3. **API_CONTRACT_LAYER**:
   - 404 Not Found ➔ Missing route registration or URL typo.
   - 400 / 422 Unprocessable Entity ➔ Request payload deviates from OpenAPI schema.
   - 401 / 403 ➔ JWT authorization failure.
4. **NETWORK_INFRASTRUCTURE_LAYER**:
   - CORS policy blocked, connection reset, DNS failure.
5. **FRONTEND_UI_LAYER**:
   - Client-side React rendering exceptions, hook ordering violations, undefined props.

---

## 4. CLI Commands & Incident Triage

```bash
# Run cross-layer correlation on current failure logs
python3 factory.py diagnose --incident INC-1001

# Inspect resulting evidence artifact in evidence/incidents/
cat evidence/incidents/INC-1001.json
```
