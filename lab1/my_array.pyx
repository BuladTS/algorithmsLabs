# cython: language_level=3
# distutils: language = c

import array

from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

from cpython.float cimport PyFloat_FromDouble, PyFloat_AsDouble


cdef struct arraydescr:
    # код типа, один символ
    char * typecode
    # размер одного элемента массива
    int itemsize
    # функция получения элемента массива по индексу. Обратите внимание,
    # что она возвращает Python тип object. Вот так выглядит сигнатура на Си:
    # PyObject * (*getitem)(struct arrayobject *, Py_ssize_t)
    object (*getitem)(array, size_t)
    # функция записи элемента массива по индексу. Третий аргумент это
    # записываемое значение, оно приходит из Python. Сигнатура на Си:
    # int (*setitem)(struct arrayobject *, Py_ssize_t, PyObject *)
    int (*setitem)(array, size_t, object)

cdef object double_getitem(array a, size_t index):
    # Функция получения значения из массива для типа double.
    # Обратите внимание, что Cython сам преобразует Сишное значение типа
    # double в аналогичны объект PyObject
    return (<double *> a.data)[index]

cdef int double_setitem(array a, size_t index, object obj):
    # Функция записи значения в массив для типа double. Здесь нужно
    # самими извлеч значение из объекта PyObject.
    if not isinstance(obj, int) and not isinstance(obj, float):
        return -1

    # Преобразования Python объекта в Сишный
    cdef double value = PyFloat_AsDouble(obj)

    if index >= 0:
        # Не забываем преобразовывать тип, т.к. a.data имеет тип char
        (<double *> a.data)[index] = value
    return 0

cdef object int_getitem(array a, size_t index):
    return (<int *> a.data)[index]

cdef int int_setitem(array a, size_t index, object obj):

    if not isinstance(obj, int):
        return -1

    cdef int value = obj

    if index >= 0:
        (<int *> a.data)[index] = value
    return 0

# Если нужно работать с несколькими типами используем массив дескрипторов:
# https://github.com/python/cpython/blob/243b6c3b8fd3144450c477d99f01e31e7c3ebc0f/Modules/arraymodule.c#L556
cdef arraydescr[2] descriptors = [
    arraydescr("d", sizeof(double), double_getitem, double_setitem),
    arraydescr("i", sizeof(int), int_getitem, int_setitem),
]

# Зачатки произвольных типов, значения - индексы дескрипторов в массиве
cdef enum TypeCode:
    DOUBLE = 0
    INTEGER = 1

# преобразование строкового кода в число
cdef int char_typecode_to_int(str typecode):
    if typecode == "d":
        return TypeCode.DOUBLE
    elif typecode == "i":
        return TypeCode.INTEGER
    return -1

cdef class array:
    # Класс статического массива.
    # В поле length сохраняем длину массива, а в поле data будем хранить
    # данне. Обратите внимание, что для data используем тип char,
    # занимающий 1 байт. Далее мы будем выделять сразу несколько ячеек
    # этого типа для одного значения другого типа. Например, для
    # хранения одного double используем 8 ячеек для char.
    cdef public size_t length
    cdef char * data
    cdef arraydescr * descr
    cdef char * typecode_array

    # Аналог метода __init__


    def __init__(self, str typecode, object value):
        self.length = len(value)

        typecode_array = typecode
        cdef int mtypecode = char_typecode_to_int(typecode)
        self.descr = &descriptors[mtypecode]

        # Выделяем память для массива
        self.data = <char *> PyMem_Malloc(self.length * self.descr.itemsize)

        for i in range(self.length):
            self.__setitem__(i, value[i])
        if not self.data:
            raise MemoryError()

    # Не забываем освобаждать память. Привязываем это действие к объекту
    # Python. Это позволяет освободить память во время сборки мусора.
    def __dealloc__(self):
        PyMem_Free(self.data)

    # Пользовательски метод для примера. Инициализация массива числами
    # от 0 до length - 1. В Cython можно использовать функции из Python,
    # они преобразуются в Сишные аналоги.
    def initialize(self):
        # Объявление переменно цикла позволяет эффективнее комплировать код.
        cdef int i
        for i in range(self.length):
            self.__setitem__(i, PyFloat_FromDouble(<double> i))

    # Добавим возможность получать элементы по индексу.
    def __getitem__(self, size_t index):
        if 0 <= index < self.length:
            # return (<double *> self.data)[index]
            return self.descr.getitem(self, index)
        raise IndexError()

    # Запись элементов по индексу.
    def __setitem__(self, size_t index, object value):
        if 0 <= index < self.length:
            self.descr.setitem(self, index, value)
        else:
            raise IndexError()

    # Добавим возможность добавлять элементы в конец списка
    def append(self, object value):
        self.length += 1
        self.data = <char *> PyMem_Realloc(self.data ,self.length * self.descr.itemsize)
        self.__setitem__(self.length - 1, value)

    def insert(self, size_t index ,object value):
        self.length += 1
        self.data = <char *> PyMem_Realloc(self.data, self.length * self.descr.itemsize)
        for i in range(self.length - 1, index, - 1):
            self.__setitem__(i, self.__getitem__(i - 1))
        self.__setitem__(index, value)

    def remove(self, object value):
        cdef int index_num
        cdef int i
        for i in range(self.length):
            if self.__getitem__(i) == value:
                index_num = i
        for i in range(index_num, self.length - 1):
            self.__setitem__(i, self.__getitem__(i + 1))
        self.length -= 1
        self.data = <char *> PyMem_Realloc(self.data, self.length * self.descr.itemsize)

    def __len__(self):
        return self.length

    def pop(self, size_t index):
        cdef int i
        num_popped = self.__getitem__(index)
        for i in range(index, self.length - 1):
            self.__setitem__(i, self.__getitem__(i + 1))
        self.length -= 1
        self.data = <char *> PyMem_Realloc(self.data, self.length * self.descr.itemsize)
        return num_popped

    def __reversed__(self):
        cdef int temp_data
        cdef int i
        for i in range(self.length // 2 + self.length % 2):
            temp_data = self.__getitem__(i)
            self.__setitem__(i, self.__getitem__(self.length - i - 1))
            self.__setitem__(self.length - i - 1, temp_data)
        return iter(self)

    def __sizeof__(self):
        return self.length * self.descr.itemsize

    def __eq__(self, object obj):
        if isinstance(obj, array.array) and obj.typecode == self.typecode_array:
            if self.length == len(obj):
                for i in range(self.length):
                    if self.__getitem__(i) != obj[i]:
                        return False
                return True
        return False


