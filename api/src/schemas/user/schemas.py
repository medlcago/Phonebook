from uuid import UUID

from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    fullname: str


class CreateUser(BaseUser):
    password: str


class ResponseUser(BaseUser):
    id: int
    user_id: UUID
