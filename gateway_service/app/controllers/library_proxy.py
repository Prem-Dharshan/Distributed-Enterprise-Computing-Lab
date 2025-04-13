import requests
from fastapi import APIRouter, Request, Response, Body
from typing import Optional, Dict

router = APIRouter()

LIBRARY_SERVICE_URL = "http://library-service:8010/library"

def proxy_request(method: str, path: str, request: Request, body: Optional[Dict] = None):
    url = f"{LIBRARY_SERVICE_URL}/{path}"
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}

    try:
        resp = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body,
            params=request.query_params
        )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers={k: v for k, v in resp.headers.items() if k.lower() != "content-encoding"},
            media_type=resp.headers.get("content-type")
        )
    except requests.RequestException as e:
        return Response(content=f"Gateway Error: {str(e)}", status_code=500)

@router.get("/{path:path}")
async def get_proxy(path: str, request: Request):
    return proxy_request("GET", path, request)

@router.post("/{path:path}")
async def post_proxy(path: str, request: Request, body: Optional[Dict] = Body(None)):
    return proxy_request("POST", path, request, body)

@router.put("/{path:path}")
async def put_proxy(path: str, request: Request, body: Optional[Dict] = Body(None)):
    return proxy_request("PUT", path, request, body)

@router.delete("/{path:path}")
async def delete_proxy(path: str, request: Request):
    return proxy_request("DELETE", path, request)
