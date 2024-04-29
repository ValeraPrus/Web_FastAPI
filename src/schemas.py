from pydantic import BaseModel, Field, EmailStr
from datetime import date


class ContactResponse(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr = Field(max_length=50)
    phone: str = Field(max_length=20)
    birthday: date = Field()
    additional: str | None = Field(default=None)

    class Config:
        orm_mode = True
