from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.core.enums import UserRole
from app.domains.positions.schema import PositionResponse


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
    password: str | None = Field(default=None, min_length=4, max_length=128)


# -------------------------
# response
# -------------------------
class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    positions: list["PositionResponse"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# token
# -------------------------
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int  # 

