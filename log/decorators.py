from functools import wraps


def log(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            logger.info(f'{func.__module__}, {func.__name__}, {result}')

            return result

        return wrapper

    return decorator
