# Software Factory

This directory defines the Software Factory operating system for the Integral Market platform. It
packages the constitution, SDD workflow, agent prompts, role skills, and context engineering into a
single, versioned source of truth.

## Quick Start

1. Read MASTER_PROMPT.md and choose the orchestrator prompt to use.
2. Follow SDD_PIPELINE.md to create or update features.
3. Use GRAPHIFY.md before cross-domain changes.
4. Keep roles aligned with ROLES.md and .claude/skills/roles.

## Key Files

- MASTER_PROMPT.md: Primary orchestration prompt for agents.
- SDD_PIPELINE.md: Spec-driven workflow and gates.
- CONTEXT_ENGINEERING.md: Context compression and retrieval.
- GRAPHIFY.md: Graphify usage and update cadence.
- ROLES.md: Role definitions and ownership mapping.
- OPERATIONS.md: Execution, validation, and recovery loops.
