from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.modules.product import service, schema

from app.core.enums import UserRole
from app.core.security import require_role

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

# -------------------------
# create product (admin)
# -------------------------
@router.post(
    "/",
    response_model=schema.ProductRead,
)
async def create_product(
    payload: schema.ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    product, error = await service.create_product(
        db=db,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
        image_url=payload.image_url,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return product


# -------------------------
# get all active products
# -------------------------
@router.get(
    "/",
    response_model=list[schema.ProductRead],
)
async def get_products(
    db: AsyncSession = Depends(get_db),
):
    return await service.get_all_active_products(db)


# -------------------------
# get product by id
# -------------------------
@router.get(
    "/{product_id}",
    response_model=schema.ProductRead,
)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    product = await service.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


# -------------------------
# update product (admin)
# -------------------------
@router.put(
    "/{product_id}",
    response_model=schema.ProductRead,
)
async def update_product(
    product_id: int,
    payload: schema.ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    product = await service.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    updated_product, error = await service.update_product(
        db=db,
        product=product,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
        image_url=payload.image_url,
        is_active=payload.is_active,
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return updated_product


# -------------------------
# delete product (admin)
# -------------------------
@router.delete(
    "/{product_id}",
)
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(require_role(UserRole.ADMIN)),
):
    product = await service.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    await service.delete_product(db, product)

    return {"message": "Product deleted"}