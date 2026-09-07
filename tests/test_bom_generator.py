import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.bom_generator import BillOfMaterialsGenerator

def test_cbom_generation():
    cbom = BillOfMaterialsGenerator.generate_cbom(
        product_name="TradingHub",
        version="1.0.0",
        raw_materials=[{"name": "fastapi-scaffold", "license": "MIT"}],
        tools=[{"name": "pytest", "license": "MIT"}],
        mcp_servers=[{"name": "factory-context-mcp"}],
        skills=[{"name": "fastapi-patterns"}],
        agents=[{"role": "Architect"}]
    )
    assert cbom["product"] == "TradingHub"
    assert len(cbom["raw_materials"]) == 1
    assert len(cbom["machinery_tools"]) == 1
    assert len(cbom["mcp_servers"]) == 1
