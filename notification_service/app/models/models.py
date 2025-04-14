from typing import List
from fastapi import WebSocket

class Channel:
    def __init__(self, name: str):
        self.name = name
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, message: str):
        for ws in self.connections:
            await ws.send_text(message)
