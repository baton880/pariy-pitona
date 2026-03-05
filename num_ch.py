def count_symb(a):
    g = dict()
    for i in a:
        g[i] = 0
    for i in a:
        g[i] += 1
    return g

s = input('')
print(count_symb(s))