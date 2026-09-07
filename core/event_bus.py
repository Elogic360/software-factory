"""
Software Factory Event Bus.
Asynchronous pub/sub event distribution for all factory and manufacturing lifecycle events.
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional

LIFECYCLE_EVENTS = [
    "project.created",
    "memory.created",
    "spec.created",
    "architecture.created",
    "plan.created",
    "task.created",
    "task.completed",
    "test.completed",
    "evidence.created",
    "gate.passed",
    "gate.failed",
    "release.created",
    "deployment.started",
    "deployment.completed",
    "deployment.failed",
    "rollback.started",
    "rollback.completed",
    "failure.recorded",
    "learning.created",
    "component.promoted",
    "skill.updated",
    "mcp.updated"
]

class FactoryEventBus:
    """Central event bus with filesystem journal persistence."""

    def __init__(self, log_dir: Optional[str] = None):
        if log_dir is None:
            self.log_dir = Path(__file__).resolve().parent.parent / "logs" / "events"
        else:
            self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.journal_file = self.log_dir / "factory_event_journal.jsonl"
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def emit(self, event_type: str, payload: Dict[str, Any], source: str = "factory-core") -> Dict[str, Any]:
        event = {
            "event_id": f"evt-{int(time.time()*1000)}",
            "event_type": event_type,
            "source": source,
            "timestamp": time.time(),
            "payload": payload
        }

        # Write to journal
        with open(self.journal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")

        # Notify subscribers
        for handler in self._subscribers.get(event_type, []):
            try:
                handler(event)
            except Exception:
                pass

        # Wildcard subscribers
        for handler in self._subscribers.get("*", []):
            try:
                handler(event)
            except Exception:
                pass

        return event

    def replay_events(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if not self.journal_file.exists():
            return []
        events = []
        with open(self.journal_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if event_type is None or data.get("event_type") == event_type:
                        events.append(data)
                except Exception:
                    continue
        return events
