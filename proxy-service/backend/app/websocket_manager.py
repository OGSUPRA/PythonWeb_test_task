from collections import defaultdict
from datetime import datetime
from typing import Optional

from fastapi import WebSocket

from app import models


class ConnectionStatusManager:
    def __init__(self):
        self.active_connections: dict[int, set[WebSocket]] = defaultdict(set)
        self.statuses: dict[int, dict] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id].add(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id not in self.active_connections:
            return

        self.active_connections[user_id].discard(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def broadcast_status(
        self,
        user_id: int,
        status: str,
        message: str,
        vm: Optional[models.VirtualMachine] = None,
    ):
        payload = self._build_payload(user_id, status, message, vm)
        self.statuses[user_id] = payload

        stale_connections = []
        for websocket in self.active_connections.get(user_id, set()):
            try:
                await websocket.send_json(payload)
            except Exception:
                stale_connections.append(websocket)

        for websocket in stale_connections:
            self.disconnect(user_id, websocket)

        return payload

    async def send_current_status(self, user_id: int, websocket: WebSocket):
        await websocket.send_json(self.get_status(user_id))

    def get_status(self, user_id: int):
        return self.statuses.get(
            user_id,
            self._build_payload(
                user_id=user_id,
                status="waiting",
                message="Waiting for proxy assignment",
                vm=None,
            ),
        )

    def _build_payload(
        self,
        user_id: int,
        status: str,
        message: str,
        vm: Optional[models.VirtualMachine] = None,
    ):
        vm_payload = None
        if vm is not None:
            vm_payload = {
                "name": vm.name,
                "host": vm.host,
                "port": vm.port,
                "protocol": vm.protocol,
            }

        return {
            "user_id": user_id,
            "status": status,
            "message": message,
            "vm": vm_payload,
            "updated_at": datetime.utcnow().isoformat(),
        }


status_manager = ConnectionStatusManager()
