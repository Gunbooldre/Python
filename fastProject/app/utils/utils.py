import asyncio
import time
from functools import wraps, lru_cache
from typing import Callable, Coroutine

from django.template.defaultfilters import yesno
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


def deco(func: Callable):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(f'Tine for exec is {end - start}')
        return res

    return wrapper


@deco
def my_func():
    time.sleep(3)
    return 1


def limit(temp: int):
    def deco2(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal temp
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            temp -= 1
            if temp == 0:
                print("ERROR MF")
                return

            print(f'Tine for exec is {end - start}')
            return res

        return wrapper
    return deco2


@limit(temp=2)
def my_func2(time_sleep: int):
    time.sleep(time_sleep)
    return 1


def deco_corutine(coroutine: Coroutine | Callable):
    async def wrapper(*args, **kwargs):
        return await coroutine(*args, **kwargs)
    return wrapper


@deco_corutine
async def my_async_func():
    print("Hello my friend")
    await asyncio.sleep(3)

# await my_async_func()


@lru_cache
def my_func_lru(x: int):
    time.sleep(5)
    return x * 2


from contextlib import contextmanager


def ctx_manager():
    print("hello")
    yield
    print("end")


with ctx_manager as m:
    print("123")


def log_func(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Start {func.__name__} args: {args} kwargs: {kwargs}")
        res = func(*args, **kwargs)
        print(f"End {func.__name__} args: {args} kwargs: {kwargs}")
        return res
    return wrapper
