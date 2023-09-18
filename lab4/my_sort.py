from typing import Optional, Callable


def my_sort(array: list, reverse: bool = False,
            key: Optional[Callable] = None, cmp: Optional[Callable] = None) -> list:
    """
    Функция для сортировки массива методом быстрой сортировки
    :param array: массив для сортировки
    :param reverse: сортировать ли в обратную сторону
    :param key: функция для получения значения
    :param cmp: функция вида def func(x,y) -> bool, для сравнения двух значений
    :return: Отсортированный массив
    """
    if key is None and cmp is None:
        quick_sort(array, 0, len(array) - 1)
    elif key is None:
        quick_sort_with_cmp(array, 0, len(array) - 1, cmp)
    elif cmp is None:
        quick_sort_with_key(array, 0, len(array) - 1, key)
    else:
        quick_sort_with_key_and_cmp(array, 0, len(array) - 1, key, cmp)

    if reverse:
        return array[::-1]
    return array


def quick_sort(nums: list, start: int, end: int) -> None:
    """
    Функция сортировки массива алгоритмом быстрой сортировки
    :param nums: массив для сортировки
    :param start: начало отрезка
    :param end: конец отрезка
    :return: None
    """
    if start >= end:
        return
    state = nums[(start + end) // 2]
    i = start
    j = end
    while i <= j:
        while nums[i] < state:
            i += 1
        while nums[j] > state:
            j -= 1
        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1
    quick_sort(nums, start, j)
    quick_sort(nums, i, end)


def quick_sort_with_key(nums: list, start: int, end: int, key: Optional[Callable]) -> None:
    """
    Функция для сортировки с заданным key
    :param nums: массив для сортировки
    :param start: начало отрезка
    :param end: конец отрезка
    :param key: функция вычисляющая значение
    :return: None
    """
    if start >= end:
        return
    state = key(nums[(start + end) // 2])
    i = start
    j = end
    while i <= j:
        while key(nums[i]) < state:
            i += 1
        while key(nums[j]) > state:
            j -= 1
        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1
    quick_sort_with_key(nums, start, j, key)
    quick_sort_with_key(nums, i, end, key)


def quick_sort_with_cmp(nums: list, start: int, end: int, cmp: Optional[Callable]) -> None:
    """
    Функция для быстрой сортировки с заданным компаратором
    :param nums: массив для сортировки
    :param start: начало отрезка
    :param end: конец отрезка
    :param cmp: функция вида def func(x,y) -> bool, возвращает больше ли x y-ка
    :return: None
    """
    if start >= end:
        return
    state = nums[(start + end) // 2]
    i = start
    j = end
    while i <= j:
        while cmp(state, nums[i]):
            i += 1
        while cmp(nums[j], state):
            j -= 1
        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1
    quick_sort_with_cmp(nums, start, j, cmp)
    quick_sort_with_cmp(nums, i, end, cmp)


def quick_sort_with_key_and_cmp(nums: list, start: int, end: int,
                                key: Optional[Callable], cmp: Optional[Callable]) -> None:
    """
    Функция для сортировки с заданными key и cmp
    :param nums: массив для сортировки
    :param start: начало отрезка
    :param end: конец отрезка
    :param key: функция вычисляющая значение
    :param cmp: функция вида def func(x,y) -> bool, возвращает больше ли x y-ка
    :return: None
    """
    if start >= end:
        return
    state = key(nums[(start + end) // 2])
    i = start
    j = end
    while i <= j:
        while cmp(state, key(nums[i])):
            i += 1
        while cmp(key(nums[j]), state):
            j -= 1
        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1
    quick_sort_with_key_and_cmp(nums, start, j, key, cmp)
    quick_sort_with_key_and_cmp(nums, i, end, key, cmp)


def main():
    pass


if __name__ == '__main__':
    main()
