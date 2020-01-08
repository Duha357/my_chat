from functools import wraps


def log(logger):
    def my_decorator(func):
        """
        Логгирует использование функции

        :param func:
        :return:
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f'{func.__module__}, {func.__name__} : {args}, {kwargs}')

            return func(*args, **kwargs)

        return wrapper

    return my_decorator
