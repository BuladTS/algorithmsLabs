from typing import Optional, Callable, Union
from my_sort import my_sort
from animation import animation
from gen_quick_sort import gen_quick_sort


def sort_file(file_path: str, reverse: bool = False, write_file_path: str = "", run_gif: bool = False,
              key: Optional[Callable] = None, cmp: Optional[Callable] = None) -> Union[list[int], list[str]]:
    """
    Функция для сортировки данных из файла
    :param file_path: путь к файлу
    :param reverse: флаг, указывающий как сортировать по убыванию или возрастанию
    :param write_file_path: путь куда записывать файл
    :param run_gif: флаг указывающий, запускать ли анимацию
    :param key: функция для получения значения
    :param cmp: функция вида def func(x,y) -> bool, для сравнения двух значений
    :return: Отсортированный массив
    """
    with open(file_path, "r") as f:
        file_strings = f.readlines()
    array = normalize_data(file_strings)
    if run_gif and len(array) != 0 and isinstance(array[0], int):
        animation(array, gen_quick_sort(array, 0, len(array) - 1, reverse))
    else:
        array = my_sort(array, reverse, key, cmp)
    if write_file_path != "":
        with open(write_file_path, "w") as f:
            for i in array:
                f.write(str(i) + ' ')
    return array


def normalize_data(file_strings: list[str]) -> Union[list[str], list[int]]:
    """
    Функция для привидения данных в виде массива:
    :param file_strings: все строки в файле:
    :return: данные в виде единого массива
    """
    if check_have_only_nums(file_strings):
        normalized_data = normalize_to_int(file_strings)
    else:
        normalized_data = normalize_to_str(file_strings)

    return normalized_data


def normalize_to_str(file_strings: list[str]) -> list[str]:
    """
    Функция для создания массива из строк на основе всех строк в файле:
    :param file_strings: все строки в файле:
    :return: единый массив строк
    """
    result = []
    for i in file_strings:
        result += i.split()
    return result


def normalize_to_int(file_string: list[str]) -> list[int]:
    """
    Функция для создания массива из чисел на основе всех строк в файле:
    :param file_string: все строки в файле:
    :return: единый массив чисел
    """
    result = []
    for i in file_string:
        result += [int(x) for x in i.split()]
    return result


def check_have_only_nums(file_string: list[str]) -> bool:
    """
    Функция для проверки состоит ли файл из чисел:
    :param file_string: все строки в файле:
    :return: единый массив чисел
    """
    for i in file_string:
        sup_string = i.replace(" ", "")
        sup_string = sup_string.replace("\n", "")
        if sup_string == "":
            continue
        try:
            eval(sup_string)
        except NameError:
            return False
        except SyntaxError:
            return False
    return True


def main():
    pass
    # file_path = '../../output.txt'
    # sort_file(file_path, write_file_path='../../input1.txt')


if __name__ == '__main__':
    main()
