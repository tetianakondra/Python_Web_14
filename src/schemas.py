from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    first_name: str = Field('First_name', min_length=3, max_length=16)
    last_name: str = Field('Last_name', min_length=3, max_length=16)
    email: EmailStr
    phone: str = Field('0631234567',  max_length=16)
    birthday: date
    description: Optional[str]


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str = 'First_name'
    last_name: str = 'Last_name'
    email: EmailStr
    phone: str = '0631234567'
    birthday: date = date(year=2012, month=12, day=12)
    description: Optional[str]

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
