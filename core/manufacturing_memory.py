"""
Software Factory Manufacturing Memory & Production Ledger.
Tracks 12 distinct memory dimensions and end-to-end product genealogy.
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

MEMORY_DIMENSIONS = [
    "PROJECT",
    "ARCHITECTURE",
    "DECISION",
    "REQUIREMENT",
    "TASK",
    "AGENT",
    "SKILL",
    "FAILURE",
    "TEST",
    "SECURITY",
    "DEPLOYMENT",
    "INCIDENT"
]

class ManufacturingMemoryLedger:
    """Enterprise 12-dimensional manufacturing memory and genealogy ledger."""

    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir is None:
            self.storage_dir = Path(__file__).resolve().parent.parent / "memory" / "manufacturing_ledger"
        else:
            self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.ledger_file = self.storage_dir / "production_ledger.json"
        self._init_storage()

    def _init_storage(self):
        if not self.ledger_file.exists():
            data = {
                "version": "1.0",
                "dimensions": {dim: [] for dim in MEMORY_DIMENSIONS},
                "genealogy": []
            }
            self._save(data)

    def _load(self) -> Dict[str, Any]:
        try:
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"version": "1.0", "dimensions": {dim: [] for dim in MEMORY_DIMENSIONS}, "genealogy": []}

    def _save(self, data: Dict[str, Any]):
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def record_entry(self, dimension: str, topic: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Records a new entry in a specific memory dimension."""
        dim_upper = dimension.upper()
        if dim_upper not in MEMORY_DIMENSIONS:
            raise ValueError(f"Invalid memory dimension '{dimension}'. Valid: {MEMORY_DIMENSIONS}")

        entry = {
            "id": f"{dim_upper.lower()}-{int(time.time()*1000)}",
            "timestamp": time.time(),
            "topic": topic,
            "content": content,
            "metadata": metadata or {}
        }

        data = self._load()
        data["dimensions"][dim_upper].append(entry)
        self._save(data)
        return entry

    def query_dimension(self, dimension: str, query: str = "") -> List[Dict[str, Any]]:
        """Queries memory entries within a dimension with optional keyword filtering."""
        dim_upper = dimension.upper()
        if dim_upper not in MEMORY_DIMENSIONS:
            return []
        data = self._load()
        entries = data["dimensions"].get(dim_upper, [])
        if not query:
            return entries
        q_lower = query.lower()
        return [
            e for e in entries
            if q_lower in e["topic"].lower() or q_lower in e["content"].lower()
        ]

    def record_genealogy_node(self, product: str, release: str, commit_sha: str, task_id: str,
                              agent: str, skill: str, mcp: str, raw_material: str, upstream_license: str) -> Dict[str, Any]:
        """Records full manufacturing genealogy node."""
        node = {
            "product": product,
            "release": release,
            "commit_sha": commit_sha,
            "task_id": task_id,
            "agent": agent,
            "skill": skill,
            "mcp": mcp,
            "raw_material": raw_material,
            "upstream_license": upstream_license,
            "recorded_at": time.time()
        }
        data = self._load()
        data["genealogy"].append(node)
        self._save(data)
        return node

    def trace_genealogy(self, product: str) -> List[Dict[str, Any]]:
        """Traces the entire lineage and dependencies for a manufactured product."""
        data = self._load()
        return [g for g in data.get("genealogy", []) if g.get("product") == product]
