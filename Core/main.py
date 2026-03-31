from typing import Callable, Any, Self
from dataclasses import dataclass

# class DemoDescriptions:
#
#     def __init__(self) -> None:
#         self.value = 1
#
#     def __get__(self, instance: object | None, owner: type ) -> int | DemoDescriptions:
#         print(f"__get__ called with instance: {instance} and owner: {owner.__name__}")
#         if instance is None:
#             return self
#         return self.value
#
#     def __set__(self, instance, value) -> None:
#         print(f"__set__ called with instance: {instance} and value: {value}")
#         self.value = value
#
# class Main:
#     x = DemoDescriptions()
#
# def main() -> None:
#     m = Main()
#     print(m.x)
#     m.x = "10"
#     print(m.x)
#     print(Main.x)
#
#
#


# class SimpleProp:
#     def __init__(self, value: Callable[[Any], Any]):
#         self._value = value
#
#     def __get__(self, instance, owner):
#         if instance is None:
#             return self
#         return self._value(instance)
#
# class User:
#     def __init__(self, first: str, last: str):
#         self.first = first
#         self.last = last
#
#     @SimpleProp
#     def full_name(self) -> str:
#         return self.first + " " + self.last
#
# def main():
#     user = User("Joe", "Doe")
#     print(user.full_name)

########################################################################################################################

class Price(float):
    def __new__(cls, value)-> Self:
        val = float(value)
        if val < 0:
            raise ValueError("Price must be positive")
        return  super().__new__(cls, val)

class Percent(float):
    def __new__(cls, value)-> Self:
        val = float(value)
        if not 0.0 <= val <= 1.0:
            raise ValueError("Percent must be between 0 and 1")
        return super().__new__(cls, val)

def apply_discount(price: Price, discount: Percent) -> float:
    return price * (1 - discount)

def main():
    price = 100

    discounted_price = apply_discount(Price(price), Percent(0.2))
    print(f"Discounted price: {discounted_price}") #80

    # wrong_one = apply_discount(Price(price), Percent(20))
    # print(f"Wrong price: {wrong_one}")
    #
    # negative_price = apply_discount(Price(-price), Percent(0.2))
    # print(f"Negative price: {negative_price}")

if __name__ == "__main__":
    main()

