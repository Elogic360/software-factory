"""
WebSocket ConnectionManager & Channel Broadcast Core
"""
import asyncio
from typing import Dict, Set, Any

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[Any]] = {}

    async def connect(self, channel: str, websocket: Any):
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)

    def disconnect(self, channel: str, websocket: Any):
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
            if not self.active_connections[channel]:
                del self.active_connections[channel]

    async def broadcast(self, channel: str, message: dict):
        if channel in self.active_connections:
            for connection in list(self.active_connections[channel]):
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(channel, connection)
