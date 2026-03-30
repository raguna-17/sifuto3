import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt
from argon2 import PasswordHasher

from .db import get_db
from .models import User


# ========================
# 設定
# ========================

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is not set")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ph = PasswordHasher()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


# ========================
# JWT関連
# ========================

def create_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None
):
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": str(user_id),   # ← 文字列に統一
        "exp": expire,
        "iss": "your-app",     # 任意だけど入れとくと良い
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# ========================
# User取得（内部用）
# ========================

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalars().first()


# ========================
# 認証依存関数
# ========================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        # 型安全化
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user


# ========================
# パスワード関連（ついでに整備）
# ========================

def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception:
        return False