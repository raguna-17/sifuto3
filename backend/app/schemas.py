from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from app.enums import ApplicationStatus

# -----------------
# User
# -----------------
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=22)

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# -----------------
# Forward referenceのための仮宣言
# -----------------
class CompanyRead(BaseModel):
    pass

# -----------------
# Application
# -----------------
class ApplicationBase(BaseModel):
    position: str = Field(max_length=100)
    applied_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None

class ApplicationCreate(ApplicationBase):
    company_id: int  # 会社IDをフロントから送信
    status: ApplicationStatus = ApplicationStatus.APPLIED

class ApplicationRead(ApplicationBase):
    id: int
    status: ApplicationStatus
    created_at: datetime
    company: CompanyRead  # 応募済み企業情報を返す
    model_config = ConfigDict(from_attributes=True)

# -----------------
# Company
# -----------------
class CompanyBase(BaseModel):
    name: str = Field(max_length=100)
    industry: Optional[str] = Field(default=None, max_length=100)

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: int
    created_at: datetime
    applications: List[ApplicationRead] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

# Forward reference更新
ApplicationRead.model_rebuild()