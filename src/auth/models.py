import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, text
import sqlalchemy.dialects.postgresql as pg

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    uid: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    username: Mapped[str] = mapped_column(pg.VARCHAR(255), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(pg.VARCHAR(255), nullable=False)
    last_name: Mapped[str] = mapped_column(pg.VARCHAR(255), nullable=False)
    email: Mapped[str] = mapped_column(pg.VARCHAR(255), nullable=False, unique=True)
    is_verified: Mapped[bool] = mapped_column(pg.BOOLEAN, nullable=True, default=False)
    password_hash: Mapped[str] = mapped_column(pg.VARCHAR(255), nullable=False)

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
