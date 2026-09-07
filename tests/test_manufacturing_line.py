import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.manufacturing_line import ManufacturingLine

def test_manufacturing_gates():
    with tempfile.TemporaryDirectory() as tmpdir:
        line = ManufacturingLine(workspace_root=tmpdir)
        gates = line.list_gates()
        assert len(gates) == 17
        assert gates[0]["id"] == "G0"
        assert any(g["id"] == "G0.5" for g in gates)
        assert gates[-1]["id"] == "G15"

        eval_res = line.evaluate_gate("G7", {"passed": True, "errors": []})
        assert eval_res["status"] == "PASSED"

        eval_g05 = line.evaluate_gate("G0.5", {"passed": True, "errors": []})
        assert eval_g05["status"] == "PASSED"
        assert eval_g05["gate_id"] == "G0.5"

def test_generate_work_orders():
    line = ManufacturingLine()
    tasks = [
        {"title": "Task A", "station": "Backend", "agent": "Backend Dev"},
        {"title": "Task B", "station": "QA", "agent": "QA Dev"}
    ]
    res = line.generate_work_orders("SpecTest", tasks)
    assert res["total_orders"] == 2
    assert res["work_orders"][0]["work_order_id"] == "WO-001"
