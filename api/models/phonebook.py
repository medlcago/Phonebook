from sqlalchemy import BIGINT, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PhoneBook(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(length=32))
    phone_number: Mapped[int] = mapped_column(String(length=12))
