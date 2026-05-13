from sqlalchemy.ext.asyncio import AsyncSession

from app.users import repository
from app.users.model import User
from app.core.enums import UserRole
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


# -------------------------
# user create
# -------------------------

async def create_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> tuple[User | None, str | None]:
    existing = await repository.get_user_by_email(db, email)

    if existing:
        return None, "Email already registered"

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.USER,
        is_active=True,
    )

    created_user = await repository.create_user(db, user)

    return created_user, None


# -------------------------
# login
# -------------------------

async def login_user(
    db: AsyncSession,
    email: str,
    password: str,
):
    print("===== LOGIN START =====")
    print("input email:", email)
    print("input password:", password)

    user = await repository.get_user_by_email(db, email)

    print("user:", user)

    if not user:
        print("USER NOT FOUND")
        return None, "Invalid credentials"

    print("db hashed password:", user.hashed_password)

    verified = verify_password(
        password,
        user.hashed_password,
    )

    print("password verified:", verified)

    if not verified:
        print("PASSWORD VERIFY FAILED")
        return None, "Invalid credentials"

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )

    print("LOGIN SUCCESS")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }, None


# -------------------------
# get user
# -------------------------

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await repository.get_user_by_id(db, user_id)


# -------------------------
# role check (pure logic)
# -------------------------

def is_admin(user: User) -> bool:
    return user.role == UserRole.ADMIN