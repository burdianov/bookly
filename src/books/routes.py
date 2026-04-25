from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.books.schemas import Book, BookCreate, BookUpdate
from src.db.main import get_session
from src.books.service import BookService


books_router = APIRouter()
book_service = BookService()


@books_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@books_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    book: BookCreate, session: AsyncSession = Depends(get_session)
) -> Book:
    new_book = await book_service.create_book(session, book)
    return new_book


@books_router.get("/{book_id}", response_model=Book)
async def get_book(book_id: UUID, session: AsyncSession = Depends(get_session)) -> Book:
    book = await book_service.get_book_by_id(session, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@books_router.patch("/{book_id}", response_model=Book)
async def update_book(
    book_id: UUID,
    book_update_data: BookUpdate,
    session: AsyncSession = Depends(get_session),
) -> Book:
    book = await book_service.update_book(session, book_id, book_update_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    book = await book_service.delete_book(session, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
