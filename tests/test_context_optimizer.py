import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.context_optimizer import ContextOptimizer

def test_context_optimizer_deduplication():
    opt = ContextOptimizer()
    blocks = [
        "Duplicate block of text.",
        "Duplicate block of text.",
        "Unique block of text."
    ]
    deduped = opt.deduplicate(blocks)
    assert len(deduped) == 2
    assert "Unique block of text." in deduped

def test_context_optimizer_budget_and_metrics():
    opt = ContextOptimizer()
    sources = [
        {"title": "Doc1", "content": "FastAPI async endpoints and OpenAPI generation.", "priority": 2.0},
        {"title": "Doc2", "content": "PostgreSQL database migrations with alembic.", "priority": 1.0},
        {"title": "Doc3", "content": "Irrelevant noise repeated many times.", "priority": 0.1}
    ]
    res = opt.optimize_context("fastapi openapi", sources, token_budget=50)
    assert "optimized_context" in res
    assert res["metrics"]["tokens_after"] <= 50
    assert res["metrics"]["cost_saved_usd"] >= 0.0
