from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from argon2.exceptions import VerifyMismatchError

from app.models import User
from app.schemas import UserCreate, UserLogin
from app.auth import create_access_token, ph


async def register_user(db: AsyncSession, user_in: UserCreate) -> User:
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = ph.hash(user_in.password)
    new_user = User(email=user_in.email, hashed_password=hashed_pw)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def login_user(db: AsyncSession, user_in: UserLogin) -> dict:
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        ph.verify(user.hashed_password, user_in.password)
    except VerifyMismatchError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)

    return {"access_token": token, "token_type": "bearer"}