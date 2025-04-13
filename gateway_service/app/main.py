from fastapi import FastAPI
from app.controllers import library_proxy
import uvicorn

app = FastAPI(
    title="Gateway Service",
    description="Proxies requests to microservices like library",
    version="1.0.0"
)

app.include_router(library_proxy.router, prefix="/library", tags=["Library"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
