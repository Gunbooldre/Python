"copy/ deepcopy"
# import copy
# a = [1, [2]]
# b = copy.copy(a)
# b.append(3)
# b[1].append(4)
# b = copy.deepcopy(a)
# print(a)

"Map"
# a = [i for i in range(10)]
# b = map(lambda x: x**2, a)
# print(list(b))
#
# def double(x):
#     return x * x
#
# b = map(double, a)
# print(list(b))

"Filter"
# a = [i for i in range(5)]
# b = filter(lambda x: x % 2 == 0, a)
# print(list(b))

"ZIP"
# a = [1,2,3 ]
# b = [4,5,6, 7]
# c = [8, 9,]
#
# for i in zip(a,b,c):
#     print(i)


"""New or INIT"""
# class A:
#
#     def __new__(cls, *args, **kwargs):
#         # object = super().__new__(cls, *args, **kwargs)
#         print("New")
#         # return object
#
#     def __init__(self, name):
#         print("init")
#         self.name = name
#
#
# a = A("Dias")
#
# print(a)
"""
Полиморфизм
"""
# class Animal:
#     def sound(self):
#         raise ValueError("Error")
#
#
# class Dog(Animal):
#     def sound(self):
#         return "Wouv"
#
#
# class Cat(Animal):
#     def sound(self):
#         return "Meow"
#
#
# class Cow(Animal):
#     def __int__(self):
#         pass
#
#
# def make_sound(animal):
#     print(animal.sound())
#
#
# d = Dog()
# c = Cat()
# cow = Cow()
#
# make_sound(d)
# make_sound(c)
# make_sound(Cow)

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