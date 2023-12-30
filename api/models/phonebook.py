from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, String, ForeignKey, UUID, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class PhoneBook(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    name: Mapped[str] = mapped_column(String(length=32))
    phone_number: Mapped[str] = mapped_column(String(length=12))

    user: Mapped["User"] = relationship(back_populates="phonebook_entries")

    __table_args__ = (
        UniqueConstraint("user_id", "phone_number", name='ux_user_phone_number'),
    )