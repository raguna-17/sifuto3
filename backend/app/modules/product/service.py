from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product import repository
from app.modules.product.model import Product


# -------------------------
# create product
# -------------------------

async def create_product(
    db: AsyncSession,
    name: str,
    description: str | None,
    price: int,
    stock: int,
    image_url: str | None,
) -> tuple[Product | None, str | None]:

    if price < 0:
        return None, "Price cannot be negative"

    if stock < 0:
        return None, "Stock cannot be negative"

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url,
        is_active=True,
    )

    created_product = await repository.create_product(db, product)

    return created_product, None


# -------------------------
# get product by id
# -------------------------

async def get_product_by_id(
    db: AsyncSession,
    product_id: int,
) -> Product | None:

    return await repository.get_product_by_id(db, product_id)


# -------------------------
# get all active products
# -------------------------

async def get_all_active_products(
    db: AsyncSession,
):

    return await repository.get_all_active_products(db)


# -------------------------
# update product
# -------------------------

async def update_product(
    db: AsyncSession,
    product: Product,
    name: str,
    description: str | None,
    price: int,
    stock: int,
    image_url: str | None,
    is_active: bool,
) -> tuple[Product | None, str | None]:

    if price < 0:
        return None, "Price cannot be negative"

    if stock < 0:
        return None, "Stock cannot be negative"

    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    product.image_url = image_url
    product.is_active = is_active

    updated_product = await repository.update_product(db, product)

    return updated_product, None


# -------------------------
# soft delete product
# -------------------------

async def delete_product(
    db: AsyncSession,
    product: Product,
):

    return await repository.delete_product(db, product)


# -------------------------
# decrease stock
# -------------------------

async def decrease_stock(
    db: AsyncSession,
    product: Product,
    quantity: int,
) -> tuple[Product | None, str | None]:

    if quantity <= 0:
        return None, "Quantity must be greater than 0"

    if product.stock < quantity:
        return None, "Not enough stock"

    product.stock -= quantity

    updated_product = await repository.update_product(db, product)

    return updated_product, None