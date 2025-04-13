from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book_schema import BookCreate
from fastapi import HTTPException

def get_all_books(db: Session):
    return db.query(Book).all()

def get_book_by_id(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def create_book(db: Session, book_data: BookCreate):
    new_book = Book(**book_data.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def update_book(db: Session, book_id: int, book_data: BookCreate):
    book = get_book_by_id(db, book_id)
    for key, value in book_data.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = get_book_by_id(db, book_id)
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
