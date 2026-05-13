from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.product.model import Product


# -------------------------
# Read
# -------------------------

async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def get_all_active_products(db: AsyncSession):
    result = await db.execute(
        select(Product).where(Product.is_active == True)
    )
    return result.scalars().all()


# -------------------------
# Create
# -------------------------

async def create_product(db: AsyncSession, product: Product):
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


# -------------------------
# Update
# -------------------------

async def update_product(db: AsyncSession, product: Product):
    await db.commit()
    await db.refresh(product)
    return product


# -------------------------
# Delete（論理削除推奨）
# -------------------------

async def delete_product(db: AsyncSession, product: Product):
    product.is_active = False
    await db.commit()
    return product