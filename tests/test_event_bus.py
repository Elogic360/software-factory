import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.event_bus import FactoryEventBus

def test_event_bus_emit_and_replay():
    with tempfile.TemporaryDirectory() as tmpdir:
        bus = FactoryEventBus(log_dir=tmpdir)
        captured = []
        bus.subscribe("task.completed", lambda evt: captured.append(evt))

        evt = bus.emit("task.completed", {"task_id": "TSK-001", "result": "passed"})
        assert evt["event_type"] == "task.completed"
        assert len(captured) == 1

        replayed = bus.replay_events("task.completed")
        assert len(replayed) == 1
        assert replayed[0]["payload"]["task_id"] == "TSK-001"
