"""
Цыдыпов.Б.Б КИ21-17/1б

Дерево пифагора
"""

import turtle
from random import randint


def generate_plant(iterations: int) -> None:
    """
    Функция управляющая построением дерева
    :return: None
    """
    axiom = "0"
    angle = 30
    line_length = 11

    axiom = create_axiom(axiom, iterations)
    draw_plant(axiom, angle, line_length)


def create_axiom(prime_axiom: str, iterations: int, ) -> str:
    """
    Функция создает аксиому по которой будет построено дерево
    :param prime_axiom: начальная аксиома
    :param iterations: кол-во итераций
    :return: полуенная аксиома из n-го кол-ва итераций
    """
    translate = {
        "1": "21",
        "0": "1[0]0"
    }
    axiom_temp = ""
    i = 0
    while i < iterations:
        for item in prime_axiom:
            if item in translate:
                axiom_temp += translate[item]
            else:
                axiom_temp += item
        prime_axiom = axiom_temp
        axiom_temp = ""
        i += 1
    return prime_axiom


def draw_plant(axiom: str, angle: int, line_length: int) -> None:
    """
    Функция для построения дерева Пифагора
    :param axiom: аксиома по которой строиться дерево
    :param angle: базовое значение угла
    :param line_length: базовая длина сучка
    :return: None
    """

    screen = turtle.Screen()
    screen.tracer(0)
    screen.colormode(255)
    screen.bgcolor("black")

    tree = turtle.Turtle()
    tree.hideturtle()
    tree.penup()
    tree.setposition(0, -350)
    tree.left(90)
    tree.pendown()
    tree.pensize(2)

    stac = []

    for item in axiom:
        if item == "2":
            tree.pencolor(generate_color())
            tree.forward(line_length)
        elif item == "1":
            tree.pencolor(generate_color())
            tree.forward(line_length)
        elif item == "0":
            tree.pencolor(generate_color())
            tree.forward(line_length)
        elif item == "[":
            stac.append(tree.xcor())
            stac.append(tree.ycor())
            stac.append(tree.heading())
            tree.left(angle - round(randint(-25, 25) / 100 * angle))
        elif item == "]":
            tree.penup()
            tree.setheading(stac.pop())
            tree.sety(stac.pop())
            tree.setx(stac.pop())
            tree.pendown()
            tree.right(angle - round(randint(-25, 25) / 100 * angle))

    screen.update()
    screen.mainloop()


def generate_color() -> tuple:
    """
    Функция для генерации случайного цвета в формате RGB
    :return: кортеж значений цвета
    """
    return randint(0, 255), randint(0, 255), randint(0, 255)


def main() -> None:
    """
    Функция управляющая всей программой
    :return: None
    """
    iterations = input("Введите количество итераций (рекомендовано 10): ")
    if iterations.isdigit() and iterations != "0":
        generate_plant(int(iterations))
    else:
        print("Некорректный ввод")


if __name__ == '__main__':
    main()
