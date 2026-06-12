from sqlalchemy import ForeignKey, Date, DateTime, Enum, Text, func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base
from app.core.enums import PreferencePriority


class ShiftPreference(Base):
    __tablename__ = "shift_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    target_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # atetimelot
    start_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    end_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # 
    priority: Mapped[PreferencePriority] = mapped_column(
        Enum(PreferencePriority),
        default=PreferencePriority.PREFERRED,
        nullable=False,
    )

    # 
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationship
    user = relationship(
        "User",
        back_populates="preferences",
    )

