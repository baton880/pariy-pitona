import warnings

def f(x):
    warnings.warn("Dont use me i am outdated!!!", UserWarning)
    return x

print(f(1))
