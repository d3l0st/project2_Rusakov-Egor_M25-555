import time
from functools import wraps

import prompt


def handle_db_errors(func):
    """Декоратор для обработки ошибок базы данных"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            return f"Ошибка: Файл данных не найден. {e}"
        except KeyError as e:
            return f"Ошибка: Таблица или столбец {e} не найден."
        except ValueError as e:
            return f"Ошибка валидации: {e}"
        except Exception as e:
            return f"Произошла непредвиденная ошибка: {e}"
    return wrapper


def confirm_action(action_name):
    """Декоратор для подтверждения опасных операций"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = prompt.string(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )
            if response.lower() != 'y':
                return "Операция отменена."
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func):
    """Декоратор для замера времени выполнения"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        duration = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {duration:.3f} секунд.")
        return result
    return wrapper


def create_cacher():
    """Фабрика для создания кэшера с замыканием"""
    cache = {}
    
    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result
    
    return cache_result


# Создаем глобальный кэшер
cacher = create_cacher()