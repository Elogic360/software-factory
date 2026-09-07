# Skill Market Intelligence & Routing Framework

## 1. Skill Discovery & Governance
The Software Factory continuously indexes skills from official and community sources:
- **Core Curated Skills**: 57 internal institutional engineering skills in `skills/`.
- **Everything Claude Code (ECC)**: 271 verified domain skills bridged in `integrations/ecc/skills/`.
- **Total Indexed Skills**: 328 skills discoverable via `.agents/skills/`.

## 2. Minimal Sufficient Context Principle
Skills are never loaded all at once into the context window.
The Smart Skill Router (`context-engine/skill_selector.py`) queries the task, code changes, and project stack to output:
1. **Required Skills** (Must-load)
2. **Recommended Skills** (High relevance)
3. **Optional Skills** (Reference on demand)
4. **Forbidden / Conflicting Skills** (Blocked from injection)
