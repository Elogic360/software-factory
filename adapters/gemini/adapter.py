"""
Gemini CLI / Antigravity Adapter — Configures GEMINI.md, central memory integration,
and progressive skills loading from the Software Factory and ECC ecosystems.
"""

from pathlib import Path
from typing import Dict, Any

def setup_gemini(target_project_dir: Path, sf_dir: Path) -> Dict[str, Any]:
    gemini_md = sf_dir / "GEMINI.md"
    target_gemini = target_project_dir / "GEMINI.md"

    if not target_gemini.exists():
        content = f"""# Gemini CLI & Antigravity Agent Configuration — Software Factory

You are connected to the Software Factory universal capability ecosystem.

## 🏛️ 1. Supreme Engineering Law
Always adhere to the constitution:
- **Path**: `{sf_dir}/constitution/CONSTITUTION.md`
- **Rules**: Strict boundary enforcement, API versioning (/api/v1/), and spec-driven execution.

## 🧠 2. Central Memory & Knowledge Integration
- Memory Hub: `{sf_dir}/state/memory-index.json`
- Architecture State: `{sf_dir}/state/architecture-state.yaml`
- ECC Capability: `{sf_dir}/capabilities/agent-harness/ecc/`

## 🧭 3. Task Bootstrap Protocol
1. Consult Constitution.
2. Route skills: `python3 {sf_dir}/context-engine/skill_selector.py --query "<task>" --top 3`.
3. Verify changes with `bin/software-factory verify`.
"""
        target_gemini.write_text(content, encoding="utf-8")

    return {
        "status": True,
        "agent": "gemini",
        "configured_files": [str(target_gemini)],
        "capabilities_connected": ["central_memory", "ecc_skills", "architecture_state"]
    }
