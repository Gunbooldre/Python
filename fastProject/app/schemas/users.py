from datetime import datetime

from pydantic import BaseModel, EmailStr, conint, Field


class UsersOut(BaseModel):
    id: int
    email: str
    created_at: datetime


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
