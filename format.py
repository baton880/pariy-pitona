def format_number(x):
    s = f'{x:.3f}'
    p = s.split('.')
    a = p[0]
    b = p[1]
    r = ''
    c = 0
    i = len(a) - 1
    while i >= 0:
        r = a[i] + r
        c += 1
        if c == 3 and i != 0:
            r = ' ' + r
            c = 0
        i -= 1

    s = f'{r} .{b}'
    s = f'{s:*^30}'
    return s

x = float(input(''))
print(format_number(x))