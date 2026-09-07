import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.agent_control_plane import AgentControlPlane

def test_agent_negotiation():
    plane = AgentControlPlane()
    caps = plane.negotiate_capabilities("Antigravity")
    assert caps["supported"] is True
    assert caps["supports_mcp"] is True
    assert caps["context_budget_tokens"] > 32000

def test_checkpoint_restore():
    with tempfile.TemporaryDirectory() as tmpdir:
        plane = AgentControlPlane(checkpoint_dir=tmpdir)
        cp_file = plane.create_checkpoint("sess-01", "proj-a", "TSK-01", {"Decision": []}, "commit123")
        assert cp_file.exists()

        restored = plane.restore_checkpoint("sess-01")
        assert restored is not None
        assert restored["git_commit"] == "commit123"
