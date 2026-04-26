from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserCreate, UserRead
from src.db.main import get_session
from src.auth.service import UserService


auth_router = APIRouter()
user_service = UserService()


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
