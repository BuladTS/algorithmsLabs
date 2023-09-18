from typing import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
from PIL import Image, ImageDraw


MAX_DEPTH = 10
DETAIL_THRESHOLD = 13


def average_color(image: Image) -> tuple[int, int, int]:
    """
    Функция для находения среднего цвета
    :param image: изображение для вычисления
    :return: кортеж цвета в формате RGB
    """
    image_as_array = np.asarray(image)
    avg_color_rows = np.average(image_as_array, axis=0)
    avg_color = np.average(avg_color_rows, axis=0)

    return int(avg_color[0]), int(avg_color[1]), int(avg_color[2])


def weighted_average(hist):
    """
    Функция для вычисления взвешенного значения массива
    :param hist: массив чисел
    :return: взвешенная дисперсия
    """
    total = sum(hist)
    error = 0

    if total > 0:
        value = sum(i * x for i, x in enumerate(hist)) / total
        error = sum(x * (value - i) ** 2 for i, x in enumerate(hist)) / total
        error = error ** 0.5

    return error


def get_detail(hist):
    """
    Функция для преобразования трех канального цвета в одноканальный
    :param hist: Гистограмма изображения
    :return: Одноканальный цвет
    """
    red_detail = weighted_average(hist[:256])
    green_detail = weighted_average(hist[256:512])
    blue_detail = weighted_average(hist[512:768])

    detail_intensity = red_detail * 0.2989 + green_detail * 0.5870 + blue_detail * 0.1140

    return detail_intensity


def int_and_round(x: float) -> int:
    """
    Функция для окугления и приведения к целому виду числа
    :param x: чсло для преобразования
    :return:
    """
    return int(round(x))


class Quadrant:
    """
    Класс квадранта
    """
    def __init__(self, image: Image, bbox: tuple, depth: int) -> None:
        """
        Функция для инициализации квадранта
        :param image: Изображение
        :param bbox: Область изображения
        :param depth: Глубина на которой находиться квадрант
        """
        self.depth = depth
        self.bbox = bbox
        self.image = image.crop(bbox)
        self.color = average_color(self.image)
        self.children = []
        self.leaf = False
        hist = self.image.histogram()
        self.detail = get_detail(hist)

    def split_four(self, image: Image) -> None:
        """
        Функция для разделения квадранта на четыре части
        :param image: Изображение
        :return: None
        """
        left, top, right, bottom = self.bbox

        mid_x = left + (right - left) / 2
        mid_y = top + (bottom - top) / 2

        if not self.check_children(left, top, right, bottom, mid_x, mid_y):
            self.leaf = True
            return

        self.insert_upper_left(Quadrant(image, (left, top, mid_x, mid_y), self.depth + 1))
        self.insert_bottom_right(Quadrant(image, (mid_x, top, right, mid_y), self.depth + 1))
        self.insert_bottom_left(Quadrant(image, (left, mid_y, mid_x, bottom), self.depth + 1))
        self.insert_bottom_right(Quadrant(image, (mid_x, mid_y, right, bottom), self.depth + 1))

    def insert_upper_left(self, quadrant) -> None:
        """
        Функция для вставки квадранта слева сверху
        :param quadrant: Квадрант для вставки
        :return: None
        """
        self.children.insert(0, quadrant)

    def insert_upper_right(self, quadrant) -> None:
        """
        Функция для вставки квадранта справа сверху
        :param quadrant: Квадрант для вставки
        :return: None
        """
        self.children.insert(1, quadrant)

    def insert_bottom_left(self, quadrant) -> None:
        """
        Функция для вставки квадранта слева внизу
        :param quadrant:  Квадрант для вставки
        :return: None
        """
        self.children.insert(2, quadrant)

    def insert_bottom_right(self, quadrant) -> None:
        """
        Функция для вставки квадранта справа внизу
        :param quadrant:  Квадрант для вставки
        :return: None
        """
        self.children.insert(3, quadrant)

    @staticmethod
    def check_children(left: int, top: int, right: int, bottom: int, mid_x: int, mid_y: int) -> bool:
        """
        Метод для проверки размеров областей, чтобы при crop
        размеры обрезанного участка не были меньше одного пикселя
        :param left: Левая граница
        :param top: Верхняя граница
        :param right: Правая граница
        :param bottom: Нижняя граница
        :param mid_x: Середина по координате Х
        :param mid_y: Середина по координате Y
        :return: False если нельзя разделить, иначе True
        """

        descriptor = int_and_round
        if descriptor(left - mid_x) * descriptor(top - mid_y) <= 1:
            return False

        if descriptor(mid_x - right) * descriptor(top - mid_y) <= 1:
            return False

        if descriptor(left - mid_x) * descriptor(mid_y - bottom) <= 1:
            return False

        if descriptor(mid_x - right) * descriptor(mid_y - bottom) <= 1:
            return False

        # images = [image.crop((left, top, mid_x, mid_y)), image.crop((mid_x, top, right, mid_y)),
        #           image.crop((left, mid_y, mid_x, bottom)), image.crop((mid_x, mid_y, right, bottom))]
        # for i in range(4):
        #     wight, height = images[i].size
        #     if wight * height < 1:
        #         return False
        return True


class QuadTree:
    """
    Класс квадродерева
    """
    def __init__(self, image: Image) -> None:
        """
        Функция инициализации
        :param image: Изображение
        """
        self.root = None
        self.image = image
        self.width, self.height = image.size
        self.max_depth = 0

    def start(self) -> None:
        """
        Метод для начала построения дерева
        :return: None
        """
        self.root = Quadrant(self.image, self.image.getbbox(), 0)
        self.build(self.root)

    def build(self, root: Quadrant) -> None:
        """
        Метод строительства дерева
        :param root: Квадрант для разделения
        :return: None
        """
        if root.depth >= MAX_DEPTH or root.detail <= DETAIL_THRESHOLD:
            if root.depth > self.max_depth:
                self.max_depth = root.depth
            root.leaf = True
            return
        root.split_four(self.image)

        with ThreadPoolExecutor() as executor:
            pool = []
            for children in root.children:
                pool.append(executor.submit(self.build, children))

            for future in as_completed(pool):
                future.result()

    def get_quadrants(self, depth: int) -> list[Quadrant, ...]:
        """
        Метод для получения квадрантов определенной глубине
        :param depth: Глубина
        :return: Список квадрантов
        """

        if depth > self.max_depth:
            depth = self.max_depth
            print("Глубина была слишком большой, из-за этого была взята максимальная глубина дерева")

        quadrants = []

        self.recursive_search(self.root, depth, quadrants.append)

        return quadrants

    def recursive_search(self, quadrant: Quadrant, max_depth: int, append: Callable) -> None:
        """
        Метод для рекурсивного поиска квадрантов определенной глубины
        :param quadrant: Квадрант для проверки на глубину
        :param max_depth: Глубина
        :param append: Метод для добавления в изначальный список
        :return: None
        """

        if quadrant.leaf is True or quadrant.depth == max_depth:
            append(quadrant)
        elif quadrant.children is not None:
            for child in quadrant.children:
                self.recursive_search(child, max_depth, append)

    def create_image(self, depth: int, show_lines=False) -> Image:
        """
        Функция для построения картинки определенной глубины
        :param depth: Глубина
        :param show_lines: Флаг отвечающий за показ линий
        :return: Изображение
        """
        image = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.width, self.height), (0, 0, 0))

        leaf_quadrants = self.get_quadrants(depth)

        for quadrant in leaf_quadrants:
            if show_lines:
                draw.rectangle(quadrant.bbox, quadrant.color, outline=(0, 0, 0))
            else:
                draw.rectangle(quadrant.bbox, quadrant.color)

        return image

    def create_gif(self, file_name: str, duration: int = 1000, loop: int = 0, show_lines: bool = False) -> None:
        """
        Функция для создания гифка
        :param file_name: Название файла гифки
        :param duration: Длительность (в миллисекундах) на один кадр
        :param loop: Количества повторений гифки
        :param show_lines: Флаг отвечающий за показ линий
        :return: None
        """
        gif = []
        end_product_image = self.create_image(self.max_depth, show_lines=show_lines)

        for i in range(self.max_depth):
            image = self.create_image(i, show_lines=show_lines)
            gif.append(image)

        for _ in range(4):
            gif.append(end_product_image)

        gif[0].save(
            file_name,
            save_all=True,
            append_images=gif[1:],
            duration=duration, loop=loop)


def main():

    image_path = "sea.jpeg"

    # load image
    image = Image.open(image_path)
    print(image)
    image = image.resize((image.size[0], image.size[1]))
    print(image)

    tree = QuadTree(image)
    tree.start()
    # # image = tree.create_image(6, show_lines=True)
    # # image.save("6_lines_b.jpg")
    # tree.create_gif("gif_3.gif", show_lines=True)
    # tree.create_gif("gif_4.gif", show_lines=False)
    # # image_array = np.asarray(image)
    # # print(image_array)
    # # print(len(image_array))
    # # print(len(image_array[0]))
    # # avg_color_per_row = np.average(image_array, axis=0)
    # # print(avg_color_per_row)
    # #
    # # print(np.average(avg_color_per_row, axis=0))
    # #
    # # print(np.round(np.average(avg_color_per_row, axis=0)))
    # # print(image.getbbox())


if __name__ == '__main__':
    main()
