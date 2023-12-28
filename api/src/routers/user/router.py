from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.user import ResponseUser, CreateUser
from services.auth import AuthService
from . import crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=ResponseUser, status_code=201, summary="Регистрация пользователя")
async def create_user(data: CreateUser, service: AuthService = Depends(), db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db=db, service=service, data=data.model_dump())
