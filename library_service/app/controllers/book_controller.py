from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import SessionLocal
from app.schemas.book_schema import BookCreate, BookRead
from app.services import book_service
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books", response_model=List[BookRead], summary="Get all books")
def get_books(db: Session = Depends(get_db)):
    return book_service.get_all_books(db)

@router.get("/books/{book_id}", response_model=BookRead, summary="Get book by ID")
def get_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.get_book_by_id(db, book_id)

@router.post("/books", response_model=BookRead, summary="Add a new book")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_service.create_book(db, book)

@router.put("/books/{book_id}", response_model=BookRead, summary="Update book details")
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    return book_service.update_book(db, book_id, book)

@router.delete("/books/{book_id}", summary="Delete a book")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return book_service.delete_book(db, book_id)
