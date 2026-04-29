from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship

from app.db import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    # 🔗 外部キー
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)

    # 📦 応募情報
    status = Column(String, default="applied", nullable=False)

    # ⏱ システム情報
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # 🔗 relations
    user = relationship("User", back_populates="applications")
    job_posting = relationship("JobPosting", back_populates="applications")

    