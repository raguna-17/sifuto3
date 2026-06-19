from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings


settings = get_settings()


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


# ==================================================
# password
# ==================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==================================================
# JWT create
# ==================================================

def _create_token(
    data: dict[str, Any],
    expires_delta: timedelta,
    token_type: str,
) -> str:
    payload = data.copy()

    payload["sub"] = str(payload["sub"])

    payload.update(
        {
            "exp": datetime.now(timezone.utc) + expires_delta,
            "type": token_type,
        }
    )

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(
    data: dict[str, Any],
) -> str:
    return _create_token(
        data=data,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        ),
        token_type="access",
    )


def create_refresh_token(
    data: dict[str, Any],
) -> str:
    return _create_token(
        data=data,
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        ),
        token_type="refresh",
    )


# ==================================================
# JWT decode
# ==================================================

def decode_token(
    token: str,
) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

    except JWTError as exc:
        raise ValueError("Invalid token") from exc

