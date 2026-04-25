from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.models import Book
from src.books.schemas import BookCreate, BookUpdate


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(Book.created_at.desc())
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_book_by_id(self, session: AsyncSession, book_id: UUID):
        return await session.get(Book, book_id)

    async def create_book(self, session: AsyncSession, book: BookCreate):
        db_book = Book(**book.model_dump())

        session.add(db_book)
        await session.commit()
        await session.refresh(db_book)

        return db_book

    async def update_book(
        self,
        session: AsyncSession,
        book_id: UUID,
        book: BookUpdate,
    ):
        db_book = await session.get(Book, book_id)

        if not db_book:
            return None

        update_data = book.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_book, key, value)

        await session.commit()
        await session.refresh(db_book)

        return db_book

    async def delete_book(self, session: AsyncSession, book_id: UUID):
        db_book = await session.get(Book, book_id)

        if not db_book:
            return None

        await session.delete(db_book)
        await session.commit()

        return db_book
