from typing import Optional, Union


def search(string: str, sub_string: Union[str, list[str]],
           case_sensitivity=False, method: str = "first",
           count: Optional[int] = None) -> Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Функция для поиска подстрок в строке методом Кнута-Морриса-Пратта
    :param string: строка в которой ведется поиск
    :param sub_string: строки которые нужно найти
    :param case_sensitivity: чувствительность к регистру
    :param method: означает какое вхождение ищется первое либо последнее
    :param count: количество вхождений которые нужно найти
    :return: индексы вхождений
    """
    result = {}
    count_result = 0
    count_none = 0
    if not case_sensitivity:
        string = string.lower()
        if isinstance(sub_string, str):
            sub_string = sub_string.lower()
        else:
            for i in sub_string:
                i.lower()
    if isinstance(sub_string, str):
        result = update_result(string, sub_string, method, count)
    else:
        for i in sub_string:
            result[i] = update_result(string, i, method, count)

            if result[i] is None:
                count_none += 1
            else:
                count_result += len(result[i])

    if count_none == len(sub_string):
        result = None
    if count_result > count:
        result = remove_needless_result(result, method, count)
    return result


def remove_needless_result(removed: dict, method: str, count: int) -> dict:
    """
    Функция для дополнительной корректировки ответа
    :param removed: список ответов которые уже получены
    :param method: уфлаг метода, который указывает какой элемент нужно удалить max или min
    :param count: количество ответов до которых нжно укоротить уже полученные ответы
    :return: финальный ответ удовлетворяющий всем условиям
    """
    elements = []
    for i in removed.values():
        if i is not None:
            elements.extend(i)
    elements.sort()
    removed = {key: value for key, value in removed.items() if not (value is None)}
    if method == "first":
        elements = elements[::-1]
    i = 0
    while len(elements) > count:
        for key, value in removed.items():
            if value is not None and elements[i] in value:
                new_value = [x for x in value if x != elements[i]]
                if len(new_value) == 0:
                    removed[key] = None
                    elements.remove(elements[i])
                    break
                else:
                    removed[key] = tuple(new_value)
                    elements.remove(elements[i])
                    break

        # i += 1
    return removed


def update_result(string: str, sub_string: str, method: str, count: int) -> tuple:
    """
    Функция для корректировки ответа
    :param string: строка в которой, ведется поиск подстроки
    :param sub_string: строка, поиск которой ведется поиск
    :param method: флаг метода, нужно ли инвертировать массив
    :param count: количество индексов, которые нужно найти
    :return: кортеж из индексов, где встречается подстрока
    """
    temp_result = find_sup(string, sub_string)
    if len(temp_result) == 0:
        result = None
    elif method == "first":
        result = temp_result[:count]
    else:
        result = temp_result[::-1][:count]
    return result


def prefix(string: str) -> list:
    """
    Функция для нахождения максимального префикса
    :param string: строка в, которой производиться поиск префикса
    :return: список максимальных префиксов для строки
    """
    prefix_array = [0] * len(string)
    j = 0
    i = 1
    while i < len(string):
        if string[j] == string[i]:
            prefix_array[i] = j + 1
            i += 1
            j += 1
        else:
            if j == 0:
                prefix_array[i] = 0
                i += 1
            else:
                j = prefix_array[j - 1]
    return prefix_array


def find_sup(string: str, sup_string: str) -> tuple:
    """
    Функция для нахождения всех подстрок
    :param string: строка в которой идет поиск
    :param sup_string: строка которую мы ищем
    :return: кортеж из индексов, где встречается подстрока
    """
    prefix_array = prefix(sup_string)
    len_string = len(string)
    len_sup_string = len(sup_string)
    into = []
    i = 0
    j = 0
    while i < len_string:
        if string[i] == sup_string[j]:
            i += 1
            j += 1
            if j == len_sup_string:
                into.append(i - len_sup_string)
                j = prefix_array[j - 1]
        else:
            if j > 0:
                j = prefix_array[j - 1]
            else:
                i += 1
    return tuple(into)


def main():
    pass


if __name__ == "__main__":
    main()
