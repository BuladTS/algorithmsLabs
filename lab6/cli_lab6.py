import click
from PIL import Image

from lab6 import QuadTree


@click.command()
@click.option('--create_gif', prompt="Введите True, для создания гифки", default=False, help="Флаг для создания гифки")
@click.option('--depth', prompt="Введите глубину изображения", type=click.IntRange(min=1), help="Глубина изображения")
@click.option('--show_lines', prompt="Введите True для показа разделяющих линий",
              default=False, help="Показывать ли линии")
def main(create_gif: bool, depth: int, show_lines: bool):
    """
    Основния функция для работы программы
    :param create_gif: Флаг для создания гифки
    :param depth: Глубина изображения
    :param show_lines: Показывать ли линии
    :return: None
    """
    image_path = click.prompt("Введите путь к изображению", type=click.Path(exists=True, file_okay=True, readable=True))
    name_image = input_name(".jpg", "Введите название для изображения")

    image = Image.open(image_path)
    image = image.resize((image.size[0], image.size[1]))
    tree = QuadTree(image)
    tree.start()
    image = tree.create_image(depth, show_lines)
    image.save(name_image)

    if create_gif:
        gif_name = input_name(".gif", "Введите название гифки")
        tree.create_gif(gif_name, show_lines=show_lines)


def input_name(type_file: str, massage: str) -> str:
    """
    Функция для получения названий файло, определенного типа
    :param type_file: Тип файла
    :param massage: Сообщение для ползователя
    :return: Название файла
    """
    file_name = ""
    while file_name.count(type_file) != 1:
        file_name = click.prompt(f"{massage}")
    return file_name


if __name__ == '__main__':
    main()
