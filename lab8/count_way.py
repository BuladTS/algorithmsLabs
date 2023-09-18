import numpy as np
import pandas


def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Функция для подсчета евклидового растояний в 2D
    :param x1: координаты 1-ой точки по X
    :param y1: координаты 1-ой точки по Y
    :param x2: координаты 2-ой точки по X
    :param y2: координаты 2-ой точки по Y
    :return:
    """
    return round(np.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)))


if __name__ == '__main__':
    matrix = np.loadtxt('dist_matrix_true.csv', delimiter='|')
    data = pandas.read_csv("data/data.csv")
    # way = [1, 6, 4, 3, 5, 2, 0]
    way = []
    with open("C_boots/best_way_way.csv", 'r') as f:
        s = f.readline()
        while s != '':
            way.append(int(s))
            s = f.readline()

    sum_d = 0
    for i in range(len(way)):
        sum_d += distance(data["latitude_dd"][way[i]], data["longitude_dd"][way[i]],
                          data["latitude_dd"][way[i - 1]], data["longitude_dd"][way[i - 1]])

    print(sum_d)
