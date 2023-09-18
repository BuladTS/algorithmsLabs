from collections import deque
from typing import Union, Optional

import requests
import chardet
from multiprocessing.pool import ThreadPool
from file_read_backwards import FileReadBackwards

import search


def check_word(word: str, lang: str) -> bool:
    """
    Функция для проверки является ли строка словом, аббревиатурой
    :param word:
    :param lang:
    :return:
    """
    address = 'https://speller.yandex.net/services/spellservice.json/checkText'
    response = requests.get(f'{address}?text={word}&lang={lang}').json()
    if not response:
        return True
    elif response[0]['code'] == 1:
        return False
    return False


def levenstain(str_1: str, str_2: str) -> int:
    """
    Функция для вычисления расстояния Левенштейна между строками
    :param str_1: первая сторока
    :param str_2: вторая строка
    :return: расстояния Левенштейна между строками
    """
    len_cut_str, len_long_str = len(str_1), len(str_2)
    if len_cut_str > len_long_str:
        str_1, str_2 = str_2, str_1
        len_cut_str, len_long_str = len_long_str, len_cut_str

    current_row = range(len_cut_str + 1)
    for i in range(1, len_long_str + 1):
        previous_row, current_row = current_row, [i] + [0] * len_cut_str
        for j in range(1, len_cut_str + 1):
            variants = [current_row[j - 1] + 1, previous_row[j - 1], previous_row[j] + 1]
            if str_1[j - 1] != str_2[i - 1]:
                variants[1] += 1
            current_row[j] = min(variants)

    return current_row[len_cut_str]


class Node:
    """
    Узел дерева
    """

    def __init__(self, word: str):
        """
        Инициализация узла
        :param word: слово в узле
        """
        self.word = word
        self.children = {}


def add_child(parent: Node, child: Node) -> None:
    """
    Функция для добавления ветвей дерева
    :param parent: родительский узел
    :param child: дочерний узел
    :return: None
    """
    if not parent.word:
        print("У корня нет слова")
        return

    if not child.word:
        print("У потомка нет корня")

    distance = levenstain(parent.word, child.word)

    if distance in parent.children.keys():
        add_child(parent.children[distance], child)
    else:
        parent.children[distance] = child


def get_similar_words(parent: Node, word: str, k: int) -> list[str, ...]:
    """
    Функция для нахождения слов похожих на word с расстоянием Левенштейна
    меньшим k
    :param parent: узел для начала поиска
    :param word: слово по которому производиться поиск
    :param k: возможная погрешность
    :return: слова находящиеся в диапазоне погрешности
    """
    words = []

    if parent.children == {}:
        return []

    candidates = deque([parent])
    while candidates:
        node = candidates.popleft()
        candidate, children = node.word, node.children

        distance = levenstain(word, candidate)
        if distance <= k:
            words.append(candidate)
        low, high = distance - k, distance + k

        candidates.extend(c for d, c in children.items() if low <= d <= high)

    return words
    # distance = levenstain(word, root.word)
    # lower, upper = distance - k, distance + k
    # if distance <= k:
    #     words.append(root.word)


def any_variants(word: str, alphabet: Optional[list[str, ...]] = None,
                 language: Optional[str] = None) -> list[str, ...]:
    """
    Функция для подбора всех осмысленных слов
    :param word: слово для изменения
    :param alphabet: алфавит для подбора
    :param language: язык алфавита
    :return: список осмысленных слов полученных изменением с расстоянием левинштейна 1
    """
    variants = []
    if alphabet is None:
        if chardet.detect(word.encode('cp1251'))['encoding'] == 'ascii':
            lang = 'en'
        elif chardet.detect(word.encode('cp1251'))['encoding'] == 'windows-1251':
            lang = 'ru'
        else:
            raise ValueError('Строка состоит из разных алфавитов')
        if lang == 'ru':
            a = ord('а')
            alphabet = [chr(i) for i in range(a, a + 6)] + [chr(a + 33)] + [chr(i) for i in range(a + 6, a + 32)]
        else:
            alphabet = list(map(chr, range(97, 123)))
    else:
        lang = language
    for i in range(len(word) - 1):
        if check_word(word[:i] + word[i + 1:], lang):
            variants.append(word[:i] + word[i + 1:])
    for i in alphabet:
        for j in range(len(word)):
            if check_word(word[:j] + i + word[j:], lang):
                variants.append(word[:j] + i + word[j:])
            if check_word(word[:j] + i + word[j + 1:], lang):
                variants.append(word[:j] + i + word[j + 1:])

    return list(set(variants))


def search_with_an_error(string: str, sub_string: Union[str, list[str]],
                         case_sensitivity=False, method: str = "first",
                         count: Optional[int] = None, alphabet: Optional[list[str, ...]] = None,
                         language: Optional[str] = None,
                         n_jobs: int = 1) -> Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Функция для поиска подстроки с ошибкой
    :param string: строка в которой производиться поиск
    :param sub_string: строка(и) для поиска
    :param case_sensitivity: восприимчивость к регистру
    :param method: означает какое вхождение ищется первое либо последнее
    :param count: кол-во вхождений, которые нужно найти
    :param alphabet: алфавит, который будет использовтся для поиска похожих слов
    :param language:язык алфавита
    :param n_jobs:кол-во потоков
    :return: индексы вхождений
    """
    words_with_mistake = []
    if isinstance(sub_string, str):
        a = any_variants(sub_string, alphabet, language)
        words_with_mistake += a
    else:
        for i in sub_string:
            words_with_mistake += any_variants(i, alphabet, language)
            words_with_mistake += [i]

    results = {}
    count_sub_strings_in_thread = len(words_with_mistake) // n_jobs
    if count_sub_strings_in_thread > 0:
        threads = []
        threads_pool = ThreadPool(processes=n_jobs)
        for i in range(n_jobs):
            if i == n_jobs - 1:
                sub_string_for_thread = words_with_mistake[i * count_sub_strings_in_thread:]
            else:
                sub_string_for_thread = words_with_mistake[i * count_sub_strings_in_thread:
                                                           (i + 1) * count_sub_strings_in_thread]

            threads.append(threads_pool.apply_async(search.search, args=(string, sub_string_for_thread, case_sensitivity,
                                                                         method, count),
            ))
        for i in range(n_jobs):
            res = threads[i].get()
            if res is not None:
                res = {key: value for key, value in res.items() if not (value is None)}
                results |= res

        if results != {}:
            results = search.remove_needless_result(results, method, count)
    else:
        results = search.search(string, words_with_mistake, case_sensitivity, method, count)
        results = {key: value for key, value in results.items() if not (value is None)}
        print(results)

    return results


def search_with_an_error_in_file(file_path: str, sub_string: Union[str, list[str]],
                                 case_sensitivity=False, method: str = "first",
                                 count: Optional[int] = None, alphabet: Optional[list[str, ...]] = None,
                                 language: Optional[str] = None, n_jobs: int = 1
                                 ) -> Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Функция для поиска подстрок в файле
    :param file_path: путь к файлу
    :param sub_string: строка(и) для поиска
    :param case_sensitivity: чувствительность к регистру
    :param method: означает какое вхождение ищется первое либо последнее
    :param count: кол-во вхождений, которые нужно найти
    :param alphabet: алфавит, который будет использовтся для поиска похожих слов
    :param language: язык алфавита
    :param n_jobs: кол-во потоков
    :return: индексы вхождений
    """
    result = {}
    if method == 'first':
        count_lines = 0
    else:
        count_lines = 1
        with open(file_path, 'r') as f:
            string = f.readline()
            while string != '':
                count_lines += 1
                string = f.readline()
    if method == "first":
        f = open(file_path, 'r')
    else:
        f = FileReadBackwards(file_path)
    while count > 0:
        string = f.readline()
        string.strip()
        if string == '':
            break
        if method == 'first':
            count_lines += 1
        else:
            count_lines -= 1
        temp_key = str(count_lines) + ' строка'
        result[temp_key] = search_with_an_error(string, sub_string, case_sensitivity, method, count,
                                                alphabet, language, n_jobs)
        if isinstance(sub_string, str) and result[temp_key] is not None:
            count -= len(result[temp_key])
        else:
            if result[temp_key] is not None:
                for i in result[temp_key].values():
                    if i is not None:
                        count -= len(i)
    f.close()
    for key, value in result.items():
        result[key] = {key: value for key, value in value.items() if not (value is None)}
    return result
    pass


def main():
    word = 'dev'
    print(search_with_an_error('dev', word, False, 'last', 10,
                               language='en', n_jobs=3))
    # print(search_with_an_error_in_file("input.txt", word, False, method='last', count=10, alphabet=['b', 't', 'c'],
    #                                    language='en', n_jobs=3))
    # pool = ThreadPool(processes=5)
    # threads = []
    # for i in range(5):
    #     threads.append(pool.apply_async(foo, args=(i + 3,)))
    #
    # for i in range(5):
    #     print(threads[i].get())


    # pull = ['some', 'soft', 'same', 'mole', 'soda', 'solder']
    # root = Node(pull[0])
    # for i in range(1, len(pull)):
    #     print(chardet.detect(pull[i].encode('cp1251')))
    #     add_child(root, Node(pull[i]))
    #
    # print(get_similar_words(root, 'sort', 2))
    # print(levenstain('noulw', 'nlw'))
    # print(levenstain('nlw', 'noulw'))


if __name__ == '__main__':
    main()
