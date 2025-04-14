from fastapi import APIRouter, Query
from app.core.channel_manager import manager

router = APIRouter()

@router.get("/channels", tags=["Channels"])
def search_channels(q: str = Query("")):
    return {"matches": manager.search_channels(q.lower())}
