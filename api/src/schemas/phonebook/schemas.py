from uuid import UUID

from pydantic import BaseModel, field_validator


class PhoneBookEntryCreate(BaseModel):
    name: str
    phone_number: str

    @field_validator("phone_number")
    def phone_number_validator(cls, phone_number: str):
        number = "".join(filter(str.isdigit, phone_number))
        if len(number) != 11:
            raise ValueError("Неверная длина номера")
        if number[0] not in ("7", "8"):
            raise ValueError("Неверный формат номера")

        return number


class PhoneBookEntryRead(PhoneBookEntryCreate):
    id: int
    user_id: UUID
