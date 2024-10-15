"Iteratore"
#
# class Counter:
#     current: int
#
#     def __init__(self):
#         self.current = 0
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         current = self.current
#         self.current += 1
#         return current
#
#
# c = Counter()
#
# i = iter(c)
# print(next(i))
# print(next(i))
# print(next(i))

"Generator"

#
# class Fibocci:
#     def __init__(self):
#         self.prev = 0
#         self.current = 1
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         value = self.prev
#         self.prev, self.current = self.current, self.prev + self.current
#         return value
#
#
# f = Fibocci()
# for i in range(1, 101):
#     print(f' The element index is {i} and his number is {f.__next__()}')
