from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import UserRole
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.domains.users.model import User
from app.domains.users.schema import (
    Token,
    UserCreate,
)


class EmailAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class UserInactiveError(Exception):
    pass


class UserService:

    @staticmethod
    async def create_user(
        db: AsyncSession,
        user_in: UserCreate,
    ) -> User:

        existing_user = await db.scalar(
            select(User).where(
                User.email == user_in.email
            )
        )

        if existing_user:
            raise EmailAlreadyExistsError()

        user = User(
            name=user_in.name,
            email=user_in.email,
            hashed_password=hash_password(
                user_in.password
            ),
            role=UserRole.USER,
            is_active=True,
        )

        try:
            db.add(user)
            await db.commit()
            await db.refresh(user)

            return user

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str,
    ) -> User | None:

        user = await db.scalar(
            select(User).where(
                User.email == email
            )
        )

        if not user:
            return None

        if not user.is_active:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user

    @staticmethod
    async def login(
        db: AsyncSession,
        email: str,
        password: str,
    ) -> Token:

        user = await UserService.authenticate_user(
            db=db,
            email=email,
            password=password,
        )

        if not user:
            raise InvalidCredentialsError()

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.value,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "role": user.role.value,
            }
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        user_id: int,
    ) -> User | None:

        return await db.scalar(
            select(User).where(
                User.id == user_id
            )
        )