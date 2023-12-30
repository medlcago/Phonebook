from uuid import UUID

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    username: str
    fullname: str


class CreateUser(BaseUser):
    password: str


class ResponseUser(BaseUser):
    id: int
    user_id: UUID


class UpdateUser(BaseUser):
    username: str | None = Field(default=None)
    fullname: str | None = Field(default=None)
