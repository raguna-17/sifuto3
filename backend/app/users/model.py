from datetime import datetime
from enum import Enum

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


# -------------------------
# role
# -------------------------

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


# -------------------------
# model
# -------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=UserRole.USER.value,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # -------------------------
    # relations
    # -------------------------

    categories = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    expenses = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    incomes = relationship(
        "Income",
        back_populates="user",
        cascade="all, delete-orphan",
    )