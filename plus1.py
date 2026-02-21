def plus_one(a):
    i = len(a) - 1
    while i >= 0:
        if a[i] < 9:
            a[i] += 1
            return a
        a[i] = 0
        i -= 1
    return [1] + a

s = input('')
a = list(map(int, s.split()))
print(plus_one(a))