from typing import Dict, List
from fastapi import WebSocket

ChannelConnections = Dict[str, List[WebSocket]]
