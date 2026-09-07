# Software Factory — Open-Source Contribution & Maintenance Guide

## 1. Adding a New Capability
1. Create a capability entry in `registries/capability_registry.yaml` conforming to `schemas/capability_schema.json`.
2. Provide valid metadata, installation commands, license classification, and health check.
3. Run `factory doctor` and `factory validate` to ensure zero regressions.

## 2. Adding a New Skill
1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter.
2. Add triggers to `context-engine/skill_selector.py`.
3. Register skill in `SKILLS_REGISTRY.md`.
