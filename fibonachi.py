def fib_rec(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_rec(n - 1) + fib_rec(n - 2)

def fib_for(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    a = 0
    b = 1
    i = 2
    while i <= n:
        c = a + b
        a = b
        b = c
        i += 1
    return b

n = int(input(''))
print(fib_rec(n))
print(fib_for(n))