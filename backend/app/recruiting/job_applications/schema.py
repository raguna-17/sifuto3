from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class JobApplicationBase(BaseModel):
    job_posting_id: int

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_posting_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)