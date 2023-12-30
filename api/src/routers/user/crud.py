import uuid

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User
from schemas.user import ResponseUser
from services.auth import AuthService


async def create_user(db: AsyncSession, service: AuthService, data: dict) -> User:
    try:
        user_id = uuid.uuid4()
        user = User(user_id=user_id, **data)
        user.password = service.hash_password(user.password).decode()
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists.")


async def update_user(db: AsyncSession, user: ResponseUser, data: dict) -> User:
    if not data:
        raise HTTPException(status_code=400, detail="Invalid data to change.")

    try:
        user_id = user.user_id
        stmt = update(User).filter_by(user_id=user_id).values(**data)
        result = await db.execute(stmt)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Data integrity error")

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    await db.commit()
    data = await db.scalar(select(User).filter_by(user_id=user_id))
    return data
