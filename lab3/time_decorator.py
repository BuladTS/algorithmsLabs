import time
from typing import Callable


def time_decorator(func: Callable):
    """
    Декоратор для засечения времени выполнения времени
    :param func: функция, время которой засекаеться
    :return: Обертку функции
    """

    def _wrapper(*args, **kwargs):
        time_start = time.time()
        func(*args, **kwargs)
        print(f'func: {func.__name__}')
        print(f'time: {time.time() - time_start:2.4f} sec')

    return _wrapper
