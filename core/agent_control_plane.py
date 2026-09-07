"""
Software Factory Agent-Agnostic Control Plane.
Negotiates capabilities and handles seamless agent handoffs and crash recovery checkpoints.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

SUPPORTED_AGENTS = [
    "Antigravity",
    "Claude Code",
    "Codex",
    "Cursor",
    "GitHub Copilot",
    "Gemini CLI",
    "OpenCode",
    "Aider",
    "Cline",
    "Roo Code"
]

class AgentControlPlane:
    """Manages agent negotiation, prompt adaptation, and session checkpoints."""

    def __init__(self, checkpoint_dir: Optional[str] = None):
        if checkpoint_dir is None:
            self.checkpoint_dir = Path(__file__).resolve().parent.parent / "recovery" / "checkpoints"
        else:
            self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def negotiate_capabilities(self, agent_name: str) -> Dict[str, Any]:
        """Detects and returns supported toolsets and environment constraints for an agent."""
        agent_clean = agent_name.strip()
        is_supported = any(a.lower() == agent_clean.lower() for a in SUPPORTED_AGENTS)

        # Baseline capabilities
        capabilities = {
            "agent": agent_clean,
            "supported": is_supported,
            "supports_mcp": agent_clean.lower() in ["antigravity", "claude code", "cursor", "cline", "roo code"],
            "supports_subagents": agent_clean.lower() in ["antigravity", "claude code"],
            "supports_shell": True,
            "supports_git": True,
            "context_budget_tokens": 128000 if "antigravity" in agent_clean.lower() or "gemini" in agent_clean.lower() else 32000,
            "recommended_transport": "stdio"
        }
        return capabilities

    def create_checkpoint(self, session_id: str, project_id: str, active_task: str, memory_state: Dict[str, Any], git_commit: str) -> Path:
        """Saves session state for seamless agent handoff or crash recovery."""
        checkpoint_data = {
            "session_id": session_id,
            "project_id": project_id,
            "active_task": active_task,
            "git_commit": git_commit,
            "timestamp": time.time(),
            "memory_state_summary": {
                "active_neurons": list(memory_state.keys()),
                "total_records": sum(len(v) if isinstance(v, list) else 1 for v in memory_state.values())
            }
        }
        checkpoint_file = self.checkpoint_dir / f"checkpoint_{session_id}.json"
        with open(checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(checkpoint_data, f, indent=2)
        return checkpoint_file

    def restore_checkpoint(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Restores session state after an agent transition or crash."""
        checkpoint_file = self.checkpoint_dir / f"checkpoint_{session_id}.json"
        if not checkpoint_file.exists():
            return None
        with open(checkpoint_file, "r", encoding="utf-8") as f:
            return json.load(f)
