from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

from src.auth.schemas import UserCreate, UserLogin, UserRead
from src.db.main import get_session
from src.auth.service import UserService
from src.auth.utils import create_access_token, verify_password
from src.auth.dependencies import RefreshTokenBearer


auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = timedelta(days=7)


@auth_router.post(
    "/signup",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_account(
    user: UserCreate, session: AsyncSession = Depends(get_session)
):
    email = str(user.email).lower()
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with this email already exists",
        )

    new_user = await user_service.create_user(user, session)

    return new_user


@auth_router.post("/login")
async def login(login_data: UserLogin, session: AsyncSession = Depends(get_session)):
    email = str(login_data.email).lower()
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user:
        is_password_valid = verify_password(password, user.password_hash)

        if is_password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_id": str(user.uid),
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_id": str(user.uid),
                },
                expiry=REFRESH_TOKEN_EXPIRY,
                refresh=True,
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "email": user.email,
                        "user_id": str(user.uid),
                    },
                }
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password",
        )


@auth_router.get("/refresh_token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()),
):
    user_data = token_details.get("user")

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token",
        )

    new_access_token = create_access_token(
        user_data=user_data,
    )

    return JSONResponse(
        content={
            "access_token": new_access_token,
        }
    )
