from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import UserRole
from app.core.security import decode_token
from app.db.session import get_db
from app.domains.users.model import User
from app.domains.users.service import UserService


# ==================================================
# OAuth2
# ==================================================
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
)


# ==================================================
# current user
# ==================================================
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    try:
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        user_id = int(payload["sub"])

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await UserService.get_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return user


# ==================================================
# role-based guard (core)
# ==================================================
def require_roles(*allowed_roles: UserRole):

    async def checker(
        user: User = Depends(get_current_user),
    ) -> User:

        if user.role == UserRole.ADMIN:
            return user

        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )

        return user

    return checker


get_admin_user = require_roles(UserRole.ADMIN)


# ==================================================
# convenience shortcuts
# ==================================================
CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]

AdminUser = Annotated[
    User,
    Depends(require_roles(UserRole.ADMIN)),
]