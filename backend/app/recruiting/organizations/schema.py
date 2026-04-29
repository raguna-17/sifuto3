from pydantic import BaseModel,ConfigDict
from typing import Optional
from datetime import datetime


# ===== 共通ベース =====
class OrganizationBase(BaseModel):
    name: str
    industry: Optional[str] = None
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None


# ===== 作成 =====
class OrganizationCreate(OrganizationBase):
    pass


# ===== 更新 =====
class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None


# ===== レスポンス =====
class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)