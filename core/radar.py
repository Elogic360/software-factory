"""
core/radar.py — Factory Radar Continuous Ecosystem Discovery Engine
Discovers new open-source repositories, agent skills, MCP servers, frameworks,
and categorizes them across development domains.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

SF_ROOT = Path(__file__).resolve().parent.parent
RADAR_CACHE = SF_ROOT / "cache" / "radar_cache.json"

# Curated Ecosystem Sources
ECOSYSTEM_SEEDS = [
    {"repo": "affaan-m/ECC", "category": "agent", "type": "skill-pack", "signals": ["agent-harness", "skills"]},
    {"repo": "colbymchenry/codegraph", "category": "intelligence", "type": "mcp-server", "signals": ["ast-graph", "token-savings"]},
    {"repo": "rtk-ai/rtk", "category": "coding", "type": "cli-tool", "signals": ["token-optimizer", "rust"]},
    {"repo": "goldmansachs/gs-quant", "category": "quant", "type": "library", "signals": ["derivatives", "pricing"]},
    {"repo": "Limex-com/ziplime", "category": "quant", "type": "quant-tool", "signals": ["polars", "backtesting", "mcp"]},
    {"repo": "D4Vinci/Scrapling", "category": "browser", "type": "browser-tool", "signals": ["stealth", "scraping"]},
    {"repo": "sparklabx/drawio-ai-kit", "category": "architecture", "type": "design-system", "signals": ["drawio", "diagrams"]},
    {"repo": "elementalsouls/Claude-BugHunter", "category": "security", "type": "security-tool", "signals": ["redteam", "sast"]},
    {"repo": "prowler-cloud/prowler", "category": "security", "type": "security-tool", "signals": ["cloud-audit", "compliance"]},
    {"repo": "vibrantlabsai/ragas", "category": "ai", "type": "testing-tool", "signals": ["rag-eval", "llm-metrics"]},
    {"repo": "ucbepic/docetl", "category": "data", "type": "data-tool", "signals": ["agentic-etl", "document-processing"]},
    {"repo": "huggingface/transformers", "category": "ai", "type": "framework", "signals": ["sota-models", "multimodal"]},
    {"repo": "run-llama/llama_index", "category": "ai", "type": "framework", "signals": ["rag", "document-agents"]},
    {"repo": "langchain-ai/langchain", "category": "ai", "type": "framework", "signals": ["agents", "tool-chains"]},
    {"repo": "quickfix/quickfix", "category": "quant", "type": "library", "signals": ["fix-protocol", "low-latency"]},
    {"repo": "alpacahq/alpaca-py", "category": "quant", "type": "library", "signals": ["broker-api", "websockets"]},
    {"repo": "hieunc229/mailflare", "category": "devops", "type": "raw-material", "signals": ["email-system", "cloudflare-workers"]}
]

class FactoryRadar:
    def __init__(self, cache_file: Optional[Path] = None):
        self.cache_file = cache_file or RADAR_CACHE
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.tracked_items: List[Dict[str, Any]] = self._load_cache()

    def _load_cache(self) -> List[Dict[str, Any]]:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return ECOSYSTEM_SEEDS

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.tracked_items, f, indent=2)

    def scan(self, period: str = "daily", category: Optional[str] = None) -> List[Dict[str, Any]]:
        results = []
        for item in self.tracked_items:
            if category and item.get("category") != category:
                continue
            
            status = "RELEVANT"
            if item.get("repo") in ["affaan-m/ECC", "colbymchenry/codegraph"]:
                status = "BREAKTHROUGH"
            elif item.get("category") == "quant":
                status = "RISING"

            results.append({
                "repo": item.get("repo"),
                "category": item.get("category"),
                "type": item.get("type"),
                "radar_status": status,
                "signals": item.get("signals", []),
                "period": period
            })
        return results

    def add_target(self, repo: str, category: str, item_type: str, signals: List[str]) -> bool:
        if not any(i.get("repo") == repo for i in self.tracked_items):
            self.tracked_items.append({
                "repo": repo,
                "category": category,
                "type": item_type,
                "signals": signals
            })
            self._save_cache()
            return True
        return False
