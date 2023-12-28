import uuid

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User
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
        raise HTTPException(status_code=409, detail=f"User already exists.")
