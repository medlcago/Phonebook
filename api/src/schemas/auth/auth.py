from pydantic import BaseModel, Field

from config import config


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    access_token_expire_minutes: int = Field(default=config.auth_jwt.access_token_expire_minutes)
