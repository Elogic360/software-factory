import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.architecture_engine import ArchitectureEngine

def test_c4_and_mermaid_generation():
    arch = ArchitectureEngine()
    c4 = arch.generate_c4_model(
        product_name="TradingCore",
        containers=[{"name": "API", "tech": "FastAPI"}],
        components=[{"name": "Router", "responsibility": "Dispatch"}]
    )
    assert c4["product"] == "TradingCore"
    mermaid = arch.generate_mermaid_c4(c4)
    assert "C4Context" in mermaid
    assert "TradingCore" in mermaid

def test_architecture_drift_detection():
    arch = ArchitectureEngine()
    expected = arch.build_architecture_graph([{"id": "auth"}, {"id": "orders"}], [])
    drift = arch.detect_drift(expected, ["/api/v1/auth", "/api/v1/orders", "/api/v1/untracked"])
    assert drift["has_drift"] is True
    assert "untracked" in drift["undocumented_live_services"]
