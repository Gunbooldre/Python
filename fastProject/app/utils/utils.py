import asyncio
import time

from passlib.context import CryptContext
from fastapi import Query
from app.schemas.schemas import PaginationParams

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(plaint_password, hashed_password):
    return pwd_context.verify(plaint_password, hashed_password)


def pagination_dep(
    limit: int = Query(5, ge=0, le=100, description="Кол-во элементов на странице"),
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
) -> PaginationParams:
    return PaginationParams(limit=limit, skip=skip)


def sync_task():
    time.sleep(3)
    print("sync_task is done")


async def async_task():
    await asyncio.sleep(3)
    print("sync_task_async is done")


