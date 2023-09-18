from random import choice
from typing import Union

import pygame
from pygame.surface import Surface


class Cell:
    """
    Класс для ячейки лабиринта
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Инициализация
        :param x: координаты по x
        :param y: координаты по y
        """
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.solution = False
        self.visited_solution = False

    def draw(self, sc: Surface, tile: int) -> None:
        """
        Функция для отрисовки ячейки
        :param sc: ссылка на окно в котором происходит отрисовка
        :param tile: размеры ячейки
        :return: None
        """
        x, y = self.x * tile, self.y * tile
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, tile, tile))

        if self.solution:
            pygame.draw.rect(sc, pygame.Color('blue'), (self.x * tile + 2, self.y * tile + 2,
                                                        tile - 4, tile - 4), border_radius=50)

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + tile, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + tile, y), (x + tile, y + tile,), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + tile, y + tile), (x, y + tile), 2)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + tile), (x, y), 2)

    # def check_neighbors_walls(self, grid_cells: list, cols: int, rows: int) -> Cell:
    #     neighbors = []
    #     top = self.check_cell(self.x, self.y - 1, grid_cells, cols, rows)
    #     bottom = self.check_cell(self.x, self.y + 1, grid_cells, cols, rows)
    #     right = self.check_cell(self.x + 1, self.y, grid_cells, cols, rows)
    #
    #     if top and self.check_walls_build(self, top):
    #         neighbors.append(top)
    #
    #     if right and self.check_walls_build(self, right):
    #         neighbors.append(right)
    #     return choice(neighbors) if neighbors else bottom

    # def check_neighbors_solution(self, grid_cells, cols, rows):
    #     neighbors = []
    #     top = self.check_cell(self.x, self.y - 1, grid_cells, cols, rows)
    #     bottom = self.check_cell(self.x, self.y + 1, grid_cells, cols, rows)
    #     left = self.check_cell(self.x + 1, self.y, grid_cells, cols, rows)
    #     right = self.check_cell(self.x - 1, self.y, grid_cells, cols, rows)
    #
    #     if top and self.check_walls_solution(self, top) and not top.visited_solution:
    #         neighbors.append(top)
    #     if bottom and self.check_walls_solution(self, bottom) and not bottom.visited_solution:
    #         neighbors.append(bottom)
    #     if right and self.check_walls_solution(self, right) and not right.visited_solution:
    #         neighbors.append(right)
    #     if left and self.check_walls_solution(self, left) and not left.visited_solution:
    #         neighbors.append(left)
    #     return choice(neighbors) if neighbors else False

    @staticmethod
    def check_walls_build(cell_1, cell_2) -> bool:
        """
        Функция для проверки есть ли стена между двумя ячейками
        :param cell_1: Первая ячейка
        :param cell_2: Вторая ячейка
        :return: есть ли стена между двумя ячейками
        """
        dx = cell_1.x - cell_2.x
        if dx == -1:
            if cell_1.walls['right'] != cell_2.walls['left']:
                return False
        elif dx == 1:
            if cell_1.walls['left'] != cell_2.walls['right']:
                return False

        dy = cell_1.y - cell_2.y
        if dy == 1:
            if cell_1.walls['top'] != cell_2.walls['bottom']:
                return False
        elif dy == -1:
            if cell_1.walls['bottom'] != cell_2.walls['top']:
                return False

        return True

    @staticmethod
    def check_walls_solution(cell_1, cell_2) -> bool:
        """
        Функция для проверки есть ли путь между двумя ячейкими
        :param cell_1: первая ячейка
        :param cell_2: вторая ячейка
        :return: есть ли путь между двумя ячейкими
        """
        dx = cell_1.x - cell_2.x
        if dx == -1 and not cell_1.walls['right'] and not cell_2.walls['left']:
            return True
        elif dx == 1 and not cell_1.walls['left'] and not cell_2.walls['right']:
            return True
        dy = cell_1.y - cell_2.y
        if dy == 1 and not cell_1.walls['top'] and not cell_2.walls['bottom']:
            return True
        elif dy == -1 and not cell_1.walls['bottom'] and not cell_2.walls['top']:
            return True

        return False

    @staticmethod
    def check_cell(x: int, y: int, grid_cells: list, cols: int, rows: int):
        """

        :param x:
        :param y:
        :param grid_cells:
        :param cols:
        :param rows:
        :return:
        """
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[x + y * cols]


def check_cell(x: int, y: int, grid_cells: list[Cell], cols: int, rows: int) -> Union[Cell, bool]:
    """
    Функция для получения ячейки из одномерного массива
    :param x: координата по x
    :param y: координата по y
    :param grid_cells: массив ячеек
    :param cols: кол-во колонок
    :param rows: кол-во строк
    :return: False если координаты выходят за границы, или ячейка
    """
    if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
        return False
    return grid_cells[x + y * cols]


def check_neighbors_solution(current_cell: Cell, grid_cells: list[Cell], cols: int, rows: int) -> Union[Cell, bool]:
    """
    Функция для получения непосвященных соседей при решении лабиринта
    :param current_cell: ячейка для которой ищем непосвященных соседей
    :param grid_cells: массив ячеек
    :param cols: кол-во колонок
    :param rows: кол-во строк
    :return: случайного соседа или False если все соседи посещены
    """
    neighbors = []
    top = check_cell(current_cell.x, current_cell.y - 1, grid_cells, cols, rows)
    bottom = check_cell(current_cell.x, current_cell.y + 1, grid_cells, cols, rows)
    left = check_cell(current_cell.x + 1, current_cell.y, grid_cells, cols, rows)
    right = check_cell(current_cell.x - 1, current_cell.y, grid_cells, cols, rows)

    if top and current_cell.check_walls_solution(current_cell, top) and not top.visited_solution:
        neighbors.append(top)
    if bottom and current_cell.check_walls_solution(current_cell, bottom) and not bottom.visited_solution:
        neighbors.append(bottom)
    if right and current_cell.check_walls_solution(current_cell, right) and not right.visited_solution:
        neighbors.append(right)
    if left and current_cell.check_walls_solution(current_cell, left) and not left.visited_solution:
        neighbors.append(left)
    return choice(neighbors) if neighbors else False


def check_neighbors_walls(current_cell: Cell, grid_cells: list[Cell], cols: int, rows: int) -> Cell:
    """
    Функция для получения соседа к которому нужно прокопать путь
    :param current_cell: нынешняя ячейка
    :param grid_cells: массив ячеек
    :param cols: кол-во колонок
    :param rows: кол-во строк
    :return: случайный сосед
    """
    neighbors = []
    top = check_cell(current_cell.x, current_cell.y - 1, grid_cells, cols, rows)
    bottom = check_cell(current_cell.x, current_cell.y + 1, grid_cells, cols, rows)
    right = check_cell(current_cell.x + 1, current_cell.y, grid_cells, cols, rows)

    if top and current_cell.check_walls_build(current_cell, top):
        neighbors.append(top)

    if right and current_cell.check_walls_build(current_cell, right):
        neighbors.append(right)
    return choice(neighbors) if neighbors else bottom


def remove_walls(current_cell: Cell, next_cell: Cell) -> None:
    """
    Функция для удаления стен между ячейками
    :param current_cell: первая ячейка
    :param next_cell: вторая ячейка
    :return: None
    """
    dx = current_cell.x - next_cell.x
    if dx == 1:
        current_cell.walls['left'] = False
        next_cell.walls['right'] = False
    elif dx == -1:
        current_cell.walls['right'] = False
        next_cell.walls['left'] = False
    dy = current_cell.y - next_cell.y
    if dy == 1:
        current_cell.walls['top'] = False
        next_cell.walls['bottom'] = False
    elif dy == -1:
        current_cell.walls['bottom'] = False
        next_cell.walls['top'] = False
