from fastapi import FastAPI

from src.books.routes import books_router

version = "v1"

app = FastAPI(
    version=version,
    title="Bookly API",
    description="A simple API for managing books",
)

app.include_router(books_router, prefix=f"/api/{version}/books", tags=["books"])
