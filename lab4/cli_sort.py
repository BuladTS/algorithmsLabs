from typing import Union

import click

from my_sort import my_sort
from sort_file import sort_file
from animation import animation
from gen_quick_sort import gen_quick_sort


@click.command()
@click.option("--input_from_file", default=False, help="Если вы хотите ввести данные из файла"
                                                       "введите --input_into_file=True")
@click.option("--output_to_file", default=False, help="Если вы хотите вывести результаты в файл"
                                                      "введите --output_to_file=True")
@click.option("--reverse", default=False, help="Если вы хотите отсортировать в обратном порядке"
                                               "введите --reverse=True")
@click.option("--run_gif", default=False, help="Анимация работает только с числовыми данными,"
                                               "если вы хотите визуализировать сортировка"
                                               "введите --run_gif=True")
@click.argument("array", nargs=-1, type=str)
def main(array: tuple, reverse: bool, input_from_file: bool, output_to_file: bool, run_gif: bool) -> None:
    """
    Основная функция для работы с cli
    :param array: кортеж полученный из командной строки
    :param reverse: флаг, указывающий как сортировать по убыванию или возрастанию
    :param input_from_file: флаг, указывающий как вводятся данные
    :param output_to_file: флаг, указывающий как выводиться результат
    :param run_gif: флаг, указывающий запускать ли анимацию
    :return: None
    """
    normalized_array = normalize_data(array)
    if run_gif and not input_from_file and len(normalized_array) != 0 and isinstance(normalized_array[0], int):
        result = normalized_array
        animation(result, gen_quick_sort(result, 0, len(result) - 1, reverse))
    else:
        result = my_sort(normalized_array, reverse)
    if input_from_file:
        input_file_path = request_file_path("Введите путь к файлу, откуда будут считаны данные")
        result = sort_file(input_file_path, reverse, run_gif=run_gif)
    if output_to_file:
        output_file_path = request_file_path("Введите путь к файлу, куда записывать результат")
        write_to_file(output_file_path, result)
    else:
        print(result)


def write_to_file(file_path: str, result: Union[list[str], list[int]]) -> None:
    """
    Функция для записи результата в файл
    :param file_path: путь к файлу
    :param result: результат, который нужно записать
    :return: None
    """
    with open(file_path, "w") as f:
        for i in result:
            f.write(str(i) + ' ')


def request_file_path(massage: str) -> str:
    """
    Функция для запроса у пользователя пути к файлу:
    :param massage: сообщение, которое выводиться пользователю:
    :return: путь к файлу
    """
    file_path = click.prompt(f"{massage}", type=click.Path(exists=True, file_okay=True, readable=True))
    return file_path


def normalize_data(data: tuple) -> Union[list[str], list[int]]:
    """
    Функция для нормализации данных, т.е определение всех данных к int или str
    :param data: данные для нормализации
    :return: нормализованные данные
    """
    result = list(data)
    try:
        result = list(map(int, data))
    except ValueError:
        return result
    return result


if __name__ == "__main__":
    main()
