from datetime import datetime, timedelta, timezone
from typing import Optional
import logging

from passlib.context import CryptContext
import jwt
import uuid

from src.config import Config

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

ACCESS_TOKEN_EXPIRY = timedelta(minutes=60)


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(
    user_data: dict,
    expiry: Optional[timedelta] = None,
    refresh: bool = False,
) -> str:
    expires_at = datetime.now(timezone.utc) + (expiry or ACCESS_TOKEN_EXPIRY)

    payload = {
        "user": user_data,
        "exp": int(expires_at.timestamp()),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    return jwt.encode(
        payload,
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> Optional[dict]:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
