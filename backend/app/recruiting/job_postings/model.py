from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship

from app.db import Base


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    
    # 🔗 外部キー（超重要）
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False,index=True)

    title = Column(String, nullable=False)          # 職種
    description = Column(String, nullable=True)     # 業務内容
    location = Column(String, nullable=True)        # 勤務地
    salary = Column(String, nullable=True)          # 給与
    employment_type = Column(String, nullable=True) # 正社員 / インターンなど
    
    # 🔐 公開制御
    is_active = Column(Boolean, default=True)       # 公開/非公開
    published_at = Column(DateTime, server_default=func.now())
    closed_at = Column(DateTime, nullable=True)

    # ⏱ システム情報
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    # 🔗 relations
    organization = relationship("Organization", back_populates="job_postings")
    user = relationship("User", back_populates="job_postings")  # ← ★追加
    applications = relationship(
        "JobApplication",
        back_populates="job_posting"
    )