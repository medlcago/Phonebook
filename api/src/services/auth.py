import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User
from config import config
from database import get_db
from schemas.auth import Token
from schemas.user import CreateUser, ResponseUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/auth/sign-in")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> ResponseUser:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=plain_password.encode(),
            hashed_password=hashed_password,
        )

    @classmethod
    def hash_password(cls, password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @classmethod
    def validate_token(cls, token: str) -> ResponseUser:
        try:
            payload = jwt.decode(
                token,
                config.auth_jwt.jwt_secret,
                algorithms=[config.auth_jwt.jwt_algorithm]
            )
        except PyJWTError:
            raise HTTPException(
                status_code=401,
                detail="Failed to verify login information.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )
        user = payload.get("user")
        try:
            user = ResponseUser.model_validate(user)
        except ValidationError:
            raise HTTPException(
                status_code=401,
                detail="Failed to verify login information.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )
        return user

    @classmethod
    def create_token(cls, user: User) -> Token:
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=config.auth_jwt.access_token_expire_minutes),
            "sub": str(user.user_id),
            "user": {
                "id": user.id,
                "user_id": str(user.user_id),
                "username": user.username,
                "fullname": user.fullname
            }
        }
        token = jwt.encode(
            payload,
            config.auth_jwt.jwt_secret,
            algorithm=config.auth_jwt.jwt_algorithm
        )
        return Token(access_token=token)

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def register_new_user(self, user_data: CreateUser) -> Token:
        user_id = uuid.uuid4()

        user = User(
            user_id=user_id,
            fullname=user_data.fullname,
            username=user_data.username,
            password=self.hash_password(user_data.password).decode()
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return self.create_token(user)

    async def authenticate_user(self, username: str, password: str) -> Token:
        user = await self.session.scalar(select(User).filter_by(username=username))
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )
        if not self.verify_password(password, user.password.encode()):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )

        return self.create_token(user)