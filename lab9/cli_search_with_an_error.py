from typing import Iterator, Union, Optional

import click
from sqlalchemy import true

import search_with_an_error
from colorama import init
import chardet


@click.command()
@click.option('--type_input', type=click.Choice(["string", "file"]), prompt="Как вы будете вводить данные",
              help="Для поиска по строке введите string,"
                   "а для поиска по файлу file")
@click.option('--sub_string', prompt="Какую строку искать, если их несколько можно ввести их через пробел в кавычках",
              help="Подстрока которой производиться поиск, "
                   "если их несколько вы можете ввести "
                   "их в кавычках через пробел")
@click.option('--case_sensitivity', default=False, help="Чувствительность к регистру")
@click.option('--method', type=click.Choice(["first", "last"]), default='first',
              help="first: поиск первого вхождения,"
                   "last: поиск последнего вхождения")
@click.option('--count', type=click.IntRange(min=1), default=1, help="Количество индексов которые нужно найти")
@click.option('--alph', default=False, help='Алфавит, который будет использовтся для поиска похожих слов')
@click.option('--n_jobs', default=3, type=click.IntRange(min=1), help='Кол-во потоков')
@click.option('--output', default='console', type=click.Choice(['console', 'file']), help='Как вывести ответ')
def main(type_input: str, sub_string: str, case_sensitivity: bool, method: str,
         count: int, alph: bool, n_jobs: int, output: str):
    init()
    sub_string = list(sub_string.split(" "))
    if len(sub_string) == 1:
        sub_string = sub_string[0]

    alphabet = None
    language = None
    if alph:
        alphabet, language = input_alphabet()

    if type_input == "file":
        file_path = input_file_path('Введите файл для поиска в нем')
        result = search_with_an_error.search_with_an_error_in_file(file_path, sub_string, case_sensitivity, method,
                                                                   count, alphabet, language, n_jobs)
        write_search_in_file(result, sub_string)
        write_results_into_file("output.txt", result)
    else:
        string = input_string()
        result = search_with_an_error.search_with_an_error(string, sub_string, case_sensitivity, method, count,
                                                           alphabet, language, n_jobs)

        write_search_in_string(result, string, sub_string)
    if output == 'file':
        write_results_into_file(input_file_path('Введите файл для сохранения'), result)
    pass


def write_results_into_file(file_path: str, result: Optional[dict]) -> None:
    """
    Функция для записи результатов в файл
    :param file_path: путь к файлу
    :param result: результаты
    :return: None
    """
    with open(file_path, 'w', encoding='windows-1251') as f:
        count_written = 0
        for key, value in result.items():
            if not isinstance(value, dict):
                f.write(f'{key}: {value}\n')
                count_written += 1
                if count_written == 10:
                    break
                continue
            else:
                f.write(f'{key}:\n')
            for key_under, value_under in value.items():
                f.write(f'\t{key_under}: {value_under}\n')
                count_written += 1
                if count_written == 10:
                    break


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
                print('\t' + next(count_color) + f'{key_under}: {value_under}')
                count_written += 1
                if count_written == 10:
                    return


def write_search_in_string(result: Optional[dict], string: str, sub_string: Union[str, list[str]]) -> None:
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


def input_alphabet() -> tuple[list[str, ...], str]:
    language = ''
    while language != 'ru' and language != 'en':
        language = click.prompt('Введите язык (поддерживается ru и en)')
    len_alphabet = click.prompt('Введите кол-во букв в алфавите', type=click.IntRange(min=2))
    alphabet = []

    for i in range(len_alphabet):
        language_code_correct = False
        if language == 'en':
            language_code = 'ascii'
        else:
            language_code = 'ISO-8859-1'
        char = ''
        while not language_code_correct:
            char = click.prompt(f'Введите {i + 1} букву алфавита')
            if chardet.detect(char.encode('cp1251'))['encoding'] == language_code:
                language_code_correct = True
        alphabet.append(char)
    return alphabet, language


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


def input_file_path(message: str) -> str:
    """
    Функция для получения от пользователя пити к файлу
    :return: путь к файлу
    """
    file_path = click.prompt(f"{message}", type=click.Path(exists=True, file_okay=True, readable=True))
    return file_path


def input_string() -> str:
    """
    Функция для получения строки для поиска
    :return: строка для поиска
    """
    string = click.prompt("Введите строку, где будет произведен поиск")
    return string


if __name__ == '__main__':
    main()
    # word = 'ком'
    # print(main('string', word, False, 'last', 10,
    #                            alph=True, n_jobs=3, output='console'))
    # # print(search_with_an_error_in_file("input.txt", word, False, method='last', count=10, alphabet=['b', 't', 'c'],
    # #                                    language='en', n_jobs=3))
    # # main('file', 'aba ab', False, 'last', 10, False, 3, 'output.txt')
