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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User
from config import config
from database import get_db
from schemas.auth import Token
from schemas.user import CreateUser, ResponseUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth/sign-in")


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
        exp_401 = HTTPException(
            status_code=401,
            detail="Failed to verify login information.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
        try:
            payload = jwt.decode(
                token,
                config.auth_jwt.jwt_secret,
                algorithms=[config.auth_jwt.jwt_algorithm]
            )
        except PyJWTError:
            raise exp_401
        user = payload.get("user")
        try:
            user = ResponseUser.model_validate(user)
        except ValidationError:
            raise exp_401
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
        try:
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
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists.")

    async def authenticate_user(self, username: str, password: str) -> Token:
        user = await self.session.scalar(select(User).filter_by(username=username))
        exp_401 = HTTPException(
            status_code=401,
            detail="Incorrect username or password.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

        if user is None:
            raise exp_401
        if not self.verify_password(password, user.password.encode()):
            raise exp_401
        return self.create_token(user)
