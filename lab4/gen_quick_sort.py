from typing import Generator


def gen_quick_sort(nums: list[int], start: int, end: int, reverse: bool) -> Generator[list[int], None, None]:
    """
    Функция генератор для построения анимации
    :param nums: массив для сортировки
    :param start: начало отрезка
    :param end: конец отрезка
    :param reverse: флаг, указывающий как сортировать по убыванию или возрастанию
    :return: Генератор с шагами сортировки
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
            if reverse:
                yield nums[::-1]
            else:
                yield nums
    yield from gen_quick_sort(nums, start, j, reverse)
    yield from gen_quick_sort(nums, i, end, reverse)
