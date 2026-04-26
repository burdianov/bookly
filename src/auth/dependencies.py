from typing import Any

from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.utils import decode_access_token


class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> dict[str, Any]:  # type: ignore[override]
        creds: HTTPAuthorizationCredentials | None = await super().__call__(request)

        if creds is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authenticated",
            )

        if creds.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme",
            )

        token_data = decode_access_token(creds.credentials)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
            )

        self.verify_token_data(token_data)

        return token_data

    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        raise NotImplementedError("Override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        if token_data.get("refresh") is True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide an access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict[str, Any]) -> None:
        if token_data.get("refresh") is not True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provide a refresh token",
            )
