from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import PhoneBook


async def create_entry(db: AsyncSession, data: dict):
    try:
        entry = PhoneBook(**data)
        entry.phone_number = "+7" + entry.phone_number[1:]
        print(entry.phone_number)
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"The phone number {entry.phone_number} is already recorded.")
