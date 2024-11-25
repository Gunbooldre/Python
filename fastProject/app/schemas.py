from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class UsersOut(BaseModel):
    id: int
    email: str
    created_at: datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UsersOut


class PostOut(BaseModel):
    Post: Post
    votes: int


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
