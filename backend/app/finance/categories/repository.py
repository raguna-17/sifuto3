from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.finance.categories.model import Category


# -------------------------
# create
# -------------------------

async def create_category(
    db: AsyncSession,
    name: str,
    user_id: int,
) -> Category:
    category = Category(
        name=name,
        user_id=user_id,
    )

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


# -------------------------
# read (single)
# -------------------------

async def get_category_by_id(
    db: AsyncSession,
    category_id: int,
    user_id: int,
) -> Category | None:
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,  # ←重要
        )
    )
    return result.scalar_one_or_none()


# -------------------------
# read (list)
# -------------------------

async def get_categories_by_user(
    db: AsyncSession,
    user_id: int,
) -> list[Category]:
    result = await db.execute(
        select(Category).where(
            Category.user_id == user_id
        )
    )
    return result.scalars().all()


# -------------------------
# delete
# -------------------------

async def delete_category(
    db: AsyncSession,
    category: Category,
) -> None:
    await db.delete(category)
    await db.commit()