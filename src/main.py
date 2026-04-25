from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from src.books.routes import books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")

    yield

    print("Shutting down...")


version = "v1"

app = FastAPI(
    version=version,
    title="Bookly API",
    description="A simple API for managing books",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for development (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router, prefix=f"/api/{version}/books", tags=["books"])
