import pathlib
from typing import Union, Optional, Generator
import csv
from file_read_backwards import FileReadBackwards

PathType = Union[str, pathlib.Path]

FILES = [
    "f1.txt",
    "f2.txt",
    "f3.txt",
    "f4.txt",
]


def my_sort(src: list[PathType], output: Optional[PathType] = None, reverse: bool = False,
            key: str = "", type_data: str = "i", nflows: int = 1,
            bsize: Optional[int] = None) -> None:
    """
    Функция для внешней сортировки путем двухпутевого слияния
    :param src: файлы из которых беруться данные
    :param output: файл для вывода ответа
    :param reverse: флаг, указывающий как сортировать (по возрастанию, по убыванию)
    :param key: ключ для csv файлов
    :param type_data: тип данных
    :param nflows: количество потоков
    :param bsize: размер данных для считывания
    :return: None
    """
    flag_output = output is not None and pathlib.Path(output).is_file()
    if flag_output:
        clear_file(FILES)
        init_f1_f2_from_txt(src, type_data, key)
        sort_merge(reverse, type_data, key, output)
    else:
        for file in src:
            clear_file(FILES)
            init_f1_f2_from_txt([file], type_data, key)
            sort_merge(reverse, type_data, key, file)


def read_file_reverse(filepath: PathType) -> Generator[str, None, None]:
    """
    Функция для чтения файла в обратном порядке
    :param filepath: путь к файлу
    :return: генератор строк в обратном порядке
    """
    with FileReadBackwards(filepath) as f:
        while True:
            line = f.readline()
            if line == "":
                yield ":"
                break
            elif line != ":\r\n":
                yield line


def write_answer(filepath, type_data, key: str, reverse: bool = False) -> None:
    """
    Функция для записи ответа в файл
    :param key: ключ для csv файлов
    :param filepath: файл в который проводиться записи
    :param type_data: тип данных
    :param reverse: флаг, указывающий как сортировать
    :return: None
    """
    if filepath.count(".txt") == 1:
        write_answer_txt(filepath, type_data, reverse)
    else:
        write_answer_csv(filepath, type_data, key, reverse)


def write_answer_csv(filepath: PathType, type_data: str, key: str, reverse: bool) -> None:
    """
    Функция для записи ответа в csv файл
    :param filepath: путь к файлу
    :param type_data: тип данных
    :param key: ключ к полю csv
    :param reverse: (по возрастанию или не повозрастанию)
    :return: None
    """

    descr = {"i": int, "s": str, "f": float}[type_data]
    copy_csv(filepath)
    fields = get_fields(filepath)
    with open(filepath, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=',', lineterminator='\n')
        writer.writeheader()

        if reverse:
            answer = read_file_reverse("f1.txt")
            for i in answer:
                if i == ":":
                    break
                writer.writerow(get_item_from_csv(key, descr(normalize_string(i))))
                del_row(key, descr(i))
            answer = read_file_reverse("f3.txt")
            for i in answer:
                if i == ":":
                    break
                writer.writerow(get_item_from_csv(key, descr(normalize_string(i))))
                del_row(key, descr(i))
        else:
            answer = file_reader("f1.txt", type_data)
            for i in answer:
                if i == "" or i == ":":
                    break
                writer.writerow(get_item_from_csv(key, descr(normalize_string(i))))
                del_row(key, descr(i))
            answer = file_reader("f3.txt", type_data)
            for i in answer:
                if i == "" or i == ":":
                    break
                writer.writerow(get_item_from_csv(key, descr(normalize_string(i))))
                del_row(key, descr(i))


def get_fields(filename: str) -> list[str]:
    """
    Функция для получения названий полей
    :param filename: путь к файлу
    :return: названия файлов
    """
    with open(filename, "r") as f:
        reader = csv.reader(f)
        return next(reader)


def get_item_from_csv(field: str, value: Union[str, int, float]) -> dict:
    """
    Функция для получения всей строки в виде словаря, с соответствующим полем
    :param field: поле для поиска
    :param value: значение для поиска
    :return: словарь с полями и значениями
    """
    with open("temp_csv.csv", "r") as f:
        reader = csv.reader(f)
        fields = next(reader)
        for line in reader:
            dc = dict(zip(fields, line))
            if dc[field] == str(value):
                return dc


def del_row(field: str, value: Union[str, int, float]) -> None:
    """
    Функия для удаления строки из вспомогательного файла
    :param field: поле для поиска
    :param value: значее поля
    :return: None
    """
    with open("temp_csv.csv", "r") as f1, open("temp_csv1.csv", "w") as f2:
        reader = csv.DictReader(f1)
        fields = reader.fieldnames
        writer = csv.DictWriter(f2, fieldnames=fields, delimiter=',', lineterminator='\n')
        writer.writeheader()
        fl_del = False
        for line in reader:
            if line[field] == value and fl_del == False:
                fl_del = True
            else:
                writer.writerow(line)
    copy_csv("temp_csv1.csv")


def copy_csv(filename: str) -> None:
    """
    Функция для копирования файла в вспомогательный файл
    :param filename: путь к файлу
    :return: None
    """
    with open(filename, "r") as f1, open("temp_csv.csv", "w") as f2:
        reader = csv.DictReader(f1)
        fields = reader.fieldnames
        writer = csv.DictWriter(f2, fieldnames=fields, delimiter=',', lineterminator='\n')
        writer.writeheader()
        for line in reader:
            writer.writerow(line)


def write_answer_txt(filepath: PathType, type_data: str, reverse: bool) -> None:
    """
    Функция для записи ответа в txt файл
    :param filepath: путь к файлу
    :param type_data: тип данных
    :param reverse: (по возрастанию или не повозрастанию)
    :return: None
    """
    with open(filepath, "w") as f:
        if reverse:
            answer = read_file_reverse("f1.txt")
            for i in answer:
                if i == ":":
                    break
                f.writelines(str(i).strip() + "\n")
            answer = read_file_reverse("f3.txt")
            for i in answer:
                if i == ":":
                    break
                f.writelines(str(i).strip() + "\n")
        else:
            answer = file_reader("f1.txt", type_data)
            for i in answer:
                if i == "" or i == ":":
                    break
                f.writelines(str(i).strip() + "\n")
            answer = file_reader("f3.txt", type_data)
            for i in answer:
                if i == "" or i == ":":
                    break
                f.writelines(str(i).strip() + "\n")


def sort_merge(reverse: bool, type_data: str, key: str, output: Optional[PathType] = None):
    """
    Функция для сортировки уже инициированных данных
    :param key: ключ для csv файлов
    :param reverse: флаг указывающий как сортировать
    :param type_data: тип данных
    :param output: путь к файлу куда записывать данные
    :return: None
    """
    phase_sort = 0

    while True:
        if phase_sort == 0:
            count_write = sorting(["f1.txt", "f2.txt"], ["f3.txt", "f4.txt"], type_data)
            clear_file(["f1.txt", "f2.txt"])
            phase_sort = 1
        else:
            count_write = sorting(["f3.txt", "f4.txt"], ["f1.txt", "f2.txt"], type_data)
            clear_file(["f3.txt", "f4.txt"])
            phase_sort = 0
        if count_write <= 1:
            break
    write_answer(output, type_data, key, reverse)


def sorting(read: list[PathType], write: list[PathType], type_data: str) -> int:
    """
    Функция для сортировки данных слиянием
    :param read: файлы в которых находятся данные
    :param write: файлы для записи промежуточных результатов
    :param type_data: тип данных
    :return: количество записей в файлы
    """
    now_write = 0
    count_write = 0
    files_read = []
    for i in range(len(read)):
        files_read.append(file_reader(read[i], type_data))

    def update_value(generator):
        try:
            value = next(generator)
        except StopIteration:
            value = None
        return value

    first_value = update_value(files_read[0])
    second_value = update_value(files_read[1])
    while True:

        first_value = normalize_string(first_value)
        second_value = normalize_string(second_value)
        if now_write == len(write):
            now_write = 0

        if first_value is None and second_value is None:
            break
        elif first_value is None:
            while second_value != ":":
                write_into_file(write[now_write], second_value)
                second_value = normalize_string(update_value(files_read[1]))
            write_into_file(write[now_write], ":")
            count_write += 1
            break
        elif second_value is None:
            while first_value != ":":
                write_into_file(write[now_write], first_value)
                first_value = normalize_string(update_value(files_read[0]))
            write_into_file(write[now_write], ":")
            count_write += 1
            break

        if first_value == ":" and second_value == ":":
            if now_write == len(write):
                now_write = 0
            write_into_file(write[now_write], second_value)
            count_write += 1
            now_write += 1
            first_value = normalize_string(update_value(files_read[0]))
            second_value = normalize_string(update_value(files_read[1]))

        elif first_value == ":":
            while second_value != ":":
                write_into_file(write[now_write], second_value)
                second_value = normalize_string(update_value(files_read[1]))

        elif second_value == ":":
            while first_value != ":":
                write_into_file(write[now_write], first_value)
                first_value = normalize_string(update_value(files_read[0]))

        elif first_value >= second_value:
            write_into_file(write[now_write], second_value)
            second_value = normalize_string(update_value(files_read[1]))
        else:
            write_into_file(write[now_write], first_value)
            first_value = normalize_string(update_value(files_read[0]))

    return count_write


def normalize_string(value: Union[str, int, float]) -> Union[str, int, float]:
    """
    Функция для удаления специяльных символов из строки
    :param value: значение для удаления спец символов
    :return: значение без специальных символов
    """
    if isinstance(value, str):
        return value.strip()
    return value


def clear_file(files: list[PathType]) -> None:
    """
    Функция для очистки списка файлов
    :param files: файлы для очистки
    :return: None
    """
    for i in files:
        open(i, "w").close()


def write_into_file(filename, string: str) -> None:
    """
    Функция для записи данных в файл
    :param filename: путь к файлу
    :param string: данные для записи
    :return: None
    """
    with open(filename, "a") as f:
        f.writelines(str(string) + "\n")


def read_txt(file: PathType, type_data: str) -> tuple[Generator[str, None, None], int]:
    """
    Функция генератор для чтения файла
    :param file: путь к файлу для чтения
    :param type_data: тип данных
    :return: генератор строк неубывающих чисел, флаг 1 если последовательность кончилась
    """
    string = ""
    last_num = ""
    with open(file, "r") as f:
        while True:
            char = f.read(1)
            if char == "\n":
                string += " "
            else:
                string += char

            if char == "" or string[-1] == " ":

                if last_num != "" and string != "":
                    if check_strs(last_num, string, type_data):
                        yield string.strip(), 1
                    else:
                        yield string.strip(), 0
                else:
                    yield string.strip(), 0
                last_num = string.strip()
                string = ""

                if char == "":
                    break
    return


def check_strs(s1: str, s2: str, type_data: str) -> bool:
    """
    Функция для сравнения двух значений
    :param s1: первое значение
    :param s2: второе значение
    :param type_data: тип данных в которой нажно сравнить
    :return: больше ли первый элемент второго
    """
    if type_data == "i":
        if int(s1) >= int(s2):
            return True
    elif type_data == "f":
        if float(s1) >= float(s2):
            return True
    elif type_data == "s":
        if s1 >= s2:
            return True
    return False


def init_f1_f2_from_txt(filenames: list[PathType], type_data: str, key: str) -> None:
    """
    Функция для начальной инициализации
    :param key:
    :param filenames: пути к файлам из которых нужно достать данные
    :param type_data: тип данных
    :return: None
    """

    def swap_now_file(tracker_file):
        if tracker_file == "f1.txt":
            tracker_file = "f2.txt"
        else:
            tracker_file = "f1.txt"
        return tracker_file

    now_file = "f2.txt"
    for filename in filenames:
        if filename.count(".txt") == 1:
            gen = read_txt(filename, type_data)
        else:
            gen = read_csv(filename, type_data, key)
        now_file = swap_now_file(now_file)
        for i in gen:

            string, flag = i
            if flag == 1:
                write_into_file(now_file, ":")
                now_file = swap_now_file(now_file)

            if now_file == "f1.txt" and string != "":
                write_into_file(now_file, string)
            elif string != "":
                write_into_file(now_file, string)

        write_into_file(now_file, ":")


def read_csv(file: PathType, type_data: str, key: str) -> tuple[Generator[str, None, None], int]:
    """
    Функция для чтения csv файла
    :param file: путь к файлу
    :param type_data: тип данных
    :param key: поле в csv файле
    :return: генератор значений и флаг окончания возрастающей серии
    """
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        last_num = ""
        for i in reader:
            line = i[key]
            if last_num != "":
                if check_strs(last_num, line, type_data):
                    yield line.strip(), 1
                else:
                    yield line.strip(), 0
            else:
                yield line.strip(), 0
            last_num = line


def file_reader(filename: PathType, type_data: str) -> Generator[list[int], None, None]:
    """
    Функция для чтения данных из временных накопителе, и представления из в виде массива
    :param filename: путь к файлу
    :param type_data: тип данных
    :return: генератор списков неубывающих данных
    """
    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if line == "":
                break
            if line != ":\n":
                if line.strip() == "":
                    yield ""
                elif type_data == "i":
                    yield int(line)
                elif type_data == "f":
                    yield float(line)
                else:
                    yield line
            else:
                yield ":"
            if line == "":
                break
    return


def main():
    pass


if __name__ == '__main__':
    main()
