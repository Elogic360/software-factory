"""
Software Factory Capability Warehouse Inventory Engine.
Indexes, validates, and manages all 15 warehouse categories.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

WAREHOUSE_CATEGORIES = [
    "skills",
    "mcp",
    "plugins",
    "tools",
    "agents",
    "harnesses",
    "libraries",
    "frameworks",
    "templates",
    "datasets",
    "benchmarks",
    "documentation",
    "patterns",
    "raw-materials",
    "domain-packs"
]

class CapabilityWarehouse:
    """Warehouse inventory controller."""

    def __init__(self, root_path: Optional[str] = None):
        if root_path is None:
            self.root_path = Path(__file__).resolve().parent.parent / "warehouse"
        else:
            self.root_path = Path(root_path)
        self.root_path.mkdir(parents=True, exist_ok=True)
        for cat in WAREHOUSE_CATEGORIES:
            (self.root_path / cat).mkdir(parents=True, exist_ok=True)

    def list_inventory(self) -> Dict[str, int]:
        """Returns count of manifests across all categories."""
        inventory = {}
        for cat in WAREHOUSE_CATEGORIES:
            cat_dir = self.root_path / cat
            manifests = list(cat_dir.glob("*.json")) + list(cat_dir.glob("*.yaml")) + list(cat_dir.glob("*.yml"))
            inventory[cat] = len(manifests)
        return inventory

    def register_item(self, category: str, item_id: str, manifest_data: Dict[str, Any]) -> Path:
        """Registers a capability manifest into the warehouse category."""
        if category not in WAREHOUSE_CATEGORIES:
            raise ValueError(f"Invalid category '{category}'. Valid: {WAREHOUSE_CATEGORIES}")

        target_file = self.root_path / category / f"{item_id}.yaml"
        with open(target_file, "w", encoding="utf-8") as f:
            yaml.dump(manifest_data, f, default_flow_style=False)
        return target_file

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Searches across all warehouse manifests."""
        results = []
        q_lower = query.lower()
        for cat in WAREHOUSE_CATEGORIES:
            cat_dir = self.root_path / cat
            for file_path in list(cat_dir.glob("*.yaml")) + list(cat_dir.glob("*.json")):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        if file_path.suffix in [".yaml", ".yml"]:
                            data = yaml.safe_load(f)
                        else:
                            data = json.load(f)
                    if isinstance(data, dict):
                        text = json.dumps(data).lower()
                        if q_lower in text:
                            results.append({
                                "category": cat,
                                "file": file_path.name,
                                "id": data.get("id", file_path.stem),
                                "name": data.get("name", file_path.stem),
                                "version": data.get("version", "1.0")
                            })
                except Exception:
                    continue
        return results
