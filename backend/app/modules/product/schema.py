from pydantic import BaseModel,ConfigDict
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: int
    stock: int
    image_url: str | None = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    stock: int | None = None
    image_url: str | None = None
    is_active: bool | None = None


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config=ConfigDict(from_attributes=True)