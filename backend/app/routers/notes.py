from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db
from app.models import User
from app.schemas import NoteRead, NoteCreate
from app.auth import get_current_user
from app.services import note_service

router = APIRouter(prefix="/api/v1/notes", tags=["notes"])


@router.get("/", response_model=List[NoteRead])
async def get_my_notes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await note_service.get_user_notes(db, current_user.id)


@router.get("/{note_id}", response_model=NoteRead)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    note = await note_service.get_user_note(db, current_user.id, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    app = await note_service.verify_user_application(
        db, current_user.id, note.application_id
    )

    if not app:
        raise HTTPException(
            status_code=404,
            detail="Application not found or not owned by user"
        )

    return await note_service.create_note(
        db,
        note.application_id,
        note.content
    )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    note = await note_service.delete_note(
        db, current_user.id, note_id
    )

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return None