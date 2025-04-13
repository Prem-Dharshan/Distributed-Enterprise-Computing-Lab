from fastapi import FastAPI
from app.controllers import book_controller
from app.database.db import Base, engine
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management Service",
    description="Lightweight FastAPI microservice for managing library books.",
    version="1.0.0"
)

app.include_router(book_controller.router, prefix="/library", tags=["Books"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8010, reload=True)


#  USAGE:
# 1. Start the service using Docker Compose:
#    docker-compose up --build
# 2. Access the API documentation at: http://localhost:8000/docs
# 3. Use the endpoints to manage books in the library.

# Run it locally too
# 1. Install dependencies:
#    pip install fastapi sqlalchemy uvicorn requests
# 2. Run the application:
#    python main.py
# 3. Access the API documentation at: http://localhost:8000/docs