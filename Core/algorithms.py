a = [1, 3, 4, 5, 6, 7, 8, 9, 10]
k = 6

def binary_seach(a: list, k: int) -> int:
    l, r = 0, len(a) - 1
    while l <= r:
        mid = (l + r) // 2
        if a[mid] < k:
            l = mid + 1
        elif a[mid] > k:
            r = mid - 1
        else:
            print(f'Index of {k} is - {mid} ')
            break
    return -1


binary_seach(a, k)
