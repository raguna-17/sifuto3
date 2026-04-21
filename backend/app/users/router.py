from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.users import service, schema
from app.users.model import User
from app.dependencies import get_current_active_user
from app.core.security import create_access_token

router = APIRouter(prefix="/users", tags=["users"])


# ユーザー登録
@router.post("/register", response_model=schema.UserResponse)
async def register_user(
    user_in: schema.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await service.create_user(db, user_in)
    return user


# ログイン
@router.post("/login")
async def login_user(
    user_in: schema.UserLogin,
    db: AsyncSession = Depends(get_db),
):
    user = await service.authenticate_user(
        db,
        email=user_in.email,
        password=user_in.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# 自分の情報取得（認証必須）
@router.get("/me", response_model=schema.UserResponse)
async def get_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user