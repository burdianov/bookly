from sqlalchemy.ext.asyncio import create_async_engine

from src.books.models import Book
from src.config import Config


engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True,
)


async def init_db():

    async with engine.begin() as conn:
        await conn.run_sync(Book.metadata.create_all)
