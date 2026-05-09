from fastapi import HTTPException, status

from app.users import repository
from app.users.model import User, UserRole
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token


# -------------------------
# user create
# -------------------------

async def create_user(db, email: str, password: str):
    existing = await repository.get_user_by_email(db, email)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=UserRole.USER.value,
        is_active=True,
    )

    return await repository.create_user(db, user)


# -------------------------
# login
# -------------------------

async def login_user(db, email: str, password: str):
    user = await repository.get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        data={"sub": user.id}
    )

    refresh_token = create_refresh_token(
        data={"sub": user.id}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# -------------------------
# get user
# -------------------------

async def get_user_by_id(db, user_id: int):
    return await repository.get_user_by_id(db, user_id)


# -------------------------
# admin role check helper
# -------------------------

def is_admin(user: User) -> bool:
    return user.role == UserRole.ADMIN.value