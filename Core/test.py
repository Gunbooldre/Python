# Sum of Digits
# Title: Sum of Digits of a Number
# Description:
# Write a Python function sum_of_digits(n) that takes an integer n as input and returns the sum of its digits. If the input number is negative, the function should still return the sum of the digits as a positive integer.
# Requirements:
# The function should be able to handle any integer value, including zero and negative numbers.
# The function should return the sum of the digits as an integer.
# Function Signature:
# def sum_of_digits(n: int) -> int:
#     # Your code here
#
#
# Examples:
# print(sum_of_digits(123))    # Output: 6  (1 + 2 + 3)
# print(sum_of_digits(-456))   # Output: 15 (4 + 5 + 6)
# print(sum_of_digits(0))      # Output: 0
# print(sum_of_digits(7891))   # Output: 25 (7 + 8 + 9 + 1)
# Notes:
# You may not use any libraries or functions that directly compute the sum of digits. Implement the logic manually.
# Consider how you will handle the input and ensure your solution is efficient and clear.


# def sum_of_digits(n: int) ->int:
#     n = abs(n)
#     total_number = 0
#     while n > 0:
#         total_number += n % 10
#         n //= 10
#     return total_number


# print(sum_of_digits(123))
# print(sum_of_digits(-456))
# print(sum_of_digits(-0))
# print(sum_of_digits(-7891))


# Best Time to Buy and Sell Stocks
# Problem statement
# Say you have an array for which the ith element is the price of a given stock on day i.
# If you were only permitted to complete at most one transaction (ie, buy one and sell one share of the stock), design an algorithm to find the maximum profit.
# Example :
# Input: 1 2 -> Expected output is 1
# Input: 5 50 51 1 3 20 -> Expected output is 46
# Input: 7 1 5 3 6 4 -> Expected Output: 5
# Input: 7 6 4 3 1 -> Expected Output 0 (No profit can be made)


# arr = [1,2,3,4,5]
def max_profit(arr):
    minP = float('inf')
    maxP = 0

    for i in arr:
        if i < minP:
            minP = i
        profit = i - minP
        if i > maxP:
            maxP = profit

    return maxP


print(max_profit([1, 2]))
print(max_profit([5,50,51,1,3,20]))
print(max_profit([7,1,5,3,6,4]))
print(max_profit([7,6,4,3,1]))
