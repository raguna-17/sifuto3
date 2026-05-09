from sqlalchemy.ext.asyncio import AsyncSession

from app.finance.categories import repository
from app.finance.categories.model import Category


# -------------------------
# create category
# -------------------------

async def create_category(
    db: AsyncSession,
    name: str,
    user_id: int,
) -> Category:
    # ここはビジネスルール置き場（今はシンプル）
    name = name.strip()

    return await repository.create_category(
        db=db,
        name=name,
        user_id=user_id,
    )


# -------------------------
# get one
# -------------------------

async def get_category(
    db: AsyncSession,
    category_id: int,
    user_id: int,
) -> Category | None:
    return await repository.get_category_by_id(
        db=db,
        category_id=category_id,
        user_id=user_id,
    )


# -------------------------
# list
# -------------------------

async def list_categories(
    db: AsyncSession,
    user_id: int,
) -> list[Category]:
    return await repository.get_categories_by_user(
        db=db,
        user_id=user_id,
    )


# -------------------------
# delete
# -------------------------

async def delete_category(
    db: AsyncSession,
    category_id: int,
    user_id: int,
) -> bool:
    category = await repository.get_category_by_id(
        db=db,
        category_id=category_id,
        user_id=user_id,
    )

    if not category:
        return False

    await repository.delete_category(db=db, category=category)
    return True