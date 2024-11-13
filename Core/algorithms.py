# a = [1, 3, 4, 5, 6, 7, 8, 9, 10]
# k = 6
#
# def binary_seach(a: list, k: int) -> int:
#     l, r = 0, len(a) - 1
#     while l <= r:
#         mid = (l + r) // 2
#         if a[mid] < k:
#             l = mid + 1
#         elif a[mid] > k:
#             r = mid - 1
#         else:
#             print(f'Index of {k} is - {mid} ')
#             break
#     return -1
#
#
# binary_seach(a, k)


import sys


import sys


# def main():
#     arr = []
#     num = int(input())
#     arr = list(map(int, input().split()))
#     x = int(input())
#
#     closest_num = arr[0]
#     min_diff = abs(closest_num - x)
#
#     for i in arr:
#         diff = abs(i - x)
#         if diff < min_diff:
#             min_diff = diff
#             closest_num = i
#     print(closest_num)

def main():
    n = int(input())
    temp = {}
    for i in range(n):
        word1, word2 = input().split()
        temp[word1] = word2
        temp[word2] = word1
    t = input()
    print(temp.get(t, ""))

if __name__ == '__main__':
    main()
