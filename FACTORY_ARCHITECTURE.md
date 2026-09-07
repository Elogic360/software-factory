# 🏛️ Software Factory Architecture Specification

## 1. System Vision & Paradigm
The **Software Factory** is a domain-general, AI-native **Software Manufacturing Operating System (MOS)**. It transitions engineering teams and AI coding agents from ad-hoc manual prompt execution into a structured, evidence-backed assembly pipeline.

```text
GLOBAL ECOSYSTEM ➔ RADAR ➔ WAREHOUSE ➔ PRODUCT INTAKE ➔ SDD COMPILER ➔ PRODUCTION FLOOR ➔ QUALITY GATES ➔ OBSERVABILITY ➔ LEARNING LOOP
```

---

## 2. Core Subsystems
1. **Multi-Neuron Central Memory** (`core/multi_neuron_memory.py`): 28 specialized memory neurons across 6 scopes (`GLOBAL`, `PROJECT`, `TEAM`, `USER`, `TASK`, `SESSION`).
2. **Context & Token Optimization Plane** (`core/context_optimizer.py`): Realtime ranking, SHA-256 deduplication, semantic compression, and hard budget enforcement.
3. **Architecture-as-Code Engine** (`core/architecture_engine.py`): C1-C4 models, Mermaid diagrams, Draw.io XML export, and live service drift detection.
4. **Enterprise SDD Plan Compiler** (`core/spec_compiler.py`): Turns requirements into executable work orders (`WO-xxx`) with strict dependency graphs.
5. **Quality Control & Assembly Line** (`core/manufacturing_line.py`): G0 through G15 gate evaluation with mandatory evidence artifacts.
6. **Agent Control Plane** (`core/agent_control_plane.py`): Capability negotiation and session crash recovery across Antigravity, Claude Code, Codex, Cursor, and OpenCode.
7. **Production Observability & SRE** (`core/observability_sre.py`): Health telemetry, error-budget tracking, and automated deployment rollback.
8. **Self-Learning Engine** (`core/learning_engine.py`): Failure mining, pattern mining, and non-breaking self-improvement proposals.
