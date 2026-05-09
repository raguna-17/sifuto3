from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.users import schema, service
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


# -------------------------
# create user (register)
# -------------------------

@router.post("/register", response_model=schema.UserResponse)
async def register(
    payload: schema.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await service.create_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )


# -------------------------
# login
# -------------------------

@router.post("/login", response_model=schema.Token)
async def login(
    payload: schema.UserLogin,
    db: AsyncSession = Depends(get_db),
):
    return await service.login_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )


# -------------------------
# current user
# -------------------------

@router.get("/me", response_model=schema.UserResponse)
async def read_me(
    current_user=Depends(get_current_user),
):
    return current_user


# -------------------------
# get user by id (admin or debug用途)
# -------------------------

@router.get("/{user_id}", response_model=schema.UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await service.get_user_by_id(db, user_id)