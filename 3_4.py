import warnings

def wrap(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__module__ = func.__module__
    return wrapper

@wrap
def f1():
    """ansadicniusdnc. """
    return 'бебебебе'

print(f1.__name__)
print(f1.__doc__)
