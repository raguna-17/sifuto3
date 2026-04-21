from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class OrganizationBase(BaseModel):
    name: str
    industry: Optional[str]=None

class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)