from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.users import schema, service
from app.core.security import get_current_user
from app.users.model import User, UserRole

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# -------------------------
# register
# -------------------------
@router.post(
    "/register",
    response_model=schema.UserResponse,
)
async def register(
    payload: schema.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user, error = await service.create_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return user


# -------------------------
# login
# -------------------------
@router.post(
    "/login",
    response_model=schema.Token,
)
async def login(
    payload: schema.UserLogin,
    db: AsyncSession = Depends(get_db),
):
    token, error = await service.login_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return token


# -------------------------
# current user
# -------------------------
@router.get(
    "/me",
    response_model=schema.UserResponse,
)
async def read_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# -------------------------
# get user by id (admin only)
# -------------------------
@router.get(
    "/{user_id}",
    response_model=schema.UserResponse,
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    user = await service.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user