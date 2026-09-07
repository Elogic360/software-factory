import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.spec_compiler import SpecCompiler

def test_spec_to_plan_compiler():
    spec = {
        "title": "PaymentEngine",
        "functional_requirements": ["Process credit cards", "Handle webhooks"],
        "architecture": {"database": "PostgreSQL"}
    }
    plan = SpecCompiler.compile_spec_to_plan(spec)
    assert plan["total_tasks"] >= 3
    assert plan["tasks"][0]["station"] == "Data Architecture"
    assert any("credit cards" in t["title"] for t in plan["tasks"])
