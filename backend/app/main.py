from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import get_settings
from app.core.logging import setup_logging

from app.domains.users.router import router as users_router
from app.domains.shift_slots.router import router as shift_slots_router
from app.domains.shift_preferences.router import router as shift_preferences_router
from app.domains.shift_assignments.router import router as shift_assignments_router
from app.domains.scheduler.router import router as scheduler_router
from app.domains.exports.router import router as exports_router  # 👈 追加

from app.domains.shift_preferences.service import (
    ShiftPreferenceConflictError,
    ShiftPreferenceNotFoundError,
)

from app.domains.shift_assignments.service import (
    DuplicateAssignmentError,
    AssignmentCapacityError,
    ShiftSlotNotFoundError,
)

settings = get_settings()
setup_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:

    app = FastAPI(
        title="Shift Management API",
        version="v1",
    )

    # -------------------------
    # middleware
    # -------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------
    # routers
    # -------------------------
    app.include_router(users_router)
    app.include_router(shift_slots_router)
    app.include_router(shift_preferences_router)
    app.include_router(shift_assignments_router)
    app.include_router(scheduler_router)
    app.include_router(exports_router)  # 👈 追加

    # -------------------------
    # exception handlers
    # -------------------------
    @app.exception_handler(ShiftPreferenceConflictError)
    async def shift_preference_conflict_handler(request: Request, exc: ShiftPreferenceConflictError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ShiftPreferenceNotFoundError)
    async def shift_preference_not_found_handler(request: Request, exc: ShiftPreferenceNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": "shift preference not found"},
        )

    @app.exception_handler(DuplicateAssignmentError)
    async def duplicate_handler(request: Request, exc: DuplicateAssignmentError):
        return JSONResponse(
            status_code=409,
            content={"detail": "duplicate assignment"},
        )

    @app.exception_handler(AssignmentCapacityError)
    async def capacity_handler(request: Request, exc: AssignmentCapacityError):
        return JSONResponse(
            status_code=409,
            content={"detail": "slot is full"},
        )

    @app.exception_handler(ShiftSlotNotFoundError)
    async def slot_not_found_handler(request: Request, exc: ShiftSlotNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": "shift slot not found"},
        )

    # -------------------------
    # lifecycle
    # -------------------------
    @app.on_event("startup")
    async def startup_event():
        logger.info("API started", extra={"version": "v1"})

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("API stopped")

    return app


app = create_app()