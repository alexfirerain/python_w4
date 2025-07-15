# function definition in another function
import time


def answer(question):
    return 'думайте сами'


def dialog():
    def answer(question):
        if question.lower().startswith('когда'):
            return 'Никогда'
        else:
            return 'Упс!'

    question = input()
    while question != '':
        print(answer((question)))
        question = input()


# dialog()


# переопределение функции
# def upper_print(another_func):
#     # объявление внутренней
#     def reassigned_func(*args, **kwargs):
#         # модифицируем аргумент
#         args_up = [str(arg).upper() for arg in args]
#         another_func(*args_up, **kwargs)
#
#     return reassigned_func


# new_print = upper_print(print)
#
# new_print('привЕт покА')


# ещё раз
def upper_print(another_func):
    def reassigned_func(*args, **kwargs):
        case = kwargs.pop('case', None)
        args_up = ''
        if case == 'U':
            args_up = [str(arg).upper() for arg in args]
        elif case == 'L':
            args_up = [str(arg).lower() for arg in args]
        else:
            args_up = args
        another_func(*args_up, **kwargs)

    return reassigned_func


new_print = upper_print(print)

new_print('ХуЧи-кУчИ')
new_print('ХуЧи-кУчИ', case='L')
new_print('ХуЧи-кУчИ', case='U')

"""
NON LOCALE
"""


def outer():
    x = 5

    def inner():
        nonlocal x
        print('Нелокальный икс это', x)
        x = 10

    inner()
    print('Новый икс', x)


outer()
"""
теперь собственно ДЕКОРАТОРЫ
"""


def logger(func):
    counter = 0

    def decorated_func(*args, **kwargs):
        nonlocal counter
        counter += 1
        print(counter, '→', 'Аргументы:', args, '\nИменованные аргументы:', kwargs)
        result = func(*args, **kwargs)
        print('\n____', 'Результат:', result, '\n____')

    return decorated_func

@logger
def make_burger(meal='говядиной', onion=False, tomato=False):
    print('булочка')
    if onion:
        print('луковые кольца')
    print('котлета с', meal)
    if tomato:
        print('помидорные кольца')
    print('булочка')
    print()

make_burger()
make_burger(onion=True)
make_burger()

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        finish = time.time()
        print(f'Функция {func.__name__} выполнена за {finish - start:.4f} мс')
        return result
    return wrapper

@timing
def test():
    time.sleep(0.8)

test()