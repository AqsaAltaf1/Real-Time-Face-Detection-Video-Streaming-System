from typing import Any

from fastapi import WebSocket


class WebSocketHub:
    """Connection manager for websocket stream consumers."""

    def __init__(self) -> None:
        self.clients: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.clients.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.clients.discard(websocket)

    async def broadcast(self, payload: dict[str, Any]) -> None:
        disconnected: list[WebSocket] = []
        for client in self.clients:
            try:
                await client.send_json(payload)
            except RuntimeError:
                disconnected.append(client)

        for client in disconnected:
            self.disconnect(client)
