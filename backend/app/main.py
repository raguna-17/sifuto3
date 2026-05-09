from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.db.imports
from app.core.config import get_settings

from app.users.router import router as user_router

from app.finance.categories.router import (
    router as category_router,
)

from app.finance.expenses.router import (
    router as expense_router,
)


from app.finance.incomes.router import (
    router as income_router,
)



settings = get_settings()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONT],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)

app.include_router(category_router)

app.include_router(expense_router)

app.include_router(income_router)