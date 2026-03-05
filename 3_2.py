import warnings

def deprecated(message):
    def decorator(func):
        def wrapper(*args):
            warnings.warn(message, UserWarning)
            return func(*args)
        return wrapper
    return decorator

@deprecated('ne usay pliz')
def f(x):
    return x

print(f(1))