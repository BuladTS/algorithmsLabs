import pathlib
from typing import Union

import numpy
import pygame
from PIL import Image
from pygame.surface import Surface

from Cell import Cell, remove_walls, check_neighbors_walls, check_neighbors_solution

PathType = Union[str, pathlib.Path]


def create_maze(width: int, height: int, tile: int, sc: Surface, image_name: str = "") -> list[Cell]:
    """
    Функция для создания лабиринта
    :param width: ширина лабиринта
    :param height: высота лабиринта
    :param tile: размер ячейки
    :param sc: ссылка на окно
    :param image_name: название файла для сохранения лабиринта
    :return: массив ячеек лабиринта
    """
    cols, rows = width // tile, height // tile
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]

    i_next = 1
    flag_draw = True
    clock = pygame.time.Clock()
    while flag_draw:
        sc.fill(pygame.Color('darkslategray'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        [cell.draw(sc, tile) for cell in grid_cells]
        current_cell.visited = True
        if i_next == len(grid_cells):
            current_cell = grid_cells[-1]
            remove_walls(current_cell, check_neighbors_walls(current_cell, grid_cells, cols, rows))
            next_cell = False
            flag_draw = False
            [cell.draw(sc, tile) for cell in grid_cells]
            if image_name != "":
                pygame.image.save(sc, image_name)
        else:
            next_cell = grid_cells[i_next]
            i_next += 1
        if next_cell:
            next_cell.visited = True
            remove_walls(current_cell, check_neighbors_walls(current_cell, grid_cells, cols, rows))
            current_cell = next_cell
        pygame.display.flip()
        clock.tick(30)

    return grid_cells


def maze_solution(width: int, height: int, tile: int, sc: Surface,
                  grid_cells: list[Cell], image_name: str = "") -> list[tuple]:
    """
    Функция для решения лабиринта
    :param width: ширина лабиринта
    :param height: высота лабиринта
    :param tile: размер одной ячейки
    :param sc: ссылка на окно pygame-а
    :param grid_cells: массив ячеек
    :param image_name: название для изображения
    :return: массив кортежей с координатами, решение
    """
    cols, rows = width // tile, height // tile
    current_cell = grid_cells[0]
    stack = []
    solution = [(0, 0)]
    grid_cells[0].solution = True
    grid_cells[0].visited_solution = True
    flag_solution = True
    clock = pygame.time.Clock()
    while flag_solution:
        sc.fill(pygame.Color('darkslategray'))
        [cell.draw(sc, tile) for cell in grid_cells]
        next_cell = check_neighbors_solution(current_cell, grid_cells, cols, rows)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if next_cell:
            next_cell.visited_solution = True
            next_cell.solution = True
            solution.append((next_cell.x, next_cell.y))
            stack.append(current_cell)
            current_cell = next_cell
        elif stack:
            solution.remove((current_cell.x, current_cell.y))
            current_cell.solution = False
            current_cell = stack.pop()

        if current_cell.x == cols - 1 and current_cell.y == rows - 1:
            [cell.draw(sc, tile) for cell in grid_cells]
            if image_name != "":
                pygame.image.save(sc, image_name)
            flag_solution = False

        pygame.display.flip()
        clock.tick(30)
    return solution


def convert_image_to_matrix(path: PathType, tile: int) -> list[list[int]]:
    """
    Функция для конвертации изображения в матрицу
    :param path: путь к изображению
    :param tile: размеры ячейки
    :return: лабиринт в виде матрицы
    """
    image = Image.open(path)
    width, height = image.size
    cols, rows = width // tile, height // tile

    pixels = numpy.asarray(image)
    array = numpy.eye(3 * rows, 3 * cols)
    array.fill(1)

    incr = tile // 2

    i_index = 0
    j_index = 0
    for i in range(incr, len(pixels), 2 * incr):
        for j in range(incr, len(pixels[i]), 2 * incr):
            i_index_array = 1 + i_index * 3
            j_index_array = 1 + j_index * 3
            array[i_index_array, j_index_array] = 0
            # left
            if sum(pixels[i][j - incr]) < 20:
                array[i_index_array][j_index_array - 1] = 0
            # right
            if sum(pixels[i][j + incr]) < 20:
                array[i_index_array][j_index_array + 1] = 0
            # top
            if sum(pixels[i - incr][j]) < 20:
                array[i_index_array - 1][j_index_array] = 0
            # bottom
            if sum(pixels[i + incr][j]) < 20:
                array[i_index_array + 1][j_index_array] = 0

            j_index += 1
        i_index += 1
        if i_index == rows and j_index == cols:
            break
        j_index = 0
    return array


def convert_matrix_to_cells(matrix: list[list[int]], cols: int, rows: int) -> list[Cell]:
    """
    Функция для конвертации матрицы в массив ячеек
    :param matrix: лабиринт в виде матрицы
    :param cols: кол-во колонок
    :param rows: кол-во строк
    :return: массив ячеек
    """
    grid_cells = []
    for i in range(rows):
        for j in range(cols):
            cell = Cell(j, i)
            i_index = 1 + i * 3
            j_index = 1 + j * 3
            walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            # left
            if matrix[i_index][j_index - 1] == 0:
                walls['left'] = False
            # right
            if matrix[i_index][j_index + 1] == 0:
                walls['right'] = False
            # top
            if matrix[i_index - 1][j_index] == 0:
                walls['top'] = False
            # bottom
            if matrix[i_index + 1][j_index] == 0:
                walls['bottom'] = False
            cell.walls = walls
            cell.visited = True
            grid_cells.append(cell)
    return grid_cells


def convert_cells_to_matrix(grid_cells: list[Cell], cols: int, rows: int) -> list[list[int]]:
    """
    Функция для перевода массива ячеек в матрицу
    :param grid_cells: массив ячеек
    :param cols: кол-во колонок
    :param rows: кол-во строк
    :return: лабиринт в виде матрицы
    """
    matrix = numpy.eye(3 * rows, 3 * cols)
    matrix.fill(1)
    for i in range(rows):
        for j in range(cols):
            current_grid = grid_cells[j + i * cols]
            i_matrix = 1 + i * 3
            j_matrix = 1 + j * 3
            matrix[i_matrix][j_matrix] = 0
            # top
            if not current_grid.walls['top']:
                matrix[i_matrix - 1][j_matrix] = 0
            # bottom
            if not current_grid.walls['bottom']:
                matrix[i_matrix + 1][j_matrix] = 0
            # left
            if not current_grid.walls['left']:
                matrix[i_matrix][j_matrix - 1] = 0
            # right
            if not current_grid.walls['right']:
                matrix[i_matrix][j_matrix + 1] = 0
    # print(numpy.matrix(matrix))
    return matrix


def save_in_txt(filename: PathType, matrix: list[list[int]]) -> None:
    """
    Функция для записи матрицы в текстовый файл
    :param filename: название файла
    :param matrix: лабиринт в виде матрицы
    :return: None
    """
    with open(filename, 'w') as f:
        for i in range(len(matrix)):
            f.write(" ".join(map(str, matrix[i])))
            f.write("\n")


def input_matrix_from_file(filename: PathType) -> list[list[int]]:
    """
    Функция для извлечения лабиринта из текстового формата
    :param filename: название файла
    :return: лабиринт в виде матрицы
    """
    matrix = []
    with open(filename, 'r') as f:
        string = f.readline()
        while string != "":
            matrix.append(list(map(lambda x: int(float(x)), list(string.split(" ")))))
            string = f.readline()
    return matrix


def create_gif(width: int, height: int, tile: int, sc: Surface,
               maze_path: PathType = "", solution_path: PathType = "") -> list[Image]:
    """
    Функция для создания гифки создания и решения лабиринта
    :param width: ширина лабиринта
    :param height: высота лабиринта
    :param tile: размер ячейки лабиринта
    :param sc: ссылка на окно pygame-а
    :param maze_path: Путь к файлу для сохранения лабиринта
    :param solution_path: Путь к файлу для сохранения решения лабиринта
    :return: массив изображений
    """
    cols, rows = width // tile, height // tile
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    i_next = 1

    flag_draw = True
    flag_gif = True
    flag_solution = True

    stack = []
    gif_list = []
    clock = pygame.time.Clock()
    while flag_gif:
        sc.fill(pygame.Color('darkslategray'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        [cell.draw(sc, tile) for cell in grid_cells]
        image = Image.frombytes("RGB", (width, height), pygame.image.tostring(sc, "RGB"))
        gif_list.append(image)

        if flag_draw:
            current_cell.visited = True
            if i_next == len(grid_cells):
                current_cell = grid_cells[-1]
                remove_walls(current_cell, check_neighbors_walls(current_cell, grid_cells, cols, rows))
                next_cell = False
                flag_draw = False
                [cell.draw(sc, tile) for cell in grid_cells]
                image = Image.frombytes("RGB", (width, height), pygame.image.tostring(sc, "RGB"))
                gif_list.append(image)
                if maze_path != "":
                    pygame.image.save(sc, maze_path)
                grid_cells[0].solution = True
                grid_cells[0].visited_solution = True
                current_cell = grid_cells[0]
            else:
                next_cell = grid_cells[i_next]
                i_next += 1
            if next_cell:
                next_cell.visited = True
                remove_walls(current_cell, check_neighbors_walls(current_cell, grid_cells, cols, rows))
                current_cell = next_cell
        elif flag_solution:
            next_cell = check_neighbors_solution(current_cell, grid_cells, cols, rows)
            grid_cells[0].solution = True
            if next_cell:
                next_cell.visited_solution = True
                next_cell.solution = True
                stack.append(current_cell)
                current_cell = next_cell
            elif stack:
                current_cell.solution = False
                current_cell = stack.pop()

            if current_cell.x == cols - 1 and current_cell.y == rows - 1:
                flag_solution = False
                if solution_path != "":
                    pygame.image.save(sc, solution_path)
        else:
            flag_gif = False

        pygame.display.flip()
        clock.tick(30)
    return gif_list
