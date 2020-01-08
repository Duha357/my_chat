from functools import wraps


def log(logger):
    def decorator(func):
        """
        Логгирует использование функции

        :param func:
        :return:
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            logger.info(f'{func.__module__}, {func.__name__}, {result}')

            return result

        return wrapper

    return decorator
