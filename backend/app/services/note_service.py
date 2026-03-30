from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Note, Application


async def get_user_notes(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Note)
        .join(Application)
        .where(Application.user_id == user_id)
    )
    return result.scalars().all()


async def get_user_note(db: AsyncSession, user_id: int, note_id: int):
    result = await db.execute(
        select(Note)
        .join(Application)
        .where(
            Note.id == note_id,
            Application.user_id == user_id
        )
    )
    return result.scalars().first()


async def verify_user_application(db: AsyncSession, user_id: int, application_id: int):
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == user_id
        )
    )
    return result.scalars().first()


async def create_note(db: AsyncSession, application_id: int, content: str):
    new_note = Note(content=content, application_id=application_id)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note


async def delete_note(db: AsyncSession, user_id: int, note_id: int):
    note = await get_user_note(db, user_id, note_id)
    if not note:
        return None

    await db.delete(note)
    await db.commit()
    return note