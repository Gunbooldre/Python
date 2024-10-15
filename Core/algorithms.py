a = [1, 3, 4, 5, 6, 7, 8, 9, 10]
k = 11

def binary_seach(a: list, k: int) -> int:
    l, r = 0, len(a) - 1
    while l <= r:
        mid = (l + r) // 2
        if a[mid] < k:
            l = a[mid] - 1
        elif a[mid] > k:
            r = a[mid] + 1
        else:
            return a[mid]
    return -1


print(binary_seach(a, k))
