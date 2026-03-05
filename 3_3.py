import warnings

def mock(ret):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return ret
        return wrapper
    return decorator

@mock(ret='six seven\n')
def f1(x, y, z):
    return x + y + z

@mock(ret='неа')
def f2(z=1, y=2):
    return y * z

print(f1(1, 2, 3))
print(f2(9, y=1))