import pathlib
from typing import Union

import click
from external_sort import my_sort
PathType = Union[str, pathlib.Path]


@click.command()
@click.option("--file_count", prompt="Введите из скольки файлов считывать данные", default=1,
              type=click.IntRange(min=1), help="Введите количество файлов для сортировки")
@click.option("--output_into_file", default=False, help="Если вы хотите вывести все в отдельный файл введите"
                                                        "--output_into_file=True")
@click.option("--type_data", prompt="Введите тип данных", type=click.Choice(["i", "f", "s"]),
              help="Переменная принимает значения: "
                   "i - для целочисленных значений; "
                   "f - для чисел с плавающей запятой; "
                   "s - для строк ")
@click.option("--reverse", default=False, help="--reverse отвечает за то как сортировать"
                                               "по возрастанию или по убыванию")
def main(file_count: int, output_into_file: bool, type_data: str, reverse: bool) -> None:
    """
    Программ для внешней сортировки файлов
    :param file_count: количество файлов для сортировки
    :param output_into_file: флаг, отвечающий выводить ли результат в файл
    :param type_data: тип данных
    :param reverse: флаг, указывающий как сортировать (по убыванию или по возрастанию)
    :return: None
    """
    files, key = input_files(file_count, "Введите путь к файлу из которого будут считаны данные")
    output = ""
    if output_into_file:
        output = input_files(1, "Введите файл для вывода")[0][0]
    my_sort(files, output, reverse, key, type_data)
    pass


def input_files(file_count: int, massage: str) -> tuple[list[PathType], str]:
    """
    Функция для получения путей
    :param file_count: количество путей
    :param massage: сообщение для пользователя
    :return: список путей и ключ для csv файлов если такие вводились
    """
    files = []
    need_key = False
    key = ""
    for _ in range(file_count):
        file = click.prompt(f"{massage}", type=click.Path(exists=True, file_okay=True, readable=True))
        if file.count(".csv") == 1:
            need_key = True
        files.append(file)
    if need_key:
        key = click.prompt("Введите ключ для csv файла")
    return files, key


if __name__ == '__main__':
    main()
