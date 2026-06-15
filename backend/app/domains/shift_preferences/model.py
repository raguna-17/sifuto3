from datetime import datetime, date

from sqlalchemy import (
    ForeignKey,
    Date,
    DateTime,
    Enum,
    Text,
    func,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base
from app.core.enums import PreferencePriority


class ShiftPreference(Base):
    __tablename__ = "shift_preferences"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # =========================
    # owner
    # =========================
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    shift_slot_id: Mapped[int] = mapped_column(
        ForeignKey("shift_slots.id"),
        nullable=False,
        index=True,
    )

    # =========================
    # target day
    # =========================
    target_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # =========================
    # optional time range
    # （日単位 or 時間帯両対応）
    # =========================
    start_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    end_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =========================
    # preference strength
    # =========================
    priority: Mapped[PreferencePriority] = mapped_column(
        Enum(PreferencePriority),
        nullable=False,
        default=PreferencePriority.NEUTRAL,
    )

    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # =========================
    # timestamps
    # =========================
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

    # =========================
    # relations
    # =========================
    user = relationship(
        "User",
        back_populates="preferences",
    )


    slot = relationship(
        "ShiftSlot",
        back_populates="preferences",
    )