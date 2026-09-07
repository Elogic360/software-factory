import yaml
from pathlib import Path

SF_ROOT = Path(__file__).resolve().parent.parent

def test_capability_registry_schema():
    cap_file = SF_ROOT / "registries" / "capability_registry.yaml"
    assert cap_file.exists()
    with open(cap_file) as f:
        data = yaml.safe_load(f)
    assert "capabilities" in data
    assert len(data["capabilities"]) > 0
    for cap in data["capabilities"]:
        assert "id" in cap
        assert "name" in cap
        assert "category" in cap
        assert "tier" in cap
        assert "license" in cap

def test_mcp_registry():
    mcp_file = SF_ROOT / "registries" / "mcp_registry.yaml"
    assert mcp_file.exists()
    with open(mcp_file) as f:
        data = yaml.safe_load(f)
    assert "mcp_servers" in data
    assert len(data["mcp_servers"]) >= 5
