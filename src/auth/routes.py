from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from src.auth.schemas import UserCreate, UserLogin, UserRead
from src.db.main import get_session
from src.auth.service import UserService
from src.auth.utils import create_access_token, verify_password


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
