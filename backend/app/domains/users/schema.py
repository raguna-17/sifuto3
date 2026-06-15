from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)

from app.core.enums import (
    PositionType,
    UserRole,
)


# ==========================================
# User Create
# ==========================================

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    position: PositionType = PositionType.STAFF


# ==========================================
# User Update
# ==========================================

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    position: PositionType | None = None
    is_active: bool | None = None


# ==========================================
# User Response
# ==========================================

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    position: PositionType
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


# ==========================================
# Current User
# ==========================================

class CurrentUser(BaseModel):
    id: int
    email: EmailStr
    position: PositionType
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True
    )