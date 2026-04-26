from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.schemas import UserCreate, UserRead
from src.auth.utils import generate_password_hash


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):

        statement = select(User).where(func.lower(User.email) == email.lower())
        result = await session.execute(statement)
        return result.scalars().one_or_none()

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(
        self, user_data: UserCreate, session: AsyncSession
    ) -> UserRead:
        email = str(user_data.email).lower()

        if await self.user_exists(email, session):
            raise ValueError("User with this email already exists")

        new_user = User(
            **user_data.model_dump(exclude={"password", "email"}),
            email=email,
            password_hash=generate_password_hash(user_data.password),
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return UserRead.model_validate(new_user)
