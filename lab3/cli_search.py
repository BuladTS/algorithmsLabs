import copy
from typing import Union, Iterator

import click
from search import search
from search_in_file import search_in_file
from colorama import init


# @click.command()
# @click.option('--type_input', type=click.Choice(["string", "file"]), prompt="Как вы будете вводить данные",
#               help="Для поиска по строке введите string,"
#                    "а для поиска по файлу file")
# @click.option('--sub_string', prompt="Какую строку искать, если их несколько можно ввести их через _",
#               help="Подстрока которой производиться поиск, "
#                    "если их несколько вы можете ввести "
#                    "их в ковычках")
# @click.option('--case_sensitivity', default=False, help="Чувствительность к регистру")
# @click.option('--method', type=click.Choice(["first", "last"]), default='first',
#               help="first: поиск первого вхождения,"
#                    "last: поиск последнего вхождения")
# @click.option('--count', type=click.IntRange(min=1), default=1, help="Количество индексов которые нужно найти")
def main(type_input: str, sub_string: str, case_sensitivity: bool, method: str, count: int) -> None:
    """
    Основная функция для работы cli
    :param type_input: тип ввода данных
    :param sub_string: строка, которой поиск ведется
    :param case_sensitivity: чувствительность к регистру
    :param method: означает какое вхождение мы ищем
    :param count: количество вхождений которые нужно найти
    :return: None
    """
    init()
    sub_string = list(sub_string.split(" "))
    if len(sub_string) == 1:
        sub_string = sub_string[0]
    if type_input == "file":
        file_path = input_file_path()
        result = search_in_file(file_path, sub_string, case_sensitivity, method, count)
        write_search_in_file(result, sub_string)
    else:
        string = input_string()
        result = search(string, sub_string, case_sensitivity, method, count)
        write_search_in_string(result, string, sub_string)


def write_search_in_file(result: dict, sub_string: Union[str, list[str]]) -> None:
    """
    Функция для вывода результата поиска в файле
    :param result: данные полученные поиском в файле
    :param sub_string: строки поиск, которых проводиться
    :return: None
    """
    count_written = 0
    count_color = next_color()
    if isinstance(sub_string, str):
        for key, value in result:
            print(next(count_color) + f'{key}: {value}')
            count_written += 1
            if count_written == 10:
                break
    else:
        for key, value in result.items():
            if value is None:
                print(next(count_color) + f'{key}: {value}')
                continue
            else:
                print(next(count_color) + f'{key}:')
            for key_under, value_under in value.items():
                print(next(count_color) + f'{key_under}: {value_under}')
                count_written += 1
                if count_written == 10:
                    return


def write_search_in_string(result: Union[None, dict], string: str, sub_string: Union[str, list[str]]) -> None:
    """
    Функция для вывода результата поиска в строке
    :param result: данные полученные поиском в строке
    :param string
    :param sub_string: строки поиск, которых проводиться
    :return: None
    """
    count_written = 0
    count_color = next_color()
    color = next(count_color)
    if isinstance(sub_string, str):
        print(color + f'{sub_string}: {result}')
        i = 0
        j = 0

        while i < len(string):
            if j == len(result):
                print(f'\33[31m{string[i:]}')
                break
            print(f'\33[31m{string[i:result[j]]}', end="")
            if result[j] < i:
                print(f'{color}{string[i:len(sub_string) + result[j]]}', end="")
                i += len(sub_string) - i + result[j]
                j += 1
            else:
                i = result[j]
                j += 1
                print(f'{color}{string[i:i + len(sub_string)]}', end="")
                i += len(sub_string)

    elif result is None:
        print(next(count_color) + 'Ничего не найдено')
    else:
        for key, value in result.items():
            color = next(count_color)
            print(color + f'{key}: {value}')
            count_written += 1

            if value is None:
                break

            i = 0
            j = 0

            while i < len(string):
                if j == len(value):
                    print(f'\33[31m{string[i:]}', end="")
                    break
                print(f'\33[31m{string[i:value[j]]}', end="")
                if value[j] < i:
                    print(f'{color}{string[i:len(key) + value[j]]}', end="")
                    i += len(key) - i + value[j]
                    j += 1
                else:
                    i = value[j]
                    j += 1
                    print(f'{color}{string[i:i + len(key)]}', end="")
                    i += len(key)
            print("\n")
            if count_written == 10:
                break


def next_color() -> Iterator[str]:
    """
    Функция для смены кода цвета
    :return: код цвета
    """
    count_color = 32
    while True:
        if count_color == 38:
            count_color = 32
        count_color += 1
        yield f'\33[{count_color}m'


def input_file_path() -> str:
    """
    Функция для получения от пользователя пити к файлу
    :return: путь к файлу
    """
    file_path = click.prompt("Введите путь до файла", type=click.Path(exists=True, file_okay=True, readable=True))
    return file_path


def input_string() -> str:
    """
    Функция для получения строки для поиска
    :return: строка для поиска
    """
    string = click.prompt("Введите строку, где будет произведен поиск")
    return string


if __name__ == "__main__":
    # main()
    main("string", "aba", False, "first", 2)
