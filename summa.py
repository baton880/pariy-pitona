def two_sum(a, n):
    i = 0
    while i < len(a):
        j = i + 1
        while j < len(a):
            if a[i] + a[j] == n:
                return [i, j]
            j += 1
        i += 1

s = input('')
a = list(map(int, s.split()))
n = int(input(''))
print(two_sum(a, n))