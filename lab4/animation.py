import random
from typing import Generator

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.container import BarContainer

from gen_quick_sort import gen_quick_sort


def animation(ls: list, generator: Generator[list[int], None, None]) -> None:
    """
    Функция для создания анимации:
    :param ls: массив по которому строиться анимация:
    :param generator: генератор, который возвращает текущее состояние массива:
    :return: None
    """
    length = len(ls)
    fig, ax = plt.subplots()

    bars = ax.bar(range(length), ls, align="edge")
    ax.set_xlim(0, length)
    ax.set_ylim(0, int(1.1 * max(ls)))

    text = ax.text(0.01, 0.95, "", transform=ax.transAxes)
    iterations = [0]

    def animate(arr: list, bar: BarContainer, iteration: list[str]):
        """
        Функция для отрисовки каждого состояния массива
        :param arr: текущее состояние массива
        :param bar: элементы на графике
        :param iteration: номер итерации
        :return: None
        """
        for bar, value in zip(bar, arr):
            bar.set_height(value)
        iteration[0] += 1
        text.set_text(f"Итерация: {iteration[0]}")

    anim = FuncAnimation(
        fig,
        func=animate,
        frames=generator,
        fargs=(bars, iterations),
        interval=40,
        repeat=False,
    )
    plt.show()


def main():
    pass
    # ls = [i for i in range(0, 500, 5)]
    # random.shuffle(ls)
    # animation(ls, gen_quick_sort(ls, 0, len(ls) - 1, True))
    # print(ls)


if __name__ == '__main__':
    main()
