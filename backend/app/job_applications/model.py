from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    organization_name = Column(String, nullable=False)
    
    job_title = Column(String, nullable=False)
    created_at=Column(DateTime, server_default=func.now(),nullable=False)
    # リレーション
    user = relationship("User", back_populates="job_applications")
    organization = relationship("Organization", back_populates="job_applications")