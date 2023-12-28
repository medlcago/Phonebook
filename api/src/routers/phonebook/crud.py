from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import PhoneBook


async def create_entry(db: AsyncSession, data: dict) -> PhoneBook:
    try:
        entry = PhoneBook(**data)
        entry.phone_number = "+7" + entry.phone_number[1:]
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"The phone number {entry.phone_number} is already recorded.")


async def get_entry_by_id(db: AsyncSession, entry_id: int, user_id: str) -> PhoneBook:
    entry = await db.scalar(select(PhoneBook).filter_by(user_id=user_id).filter_by(id=entry_id))
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Entry with id {entry_id} not found.")
    return entry


async def get_all_entries_by_user_id(db: AsyncSession, user_id: str) -> Sequence[PhoneBook]:
    entries = (await db.scalars(select(PhoneBook).filter_by(user_id=user_id))).all()
    if entries:
        return entries
    raise HTTPException(status_code=404, detail="No entries found.")
