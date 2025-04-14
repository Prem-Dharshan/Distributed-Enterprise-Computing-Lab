from fastapi import WebSocket
from typing import Dict, List
from app.core.types import ChannelConnections
from app.core.channel_store import load_channels, save_channels

class ChannelManager:
    def __init__(self):
        self.channels: ChannelConnections = {}
        self.persistent_channels = load_channels()

        for channel in self.persistent_channels:
            self.channels[channel] = []

    def get_available_channels(self) -> List[str]:
        return list(self.channels.keys())

    def search_channels(self, query: str) -> List[str]:
        return [c for c in self.channels if c.startswith(query)]

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        if channel not in self.channels:
            self.channels[channel] = []
            save_channels(list(self.channels.keys()))
        self.channels[channel].append(websocket)

    def disconnect(self, websocket: WebSocket, channel: str):
        if channel in self.channels and websocket in self.channels[channel]:
            self.channels[channel].remove(websocket)
            if not self.channels[channel]:
                del self.channels[channel]
                save_channels(list(self.channels.keys()))

    async def broadcast(self, channel: str, message: str):
        if channel in self.channels:
            for conn in self.channels[channel]:
                await conn.send_text(message)

manager = ChannelManager()
