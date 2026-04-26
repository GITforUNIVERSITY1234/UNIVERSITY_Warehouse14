"""
from datetime import datetime

# Объявление декоратора - функция, которая принимает на вход другую функцию,
# поведение которой нужно расширить
def do_twice(func):
    # Функция-обёртка - здесь мы вызываем нашу исходную функцию +
    # дописываем логику, которая нам нужна
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    # Возвращаем функцию-обертку
    return wrapper

# Помечаем функцию "my_func" декоратором "do_twice"
@do_twice
def my_func():
    print("hello!")
    return 35

# Декоратор, вычисляющий, сколько времени выполняется обернутая функция
def measure_time(func):
    def wrapper(*args, **kwargs):
        # Время начала выполнения функции
        start_time = datetime.now()
        # Вызываем функцию
        res = func(*args, **kwargs)
        # Возвращаем результат выполнения функции, а также время ее работы
        return (res, datetime.now() - start_time)
    # Возвращаем функцию-обертку
    return wrapper

@measure_time
def sum_of_n_ints(n):
    sum = 0
    for j in range(n):
        for i in range(n):
            sum += i
    return sum

s, duration = sum_of_n_ints(10000)
print(f"sum: {s}, duration: {duration}")
"""
