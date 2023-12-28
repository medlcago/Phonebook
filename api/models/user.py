from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.models import Base

if TYPE_CHECKING:
    from .phonebook import PhoneBook


class User(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str] = mapped_column(String(length=255))
    password: Mapped[str] = mapped_column(String(length=255))

    phonebook_entries: Mapped[list["PhoneBook"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
