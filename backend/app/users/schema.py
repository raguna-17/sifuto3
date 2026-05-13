from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import UserRole


# -------------------------
# base
# -------------------------

class UserBase(BaseModel):
    email: EmailStr


# -------------------------
# create
# -------------------------

class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=128)


# -------------------------
# login
# -------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -------------------------
# update
# -------------------------

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


# -------------------------
# response
# -------------------------

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"