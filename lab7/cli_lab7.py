import click
from controller import controller


@click.command()
@click.option("--input_type", type=click.Choice(["picture", "txt", "none"]), default="none",
              help="Как вводить лабиринт picture: из изображения,"
                   "txt: из txt файла, none: не вводить")
@click.option("--output", type=click.Choice(["picture", "txt", "none"]), default="none",
              help="Как выводить лабиринт picture: в виде изображения,"
                   "txt: в виде txt файла, none: не выводить")
@click.option("--solution", type=click.Choice(["picture", "console"]), default="console",
              help="Сохранить ли решение console: вывод в консоль"
                   "picture: сохранить как изображение")
@click.option("--gif", default=True, help="False: не создавать гифку")
@click.option("--input_size", default=False, help="True: для задания размеров")
def main(input_type, output, solution, gif, input_size):
    maze_path = ""
    width, height = 1202, 702
    tile = 100
    if input_type != "none":
        maze_path = request_file_path("Введите путь к файлу откуда будет взят лабиринт")
        tile = request_int("Введите какой размер у ячейки", 10, 250)
        if maze_path.count(".txt"):
            width = request_int("Введите ширину экрана", 100, 1400)
            height = request_int("Введите высоту экрана", 100, 900)
    elif input_size:
        width = request_int("Введите ширину экрана", 100, 1400)
        height = request_int("Введите высоту экрана", 100, 900)
        tile = request_int("Введите размер одной ячейки", 10, 250)

    output_maze_path = ""
    if output != "none" and input_type == "none":
        output_maze_path = input_name([".jpg", ".txt"], "Введите название файла где сохранить лабиринт")
        output_maze_path = output_maze_path.split(".")[0] + f'_tile_{tile}.' + output_maze_path.split(".")[1]
    solution_path = ""
    if solution != "console":
        solution_path = input_name([".jpg"], "Введите название файла где сохранить решение")
    gif_path = ""
    if gif:
        gif_path = input_name([".gif"], "Введите название гифки")
        gif_path = gif_path.split(".")[0] + f'_tile_{tile}.' + gif_path.split(".")[1]
    controller(width, height, tile, maze_path, solution_path, gif_path, output_maze_path)


def request_int(massage: str, min_num, max_num) -> str:
    return click.prompt(f"{massage}", type=click.IntRange(min=min_num, max=max_num))


def request_file_path(massage: str) -> str:
    """
    Функция для запроса у пользователя пути к файлу:
    :param massage: сообщение, которое выводиться пользователю:
    :return: путь к файлу
    """
    file_path = click.prompt(f"{massage}", type=click.Path(exists=True, file_okay=True, readable=True))
    return file_path


def input_name(type_file: list[str], massage: str) -> str:
    """
    Функция для получения названий файло, определенного типа
    :param type_file: Тип файла
    :param massage: Сообщение для ползователя
    :return: Название файла
    """
    file_name = "."
    while not (file_name[file_name.index("."):] in type_file):
        file_name = click.prompt(f"{massage}")
    return file_name


if __name__ == '__main__':
    main()
