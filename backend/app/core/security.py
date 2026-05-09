from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import get_settings
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# -------------------------
# password
# -------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# -------------------------
# JWT create
# -------------------------

def create_access_token(data: dict) -> str:
    settings = get_settings()

    payload = data.copy()
    payload["sub"] = str(payload["sub"])

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire, "type": "access"})

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(data: dict) -> str:
    settings = get_settings()

    payload = data.copy()
    payload["sub"] = str(payload["sub"])

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload.update({"exp": expire, "type": "refresh"})

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


# -------------------------
# decode
# -------------------------

def decode_token(token: str) -> dict:
    settings = get_settings()

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )


# -------------------------
# current user
# -------------------------

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    from app.users.service import get_user_by_id

    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(401, "Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")

        user = await get_user_by_id(db, int(user_id))

        if not user:
            raise HTTPException(401, "User not found")

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# -------------------------
# role check
# -------------------------

def require_role(role: str):
    async def checker(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(403, "Forbidden")
        return user

    return checker