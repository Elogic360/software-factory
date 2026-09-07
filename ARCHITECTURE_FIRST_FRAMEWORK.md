# Software Factory — Section 22 Architecture-First Framework

## 1. Principle
In the Software Factory Operating System, **architecture is executable code**. 

No AI coding agent may write application code without an explicit `state/architecture-state.yaml` specification defining:
- System boundaries (modules & responsibilities)
- Exported and forbidden imports
- Data models & database schema relations
- API routes and security contracts
- Universal architectural invariants

---

## 2. Universal Architectural Invariants
All projects managed by the Software Factory must comply with these non-negotiable invariants:
1. **`NO_CROSS_SCHEMA_WRITES`**: A service or module must never perform direct writes across DB schemas.
2. **`ALL_ROUTES_VERSIONED_V1`**: All public and internal API endpoints must be prefixed with `/api/v1/`.
3. **`STRICT_MODULE_EXPORTS`**: Modules must only consume external domain internals via public index exports.
4. **`NO_RAW_QUERIES_IN_CONTROLLERS`**: Controllers and HTTP handlers must delegate data access to service/repository layers.
5. **`NO_HARDCODED_SECRETS`**: Configuration and secrets must be injected via environment or secure keyrings.

---

## 3. Architecture Compiler
The `ArchitectureStateManager` (`core/architecture_state.py`) compiles `architecture-state.yaml` directly into:
- Directory skeletons with bounded context boundaries.
- Module initialization files (`__init__.py` / `index.ts`) with explicit `__all__` exports.
- Architectural compliance scanners that verify no forbidden imports exist in source code.

---

## 4. CLI Commands

```bash
# Validate architecture state
python3 factory.py architecture validate

# Detect architectural drift
python3 factory.py architecture drift

# Run full-spectrum verification loop
python3 factory.py verify
```
