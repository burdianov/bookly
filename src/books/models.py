import uuid
from datetime import date, datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, text
import sqlalchemy.dialects.postgresql as pg


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    uid: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),  # 🔥 DB generates UUID
    )

    title: Mapped[str] = mapped_column(pg.VARCHAR(255), nullable=False)
    author: Mapped[str] = mapped_column(pg.VARCHAR(255), nullable=False)
    publisher: Mapped[str] = mapped_column(pg.VARCHAR(255), nullable=False)

    published_date: Mapped[date] = mapped_column(pg.DATE, nullable=False)
    page_count: Mapped[int] = mapped_column(pg.INTEGER, nullable=False)
    language: Mapped[str] = mapped_column(pg.VARCHAR(20), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        pg.TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        pg.TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
