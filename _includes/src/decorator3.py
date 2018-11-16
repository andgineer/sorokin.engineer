import inspect
import functools


def my_decorator(original_function):
    @functools.wraps
    def wrapper(*args, **kwargs):
        try:
            return original_function(*args, **kwargs)
        finally:
            some_clean_up()
    wrapper.__signature__ = inspect.signature(original_function)
    return wrapper