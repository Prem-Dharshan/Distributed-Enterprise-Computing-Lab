from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.core.channel_manager import manager
from app.routers import channels
import uvicorn

app = FastAPI(
    title="Notification Service",
    description="WebSocket broadcasting with channel-based subscriptions",
    version="1.0.0"
)

app.include_router(channels.router)

@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await manager.connect(websocket, channel)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(channel, f"[{channel}] {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8020, reload=True)
