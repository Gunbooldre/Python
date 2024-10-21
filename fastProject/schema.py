from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    body: str
    published: bool = False
    rating: Optional[int] = None
