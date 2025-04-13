from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    available_copies: int

class BookRead(BookCreate):
    id: int

    class Config:
        from_attributes = True
