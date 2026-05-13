from sqlalchemy import String, Text, Float, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    price: Mapped[int] = mapped_column(Integer, nullable=False, default=1000)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- relationships ---
    carts: Mapped[list["Cart"]] = relationship(
        back_populates="product",
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="product",
    )

    