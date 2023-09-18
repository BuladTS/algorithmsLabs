from typing import Union, Optional
from search import search


def search_in_file(file_path: str, sub_string: Union[str, list[str]],
                   case_sensitivity=False, method: str = "first",
                   count: Optional[int] = None) -> Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Функция для построчного поиска подстроки в файле
    :param file_path: путь к файлу
    :param sub_string: строки которые нужно найти
    :param case_sensitivity: чувствительность к регистру
    :param method: означает какое вхождение ищется первое либо последнее
    :param count: количество вхождений которые нужно найти
    :return: словарь всех найденных индексов в каждой строке
    """
    result = {}
    count_lines = 0
    with open(file_path, 'r') as f:
        while count > 0:
            string = f.readline()
            if string == '':
                break
            count_lines += 1
            temp_key = str(count_lines) + ' строка'
            result[temp_key] = search(string, sub_string, case_sensitivity, method, count)
            if isinstance(sub_string, str) and result[temp_key] is not None:
                count -= len(result[temp_key])
            else:
                if result[temp_key] is not None:
                    for i in result[temp_key].values():
                        if i is not None:
                            count -= len(i)
    return result


def main():
    file_path = "../../output.txt"
    print(search_in_file(file_path, ["a", "b"], False, 'first', 50))


if __name__ == "__main__":
    main()
