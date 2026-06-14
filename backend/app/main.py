from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings

from app.domains.users.router import router as users_router
from app.domains.positions.router import router as positions_router
from app.domains.shift_slots.router import router as shift_slots_router
from app.domains.shift_slot_requirements.router import (
    router as shift_slot_requirements_router,
)
from app.domains.shift_preferences.router import (
    router as shift_preferences_router,
)
from app.domains.shift_assignments.router import (
    router as shift_assignments_router,
)


settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)

app.include_router(positions_router)

app.include_router(shift_slots_router)

app.include_router(shift_slot_requirements_router)

app.include_router(shift_preferences_router)

app.include_router(shift_assignments_router)


