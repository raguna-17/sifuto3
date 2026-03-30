from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas import UserCreate, UserRead, UserLogin
from app.auth import get_current_user
from app.models import User
from app.services import user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.register_user(db, user_in)


@router.post("/login")
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    return await user_service.login_user(db, user_in)


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user