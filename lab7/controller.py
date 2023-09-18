import numpy
import pygame
import maze


def controller(width=1202, height=702, tile=100, maze_path="",
               solution_path="", gif_path="", output_maze_path="") -> None:
    """
    Функция для контролирования работы программы
    :param width: ширина лабиринта
    :param height: высота лабиринта
    :param tile: размер ячейки лабиринта
    :param maze_path: путь к лабиринту для считывания
    :param solution_path: путь куда сохранить решение лабиринта
    :param gif_path: путь куда сохранить gif изображение
    :param output_maze_path: путь куда вывести лабиринт
    :return: None
    """
    res = width, height
    cols, rows = width // tile, height // tile
    pygame.init()
    sc = pygame.display.set_mode(res)
    grid_cells = []
    if gif_path != "":
        gif_list = maze.create_gif(width, height, tile, sc, output_maze_path, solution_path)
        gif_list[0].save(
            gif_path,
            save_all=True,
            append_images=gif_list[1:],
            optimize=True,
            duration=200,
            loop=0
        )
    else:
        if maze_path != "":
            if maze_path.count(".txt") == 1:
                matrix = maze.input_matrix_from_file(maze_path)
                grid_cells = maze.convert_matrix_to_cells(matrix, cols, rows)
            elif maze_path.count(".jpg") == 1:
                matrix = maze.convert_image_to_matrix(maze_path, tile)
                grid_cells = maze.convert_matrix_to_cells(matrix, cols, rows)
        else:
            if output_maze_path.count(".jpg") == 1:
                grid_cells = maze.create_maze(width, height, tile, sc, output_maze_path)
            elif output_maze_path.count(".txt") == 1:
                grid_cells = maze.create_maze(width, height, tile, sc)
                matrix = maze.convert_cells_to_matrix(grid_cells, cols, rows)
                maze.save_in_txt(output_maze_path, matrix)

        solution = maze.maze_solution(width, height, tile, sc, grid_cells, solution_path)
        if solution_path == "":
            print(solution)

    # sc.copy()
    # gif_list = maze.create_gif(width, height, tile, sc)
    # gif_list[0].save(
    #     'gif_gen_lab.gif',
    #     save_all=True,
    #     append_images=gif_list[1:],
    #     optimize=True,
    #     duration=200,
    #     loop=0
    # )
    # grid_cells = maze.create_maze(width, height, tile, sc)
    # solution = maze.maze_solution(width, height, tile, sc, grid_cells)
    # matrix = maze.convert_image_to_matrix("lab_7b.jpg", tile)
    # matrix = maze.input_matrix_fromfile("maze.txt")
    # print(numpy.matrix(matrix))
    # grid_cells = maze.convert_matrix_to_cells(matrix, cols, rows)
    # solution = maze.maze_solution(width, height, tile, sc, grid_cells)
    # print(solution)
    # matrix = maze.convert_cells_to_matrix(grid_cells, cols, rows)
    # maze.save_in_txt("maze.txt", matrix)
    # clock = pygame.time.Clock()
    # while True:
    #
    #     sc.fill(pygame.Color('darkslategray'))
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             exit()
    #     # [cell.draw(sc, tile) for cell in grid_cells]
    #
    #     pygame.display.flip()
    #     clock.tick(30)


if __name__ == '__main__':
    pass
    # res = 802, 502
    # cols, rows = 802 // 100, 502 // 100
    # pygame.init()
    # sc = pygame.display.set_mode(res)
    # grid_cells = []
    # matrix = maze.input_matrix_from_file("lab.txt")
    # print(numpy.matrix(matrix))
    # grid_cells = maze.convert_matrix_to_cells(matrix, cols, rows)
    # maze.maze_solution(802, 502, 100, sc, grid_cells)
    # controller(maze_path="lab.txt", tile=50, solution_path="maze1.jpg")
