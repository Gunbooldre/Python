"""Декораторы"""
# def repeat(n):
#     def decoratore(func):
#         def wrapper(*args, **kwargs):
#             print("Begging")
#             result = []
#             for i in range(n):
#                 r = func(*args, **kwargs)
#                 result.append(r)
#             print("End")
#             return result
#         return wrapper
#     return decoratore
#
#
# @repeat(3)
# def hello_world(name):
#     print( f'Hello my friend {name}')
#
# hello_world("Dias")


# def decoratore(func):
#     def wrapper(*args, **kwargs):
#         print("Begging")
#         result = func(*args, **kwargs)
#         print("End")
#         return result
#     return wrapper
#
#
# @decoratore
# def hello_world(name):
#     print(f'Hello my friend {name}')
#
# hello_world("Dias")




# def decorator(func):
#     def wrapper(*args,**kwargs):
#         print("in Wparrer")
#         result = func(*args, **kwargs)
#         return result
#     return wrapper
#
# @decorator
# def helloWorld():
#     print("hello WOrld")
#
#
#
# helloWorld()

from functools import wraps
import logging

logger = logging.getLogger(__name__)

def cashe(func):
    cashe_ = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal cashe_
        key = ''
        for arg in args:
            key += f'{arg}_'
        for k, v in kwargs.items():
            key += f'{k}_{v}'

        if key in cashe_:
            res = cashe_[key]
            print((f"Get result of {func.__name__} ({args}) and  ({kwargs}) and result is {res}"))
            print (res)
        res = func(*args, **kwargs)
        cashe_[key] = res
        print (res)
    return wrapper


@cashe
def foo(s):
    return (s)

foo("Hello my little friend")
foo("Hello my little friend")
foo("Hello my little friend")
foo("Hello my little friend")