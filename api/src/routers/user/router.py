from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.user import ResponseUser, CreateUser, UpdateUser
from services.auth import AuthService, get_current_user
from . import crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=ResponseUser, status_code=201, summary="Регистрация пользователя")
async def create_user(data: CreateUser, service: AuthService = Depends(), db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db=db, service=service, data=data.model_dump())


@router.patch("/", response_model=ResponseUser, response_model_exclude_unset=True, summary="Обновить данные пользователя")
async def update_user(data: UpdateUser, user: ResponseUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.update_user(db=db, user=user, data=data.model_dump(exclude_unset=True))
