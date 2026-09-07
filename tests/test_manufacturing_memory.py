import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.manufacturing_memory import ManufacturingMemoryLedger

def test_manufacturing_memory_dimensions():
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger = ManufacturingMemoryLedger(storage_dir=tmpdir)
        entry = ledger.record_entry("DECISION", "DB Choice", "Selected PostgreSQL TimescaleDB")
        assert entry["id"].startswith("decision-")

        entries = ledger.query_dimension("DECISION", "PostgreSQL")
        assert len(entries) == 1
        assert "TimescaleDB" in entries[0]["content"]

def test_manufacturing_genealogy():
    with tempfile.TemporaryDirectory() as tmpdir:
        ledger = ManufacturingMemoryLedger(storage_dir=tmpdir)
        ledger.record_genealogy_node(
            product="TestProduct",
            release="1.0.0",
            commit_sha="abc1234",
            task_id="WO-001",
            agent="Architect",
            skill="fastapi-patterns",
            mcp="factory-context-mcp",
            raw_material="fastapi-scaffold",
            upstream_license="MIT"
        )
        nodes = ledger.trace_genealogy("TestProduct")
        assert len(nodes) == 1
        assert nodes[0]["agent"] == "Architect"
        assert nodes[0]["raw_material"] == "fastapi-scaffold"
