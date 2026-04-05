from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.enums import ApplicationStatus
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    applications = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    industry = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())

    applications = relationship(
        "Application",
        back_populates="company",
        cascade="all, delete-orphan",
    )


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    position = Column(String(100), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, nullable=False)
    applied_date = Column(DateTime, server_default=func.now(), nullable=False)
    interview_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    company = relationship("Company", back_populates="applications")
    user = relationship("User", back_populates="applications")

    __table_args__ = (
        UniqueConstraint("user_id", "company_id", "position", name="uq_user_company_position"),
    )