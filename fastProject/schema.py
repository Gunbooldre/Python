from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    title: str
    body: str
    published: bool = False
    rating: Optional[int] = None
