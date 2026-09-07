# Software Factory — API Testing Plane & Contract-First Framework

## 1. Overview
The **API Testing Plane** (`core/api_testing_engine.py`) enforces strict contract-first API development. No endpoint is built without an OpenAPI 3.x specification, and no UI interaction is merged without runtime verification against that contract.

---

## 2. Core Capabilities
1. **OpenAPI 3.x Validation**:
   - Validates paths, HTTP methods, operation IDs, request schemas, parameters, response definitions, and status codes.
2. **Automated Contract Test Generation**:
   - Compiles exhaustive assertions for every declared route and expected status code.
3. **Response Schema Assertion**:
   - Performs deep type checking, required field checks, and structural verification on response bodies.
4. **Contract Drift Detection**:
   - Intercepts live or mocked network traffic logs to flag undocumented endpoints, undocumented status codes, or payload schema divergences.
5. **UI-to-API Interaction Tracing**:
   - Asserts latency thresholds (<500ms) and payload correctness when UI widgets trigger backend HTTP requests.

---

## 3. CLI Commands

```bash
# Validate an OpenAPI specification
python3 factory.py api validate --spec specs/openapi.yaml

# Generate and display contract test assertions
python3 factory.py api test-contract

# Detect contract drift from recorded network traffic
python3 factory.py api drift
```
