from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PaginationParams(BaseModel):
    limit: int = Field(5, ge=0, le=100, description="Кол-во элементов на странице")
    skip: int = Field(5, ge=0, description="Сокращения для пагинации")
