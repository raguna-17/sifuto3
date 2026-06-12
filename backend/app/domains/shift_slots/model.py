from datetime import date,datetime

from sqlalchemy import (
    Date,
    DateTime,
    Integer,
    func,
    ForeignKey,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base


class ShiftSlot(Base):
    """
    繧ｷ繝輔ヨ譫・磯怙隕∝・・・
    萓具ｼ・
      2026-06-10 10:00-14:00 / 繝帙・繝ｫ2莠ｺ
    """

    __tablename__ = "shift_slots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # 蟇ｾ雎｡譌･・磯°逕ｨ蜊倅ｽ搾ｼ・
    target_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # 豁｣隕丞喧・壽律譎ゅ↓縺吶ｋ・磯㍾隕・ｼ・
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # 逶｣譟ｻ
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

    # ==================================================
    # relationships
    # ==================================================

    assignments = relationship(
        "ShiftAssignment",
        back_populates="slot",
        cascade="all, delete-orphan",
    )

    requirements = relationship(
        "ShiftSlotRequirement",
        back_populates="slot",
        cascade="all, delete-orphan",
    )
