import functools
import unittest.mock


def lru_cache(function=None, *, maxsize=None):
    """
    Декоратор для кеширования работы функции
    Используем OrderedDict из модуля collections, а не обычный dict,
    чтобы не создавать дополнительные коллекции для хранения порядка вызовов функции
    Параметр function используем для того, чтобы при использовании декоратора без скобок,
    задекорированная функция передавалась в этот параметр
    """
    cache = {}

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if (func_args := args + tuple(kwargs.items())) in cache: # объединяем все аргументы в 1 кортеж
                return cache[func_args]
            else:
                result = func(*args, **kwargs)

                if maxsize is not None and len(cache) == maxsize:
                    cache.pop(next(iter(cache)))

                cache[func_args] = result

                return result
        return wrapper

    if function:
        return decorator(function)
    return decorator

@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':
    
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
