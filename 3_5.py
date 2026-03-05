def singledispatch(func):
    registry = dict()
    def wrapper(*args, **kwargs):
        x = args[0]
        t = type(x)
        if t in registry:
            return registry[t](*args, **kwargs)
        return func(*args, **kwargs)
    def register(type_key):
        def decorator(impl_func):
            registry[type_key] = impl_func
            return impl_func
        return decorator
    wrapper.register = register
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__module__ = func.__module__
    return wrapper

@singledispatch
def f1(a):
    return 'im not implemented'

@f1.register(int)
def _(a):
    return f"{a} im int"

@f1.register(str)
def _(a):
    return f"{a} im string"

print(f1('213'))
print(f1(213))
print(f1([213]))