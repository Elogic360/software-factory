import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.warehouse import CapabilityWarehouse

def test_warehouse_inventory():
    wh = CapabilityWarehouse()
    inv = wh.list_inventory()
    assert len(inv) == 15
    assert inv["skills"] >= 1
    assert inv["mcp"] >= 2

def test_warehouse_search():
    wh = CapabilityWarehouse()
    results = wh.search("FastAPI")
    assert len(results) > 0
    assert any("fastapi" in r["id"].lower() for r in results)
