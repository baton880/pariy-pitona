def is_correct_brackets_seq(s):
    k = 0
    for i in s:
        if i == '(':
            k += 1
        else:
            k -= 1
        if k < 0:
            return False
    return k == 0

s = input('')
print(is_correct_brackets_seq(s))