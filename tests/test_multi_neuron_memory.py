import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.multi_neuron_memory import CentralEngineeringMemory

def test_multi_neuron_operations():
    with tempfile.TemporaryDirectory() as tmpdir:
        mem = CentralEngineeringMemory(base_dir=tmpdir)
        entry = mem.remember("Decision", "Auth Choice", "Selected OAuth2 / JWT", project_id="proj_alpha")
        assert entry["neuron"] == "Decision"
        assert entry["project_id"] == "proj_alpha"

        recalled = mem.recall("Decision", entry["id"], project_id="proj_alpha")
        assert recalled is not None
        assert recalled["topic"] == "Auth Choice"

        promoted = mem.promote(entry["id"], project_id="proj_alpha")
        assert promoted is not None
        assert promoted["project_id"] == "global"

def test_memory_router():
    with tempfile.TemporaryDirectory() as tmpdir:
        mem = CentralEngineeringMemory(base_dir=tmpdir)
        route_res = mem.route_query("How to implement JWT authentication?", project_id="proj_alpha")
        assert "Security" in route_res["routed_neurons"]
        assert "Decision" in route_res["routed_neurons"]
