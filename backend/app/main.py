from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.db.imports

from app.core.config import get_settings

from app.users.router import router as user_router

from app.modules.product.router import (
    router as product_router,
)

from app.modules.cart.router import (
    router as cart_router,
)

from app.modules.order.router import (
    router as order_router,
)

settings = get_settings()

app = FastAPI(
    title="EC API",
)

# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONT],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# routers
# -------------------------

app.include_router(user_router)

app.include_router(product_router)

app.include_router(cart_router)

app.include_router(order_router)