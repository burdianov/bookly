from alembic.environment import Optional
from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime


class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=3, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


class UserRead(BaseModel):
    uid: uuid.UUID
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
