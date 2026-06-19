from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)

from app.core.enums import UserRole


# ==========================================
# User Create
# ==========================================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# ==========================================
# User Update
# ==========================================

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None


# ==========================================
# User Response
# ==========================================

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================
# Login
# ==========================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ==========================================
# Token
# ==========================================

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


