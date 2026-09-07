"""
Software Factory Central Multi-Neuron Memory System.
Manages 28 specialized memory neurons across Global, Project, Task, and Session scopes.
Provides Memory Router, Promotion Pipeline, Quality Control, and 12 executable memory verbs:
remember, recall, search, retrieve, summarize, link, promote, demote, invalidate, supersede, forget, archive.
"""

import json
import time
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

MEMORY_NEURONS = [
    "Project", "Architecture", "Specification", "Decision", "Task",
    "Implementation", "CodeKnowledge", "Component", "Skill", "MCP",
    "Tool", "Documentation", "Dependency", "Test", "Failure",
    "Incident", "Deployment", "Security", "Performance", "UX",
    "Domain", "Agent", "Prompt", "Context", "Loop",
    "Research", "Learning", "Factory"
]

FORBIDDEN_PATTERNS = [
    r"bearer\s+[a-zA-Z0-9_\-\.]{20,}",
    r"ghp_[a-zA-Z0-9]{36}",
    r"sk-[a-zA-Z0-9]{20,}",
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"aws_secret_access_key\s*=",
    r"password\s*[:=]\s*['\"][^'\"]{6,}['\"]",
]

class MemoryNeuron:
    """Represents an active memory node with confidence, provenance, and lifecycle."""

    def __init__(self, neuron_type: str, scope: str = "PROJECT", project_id: str = "default"):
        self.neuron_type = neuron_type
        self.scope = scope  # GLOBAL, PROJECT, TEAM, USER, TASK, SESSION
        self.project_id = project_id
        self.records: List[Dict[str, Any]] = []

    def add(
        self,
        topic: str,
        content: str,
        provenance: str = "agent",
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        entry = {
            "id": f"{self.neuron_type.lower()}-{int(time.time()*1000)}-{len(self.records)+1}",
            "neuron": self.neuron_type,
            "scope": self.scope,
            "project_id": self.project_id,
            "topic": topic,
            "content": content,
            "provenance": provenance,
            "confidence": max(0.0, min(1.0, confidence)),
            "timestamp": time.time(),
            "updated_at": time.time(),
            "status": "ACTIVE",  # ACTIVE, SUPERSEDED, ARCHIVED, PROMOTED, INVALIDATED
            "metadata": metadata or {},
            "links": []
        }
        self.records.append(entry)
        return entry

class CentralEngineeringMemory:
    """Master Multi-Neuron Memory Controller with Router and Promotion Pipeline."""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent / "memory" / "central_neurons"
        else:
            self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.neurons: Dict[str, MemoryNeuron] = {}
        self._init_neurons()
        self._load_all()

    def _init_neurons(self, project_id: str = "default"):
        for n_type in MEMORY_NEURONS:
            key = f"{project_id}:{n_type}"
            if key not in self.neurons:
                self.neurons[key] = MemoryNeuron(n_type, scope="PROJECT", project_id=project_id)

    def _get_neuron_file(self, project_id: str, neuron_type: str) -> Path:
        proj_dir = self.base_dir / project_id
        proj_dir.mkdir(parents=True, exist_ok=True)
        return proj_dir / f"{neuron_type.lower()}_neuron.json"

    def _save_neuron(self, project_id: str, neuron_type: str):
        key = f"{project_id}:{neuron_type}"
        neuron = self.neurons.get(key)
        if not neuron:
            return
        file_path = self._get_neuron_file(project_id, neuron_type)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([r for r in neuron.records], f, indent=2)

    def _load_all(self):
        for proj_dir in self.base_dir.iterdir():
            if proj_dir.is_dir():
                project_id = proj_dir.name
                self._init_neurons(project_id)
                for f in proj_dir.glob("*_neuron.json"):
                    n_type = f.stem.replace("_neuron", "").capitalize()
                    matching_neuron = next((nt for nt in MEMORY_NEURONS if nt.lower() == n_type.lower()), None)
                    if matching_neuron:
                        key = f"{project_id}:{matching_neuron}"
                        try:
                            with open(f, "r", encoding="utf-8") as nf:
                                data = json.load(nf)
                                if isinstance(data, list):
                                    self.neurons[key].records = data
                        except Exception:
                            continue

    def is_safe_to_remember(self, content: str, topic: str = "") -> bool:
        """Enforces security boundaries: blocks secrets, credentials, and API keys."""
        combined = f"{topic} {content}"
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, combined, re.IGNORECASE):
                return False
        return True

    # ── 12 Executable Memory Verbs ──────────────────────────────────────────

    def remember(
        self,
        neuron_type: str,
        topic: str,
        content: str,
        project_id: str = "default",
        provenance: str = "agent",
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """1. remember(): Safely adds record with secret filtering and deduplication."""
        if not self.is_safe_to_remember(content, topic):
            raise ValueError("Security violation: Memory content contains secrets, tokens, or credentials.")

        self._init_neurons(project_id)
        matching_nt = next((nt for nt in MEMORY_NEURONS if nt.lower() == neuron_type.lower()), "Factory")
        key = f"{project_id}:{matching_nt}"

        # Dedup check
        for r in self.neurons[key].records:
            if r["topic"].lower() == topic.lower() and r["content"].strip() == content.strip():
                r["updated_at"] = time.time()
                self._save_neuron(project_id, matching_nt)
                return r

        entry = self.neurons[key].add(topic, content, provenance=provenance, confidence=confidence, metadata=metadata)
        self._save_neuron(project_id, matching_nt)
        return entry

    def recall(self, neuron_type: str, topic_or_id: str, project_id: str = "default") -> Optional[Dict[str, Any]]:
        """2. recall(): Finds exact matching record by ID or topic."""
        self._init_neurons(project_id)
        matching_nt = next((nt for nt in MEMORY_NEURONS if nt.lower() == neuron_type.lower()), None)
        if not matching_nt:
            return None
        key = f"{project_id}:{matching_nt}"
        for r in self.neurons[key].records:
            if r["id"] == topic_or_id or r["topic"].lower() == topic_or_id.lower():
                return r
        return None

    def search(
        self,
        query: str,
        project_id: str = "default",
        neuron_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """3. search(): Full-text keyword search across active neuron records."""
        self._init_neurons(project_id)
        q_lower = query.lower()
        results = []
        target_neurons = neuron_types or MEMORY_NEURONS
        for nt in target_neurons:
            matching_nt = next((n for n in MEMORY_NEURONS if n.lower() == nt.lower()), None)
            if not matching_nt:
                continue
            key = f"{project_id}:{matching_nt}"
            for r in self.neurons.get(key, MemoryNeuron(matching_nt)).records:
                if r.get("status") in ["ARCHIVED", "INVALIDATED"]:
                    continue
                if q_lower in r["topic"].lower() or q_lower in r["content"].lower():
                    results.append(r)
        return results

    def retrieve(self, query: str, project_id: str = "default", limit: int = 5) -> List[Dict[str, Any]]:
        """4. retrieve(): Relevance-ranked memory retrieval with limit."""
        hits = self.search(query, project_id=project_id)
        hits.sort(key=lambda x: x.get("confidence", 1.0), reverse=True)
        return hits[:limit]

    def summarize(self, neuron_type: str, project_id: str = "default") -> Dict[str, Any]:
        """5. summarize(): Produces high-level summary of a neuron's contents."""
        self._init_neurons(project_id)
        matching_nt = next((nt for nt in MEMORY_NEURONS if nt.lower() == neuron_type.lower()), None)
        if not matching_nt:
            return {"neuron": neuron_type, "total": 0, "topics": []}
        key = f"{project_id}:{matching_nt}"
        records = [r for r in self.neurons[key].records if r.get("status") == "ACTIVE"]
        return {
            "neuron": matching_nt,
            "project_id": project_id,
            "active_count": len(records),
            "topics": [r["topic"] for r in records],
            "average_confidence": round(sum(r["confidence"] for r in records) / len(records), 2) if records else 1.0
        }

    def link(self, source_id: str, target_id: str, relation: str, project_id: str = "default") -> bool:
        """6. link(): Links two memory nodes across neurons with relationship semantics."""
        self._init_neurons(project_id)
        found = False
        for key, neuron in self.neurons.items():
            if key.startswith(f"{project_id}:"):
                for r in neuron.records:
                    if r["id"] == source_id:
                        r["links"].append({"target": target_id, "relation": relation, "timestamp": time.time()})
                        self._save_neuron(project_id, neuron.neuron_type)
                        found = True
                        break
        return found

    def promote(self, source_id: str, project_id: str = "default", target_scope: str = "GLOBAL") -> Optional[Dict[str, Any]]:
        """7. promote(): Promotes validated project memory to global factory knowledge."""
        for key, neuron in self.neurons.items():
            if key.startswith(f"{project_id}:"):
                for r in neuron.records:
                    if r["id"] == source_id:
                        global_entry = self.remember(
                            neuron_type="Factory",
                            topic=f"[Promoted] {r['topic']}",
                            content=r["content"],
                            project_id="global",
                            provenance=f"promoted_from:{project_id}:{source_id}",
                            confidence=1.0,
                            metadata={"original_metadata": r.get("metadata", {}), "target_scope": target_scope}
                        )
                        r["status"] = "PROMOTED"
                        self._save_neuron(project_id, neuron.neuron_type)
                        return global_entry
        return None

    def demote(self, record_id: str, project_id: str = "default") -> bool:
        """8. demote(): Lowers confidence of a record due to uncertainty or conflict."""
        for key, neuron in self.neurons.items():
            if key.startswith(f"{project_id}:"):
                for r in neuron.records:
                    if r["id"] == record_id:
                        r["confidence"] = max(0.1, r["confidence"] - 0.3)
                        r["updated_at"] = time.time()
                        self._save_neuron(project_id, neuron.neuron_type)
                        return True
        return False

    def invalidate(self, record_id: str, reason: str = "", project_id: str = "default") -> bool:
        """9. invalidate(): Flags record as invalid or contradicted by new findings."""
        for key, neuron in self.neurons.items():
            if key.startswith(f"{project_id}:"):
                for r in neuron.records:
                    if r["id"] == record_id:
                        r["status"] = "INVALIDATED"
                        r["invalidation_reason"] = reason
                        r["updated_at"] = time.time()
                        self._save_neuron(project_id, neuron.neuron_type)
                        return True
        return False

    def supersede(self, old_record_id: str, new_record_id: str, project_id: str = "default") -> bool:
        """10. supersede(): Marks old record as superseded by a newer version."""
        for key, neuron in self.neurons.items():
            if key.startswith(f"{project_id}:"):
                for r in neuron.records:
                    if r["id"] == old_record_id:
                        r["status"] = "SUPERSEDED"
                        r["superseded_by"] = new_record_id
                        r["updated_at"] = time.time()
                        self._save_neuron(project_id, neuron.neuron_type)
                        return True
        return False

    def forget(self, record_id: str, project_id: str = "default") -> bool:
        """11. forget(): Permanently deletes record."""
        for key, neuron in self.neurons.items():
            if key.startswith(f"{project_id}:"):
                initial_len = len(neuron.records)
                neuron.records = [r for r in neuron.records if r["id"] != record_id]
                if len(neuron.records) < initial_len:
                    self._save_neuron(project_id, neuron.neuron_type)
                    return True
        return False

    def archive(self, record_id: str, project_id: str = "default") -> bool:
        """12. archive(): Moves record to inactive archive status without deletion."""
        for key, neuron in self.neurons.items():
            if key.startswith(f"{project_id}:"):
                for r in neuron.records:
                    if r["id"] == record_id:
                        r["status"] = "ARCHIVED"
                        r["updated_at"] = time.time()
                        self._save_neuron(project_id, neuron.neuron_type)
                        return True
        return False

    # ── Memory Router ────────────────────────────────────────────────────────

    def route_query(self, query: str, project_id: str = "default") -> Dict[str, Any]:
        """Determines what knowledge is needed and retrieves minimal high-precision context."""
        q_lower = query.lower()
        selected_neurons = []
        if any(w in q_lower for w in ["auth", "login", "jwt", "session", "security", "role", "rbac"]):
            selected_neurons.extend(["Security", "Architecture", "Component", "Decision"])
        elif any(w in q_lower for w in ["db", "database", "postgres", "sql", "migration", "schema"]):
            selected_neurons.extend(["Architecture", "Dependency", "Component", "CodeKnowledge"])
        elif any(w in q_lower for w in ["test", "e2e", "unit", "coverage", "mock"]):
            selected_neurons.extend(["Test", "Quality", "Failure"])
        elif any(w in q_lower for w in ["fail", "error", "bug", "crash", "incident", "rca"]):
            selected_neurons.extend(["Failure", "Incident", "Decision"])
        else:
            selected_neurons.extend(["Project", "Architecture", "Specification", "Decision"])

        selected_neurons = list(set(selected_neurons))
        project_hits = self.search(query, project_id=project_id, neuron_types=selected_neurons)
        global_hits = self.search(query, project_id="global", neuron_types=["Factory", "Skill", "Component"])

        return {
            "query": query,
            "routed_neurons": selected_neurons,
            "project_context": project_hits,
            "global_factory_context": global_hits,
            "total_records_retrieved": len(project_hits) + len(global_hits)
        }

    # ── Centralization & Project Discovery Ingestion ─────────────────────────

    def ingest_existing_project(self, project_root: str, project_id: str) -> Dict[str, Any]:
        """Scans project directory for docs, ADRs, specs, configs, and centralizes them."""
        p_root = Path(project_root)
        discovered = {"docs": 0, "specs": 0, "adrs": 0, "schemas": 0}
        if not p_root.exists():
            return discovered

        for md_file in p_root.glob("**/*.md"):
            if ".factory" in str(md_file) or "node_modules" in str(md_file) or ".git" in str(md_file):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                name_lower = md_file.name.lower()
                if "adr" in str(md_file).lower() or "decision" in name_lower:
                    self.remember("Decision", md_file.stem, content[:2000], project_id=project_id, provenance=str(md_file))
                    discovered["adrs"] += 1
                elif "spec" in name_lower or "prd" in name_lower or "requirement" in name_lower:
                    self.remember("Specification", md_file.stem, content[:2000], project_id=project_id, provenance=str(md_file))
                    discovered["specs"] += 1
                elif "arch" in name_lower or "design" in name_lower:
                    self.remember("Architecture", md_file.stem, content[:2000], project_id=project_id, provenance=str(md_file))
                    discovered["docs"] += 1
                else:
                    self.remember("Documentation", md_file.stem, content[:1500], project_id=project_id, provenance=str(md_file))
                    discovered["docs"] += 1
            except Exception:
                continue

        return discovered
