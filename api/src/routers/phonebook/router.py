from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.phonebook import PhoneBookEntryCreate, PhoneBookEntryRead
from schemas.user import ResponseUser
from services.auth import get_current_user
from . import crud

router = APIRouter(prefix="/phonebook", tags=["Phonebook"])


@router.post("/", summary="Создание новой записи", response_model=PhoneBookEntryRead)
async def create_entry(entry: PhoneBookEntryCreate, user: ResponseUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    data = entry.model_dump()
    data.update(user_id=user.user_id)
    return await crud.create_entry(db=db, data=data)
