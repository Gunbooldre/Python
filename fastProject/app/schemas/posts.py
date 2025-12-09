from datetime import datetime

from pydantic import BaseModel

from app.schemas.users import UsersOut


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

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int
