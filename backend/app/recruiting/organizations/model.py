from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)

    # 📦 求人情報
    name = Column(String, nullable=False)              # 会社名
    industry = Column(String, nullable=True)           # 業界
    headquarters = Column(String, nullable=True)       # 本社所在地
    founded_year = Column(Integer, nullable=True)      # 設立年
    
    

    # ⏱ システム情報
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at=Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

    
    job_postings = relationship("JobPosting",back_populates="organization",cascade="all, delete-orphan")