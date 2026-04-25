from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.books.routes import books_router
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")

    await init_db()

    yield

    print("Shutting down...")


version = "v1"

app = FastAPI(
    version=version,
    title="Bookly API",
    description="A simple API for managing books",
    lifespan=lifespan,
)

app.include_router(books_router, prefix=f"/api/{version}/books", tags=["books"])
