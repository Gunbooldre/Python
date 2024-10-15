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
import sys

def fibonacci(n):
    prev, cur = 0, 1
    result = []
    for _ in range(n):
        result.append(prev)
        prev, cur = cur, prev + cur
    return result

fib_sequence = fibonacci(10000)  # Генерируем 1000 чисел
print(f"Size of Fibonacci sequence (1000 elements): {sys.getsizeof(fib_sequence)} bytes")


class GeneratoreFibocci:
    def __init__(self):
        self.prev = 0
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        value = self.prev
        self.prev, self.current = self.current, self.prev + self.current
        return value


g = GeneratoreFibocci()
# for i in range(1, 10000):
#     print(f' The element index is {i} and his number is {f.__next__()}')
print(f"Size of Fibonacci generator object: {sys.getsizeof(g)} bytes")


class IteratoreFibonacci:
    def __init__(self, max_iterations=None):
        self.prev = 0
        self.current = 1
        self.iterations = 0
        self.max_iterations = max_iterations

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterations >= self.max_iterations:
            raise StopIteration
        value = self.prev
        self.prev, self.current = self.current, self.prev + self.current
        self.iterations += 1
        return value


i = IteratoreFibonacci(10000)  # Здесь передаем 10000 итераций
for num in range(10000):  # Первые 10 чисел
    next(i)

print(f"Size of Fibonacci Iteratore object: {sys.getsizeof(i)} bytes")
