"""
Модуль классов геометрических фигур.

Импортируется функционал стандартной библиотеки math.
Для формирования графических изображений импортируются  библиотеки numpy и matplotlib.
"""
from math import pi, sqrt, tan, sin
import numpy as np
import matplotlib.pyplot as plt


class Param:
    """Класс-дескриптор для присвоения и вызова значений свойств классов."""

    def __set_name__(self, owner, name):
        """Позволяет получить имя атрибута, связанного с дескриптором."""
        self.__name = name

    def __get__(self, instance, owner):
        """Возвращает значение, хранящееся в экземпляре instance."""
        return instance.__dict__[self.__name]

    def __set__(self, instance, value):
        """
        Сохраняет значение value в экземпляре класса instance.

        В случае некорректного значения заменяет его на ноль,
        чтобы не вызывать ошибку, а в дальнейшем обработать ноль как ошибку.
        """
        if self.__check_params(value):
            instance.__dict__[self.__name] = float(value)
        else:
            instance.__dict__[self.__name] = 0.0

    def __check_params(self, value):
        """Проверяет, чтобы присваиваемые значения были числами."""
        return type(value) in (int, float)


class Shape(Param):
    """Родительский класс для всех классов модуля. Определяет общую структуру и функционал."""

    title = 'Shape'

    def __init__(self):
        """Инициализирует экземпляр класса при его создании."""
        pass

    def check_possibility(self):
        """Проверяет возможность существования экземпляра класса в зависимости от его параметров."""
        pass

    def calc_apothem(self):
        """Возвращает значение апофемы для фигур, которым присущ этот параметр."""
        pass

    def calc_perimeter(self):
        """Возвращает значение периметра для фигур, которым присущ этот параметр."""
        pass

    def calc_area(self):
        """Возвращает значение площади поверхности фигуры."""
        pass

    def calc_volume(self):
        """Возвращает значение объема для фигур, которым присущ этот параметр."""
        pass

    def draw(self):
        """Формирует графическое изображение фигуры."""
        pass


class Square(Shape):
    """Класс-наследник класса Shape. Определяет функционал квадрата."""

    title = 'Square'
    names = ('Length',)
    length = Param()

    def __init__(self, length=0):
        """
        Наследуется от родителя. Дополняется одним параметром.

        :param length: длина стороны квадрата
        :type length: float
        :return: None
        """
        super().__init__()
        self.length = length

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования квадрата.
        :return: bool
        """
        return self.length != 0

    def calc_perimeter(self):
        """
        Переопределяет метод родителя. Возвращает значение периметра квадрата.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.length * 4
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя. Возвращает значение площади квадрата.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.length * self.length
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение квадрата."""
        fig = plt.figure(figsize=(4, 4), facecolor='#eee')
        ax = fig.add_subplot()
        fig.suptitle('Square')
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        pr = plt.Polygon(([0, 0], [0, 4], [4, 4], [4, 0]), facecolor='skyblue')
        ax.add_patch(pr)
        plt.axis('off')
        plt.show()


class Cube(Square):
    """Класс-наследник класса Square. Определяет функционал куба. При инициализации так же получает один параметр."""

    title = 'Cube'

    def calc_perimeter(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления периметра куба.

        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.length * 12
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя в части вычисления пложади куба.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.length * self.length * 6
            return round(result, 2)
        return 'ERROR'

    def calc_volume(self):
        """
        Переопределяет метод родителя Shape. Возвращает значение объема куба.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.length ** 3
            return round(result, 2)
        return 'ERROR'


class Rectangle(Square):
    """
    Класс-наследник класса Square. Определяет функционал прямоугольника.

    При инициализации получает один дополнительный параметр.
    """

    title = 'Rectangle'
    names = ('Length', 'Width')
    width = Param()

    def __init__(self, length=0, width=0):
        """
        Наследуется от родителя. Дополняется одним параметром.

        :param width: ширина прямоугольника
        :type width: float
        :return: None
        """
        super().__init__(length)
        self.width = width

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования прямоугольника.
        :return: bool
        """
        return self.length != 0 and self.width != 0

    def calc_perimeter(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления периметра прямоугольника.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = (self.length + self.width) * 2
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления площади прямоугольника.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.length * self.width
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение прямоугольника."""
        fig = plt.figure(figsize=(4, 4), facecolor='#eee')
        ax = fig.add_subplot()
        fig.suptitle('Rectangle')
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        pr = plt.Polygon(([0, 0], [0, 2.5], [4, 2.5], [4, 0]), facecolor='skyblue')
        ax.add_patch(pr)
        plt.axis('off')
        plt.show()


class Box(Rectangle):
    """
    Класс-наследник класса Rectangle. Определяет функционал параллелепипеда.
    При инициализации получает один дополнительный параметр.
    """

    title = 'Box'
    names = ('Length', 'Width', 'Height')
    height = Param()

    def __init__(self, length=0, width=0, height=0):
        """
        Наследуется от родителя. Дополняется одним параметром.

        :param height: высота параллелепипеда
        :type height: float
        :return: None
        """
        super().__init__(length, width)
        self.height = height

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования параллелепипеда.
        :return: bool
        """
        return self.length != 0 and self.width != 0 and self.height != 0

    def calc_perimeter(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления периметра параллелепипеда.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = (self.length + self.width) * 2 + self.height * 4
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления площади параллелепипеда.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = (self.length * self.width + self.height * self.length + self.height * self.width) * 2
            return round(result, 2)
        return 'ERROR'

    def calc_volume(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления объема параллелепипеда.

        Возвращает ERROR, если введен некорректный параметр длины.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.length * self.width * self.height
            return round(result, 2)
        return 'ERROR'


class Circle(Shape):
    """Класс-наследник класса Shape. Определяет функционал круга."""

    title = 'Circle'
    names = ('Radius',)
    radius = Param()

    def __init__(self, radius=0):
        """
        Наследуется от родителя. Дополняется одним параметром.

        :param radius: радиус круга
        :type radius: float
        :return: None
        """
        super().__init__()
        self.radius = radius

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования круга.
        :return: bool
        """
        return self.radius != 0

    def calc_perimeter(self):
        """
        Переопределяет метод родителя. Возвращает значение длины окружности.

        Возвращает ERROR, если введен некорректный параметр радиуса.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = 2 * pi * self.radius
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя. Возвращает значение площади круга.

        Возвращает ERROR, если введен некорректный параметр радиуса.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = pi * self.radius ** 2
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение круга."""
        fig = plt.figure(figsize=(4, 4), facecolor='#eee')
        ax = fig.add_subplot()
        fig.suptitle('Circle')
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        cr = plt.Circle((0, 0), 2, facecolor='skyblue', fill=True)
        ax.add_patch(cr)
        plt.axis('off')
        plt.show()


class Ball(Circle):
    """Класс-наследник класса Circle. При инициализации получает те же параметры. Определяет функционал шара."""

    title = 'Ball'

    def calc_perimeter(self):
        """Переопределяет метод родителя, т.к. шар не имеет периметра."""
        pass

    def calc_area(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления площади шара.

        Возвращает ERROR, если введен некорректный параметр радиуса.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = 4 * pi * self.radius ** 2
            return round(result, 2)
        return 'ERROR'

    def calc_volume(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления объема шара.

        Возвращает ERROR, если введен некорректный параметр радиуса.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = pi * self.radius ** 3 * 4 / 3
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение шара."""
        fig = plt.figure(figsize=(4, 4), facecolor='#eee')
        ax_3d = fig.add_subplot(projection='3d')
        r = 2
        p = np.arange(0, 2 * np.pi, 0.1)
        t = np.arange(0, 2 * np.pi, 0.1)
        phi, theta = np.meshgrid(p, t)
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        ax_3d.plot_surface(x, y, z, facecolor='skyblue')
        plt.axis('off')
        plt.show()


class Cylinder(Circle):
    """Класс-наследник класса Circle. Определяет функционал цилиндра."""

    title = 'Cylinder'
    names = ('Radius', 'Height')
    height = Param()

    def __init__(self, radius=0, height=0):
        """
        Наследуется от родителя. Дополняется при инициализации одним параметром.

        :param height: высота цилиндра
        :type height: float
        :return: None
        """
        super().__init__(radius)
        self.height = height

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования цилиндра.
        :return: bool
        """
        return self.radius != 0 and self.height != 0

    def calc_perimeter(self):
        """Переопределяет метод родителя, т.к. цилиндр не имеет периметра."""
        pass

    def calc_area(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления площади цилиндра.

        Возвращает ERROR, если введен некорректный параметр радиуса или высоты.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = 2 * pi * self.radius * (self.height + self.radius)
            return round(result, 2)
        return 'ERROR'

    def calc_volume(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления объема цилиндра.

        Возвращает ERROR, если введен некорректный параметр радиуса или высоты.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.height * pi * self.radius ** 2
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение цилиндра."""
        fig = plt.figure(figsize=(4, 4))
        ax_3d = fig.add_subplot(projection='3d')
        fig.suptitle('Cylinder')
        u = np.linspace(0, 2 * np.pi, 50)
        h = np.linspace(0, 1, 25)
        x = np.outer(np.sin(u), np.ones(len(h)))
        y = np.outer(np.cos(u), np.ones(len(h)))
        z = np.outer(np.ones(len(u)), h)
        ax_3d.plot_surface(x, y, z, color='skyblue')
        plt.axis('off')
        plt.show()


class Cone(Cylinder):
    """Класс-наследник класса Cylinder. Имеет те же параметры. Определяет функционал конуса."""

    title = 'Cone'

    def calc_area(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления площади конуса.

        Возвращает ERROR, если введен некорректный параметр радиуса или высоты.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = pi * self.radius * (self.radius + sqrt(self.radius ** 2 + self.height ** 2))
            return round(result, 2)
        return 'ERROR'

    def calc_volume(self):
        """
        Переопределяет метод родителя в соответствии с правилом вычисления объема конуса.

        Возвращает ERROR, если введен некорректный параметр радиуса или высоты.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = (self.height * pi * self.radius ** 2) / 3
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение конуса."""
        pass


class Pyramid(Shape):
    """Класс-наследник базового класса Shape. Определяет функционал правильной пирамиды."""

    title = 'Pyramid'
    names = ('Quantity', 'Length', 'Height')
    quantity = Param()
    length = Param()
    height = Param()

    def __init__(self, quantity=0, length=0, height=0):
        """
        Наследуется от родителя. Дополняется при инициализации тремя параметрами.

        :param quantity: количество сторон основания
        :param length: длина стороны основания
        :param height: высота пирамиды
        :type quantity: float
        :type length: float
        :type height: float
        :return: None
        """
        super().__init__()
        self.quantity = quantity
        self.length = length
        self.height = height

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования пирамиды.
        :return: bool
        """
        return self.quantity != 0 and self.length != 0 and self.height != 0

    def calc_apothem(self):
        """
        Переопределяет метод родителя. Возвращает значение апофемы.

        Возвращает ERROR, если введен некорректный параметр.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = sqrt(self.height ** 2 + (self.length / (2 * tan(pi / self.quantity))) ** 2)
            return round(result, 2)
        return 'ERROR'

    def calc_perimeter(self):
        """
        Переопределяет метод родителя. Возвращает значение общего периметра пирамиды.

        Возвращает ERROR, если введен некорректный параметр.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.quantity * sqrt(
                self.height ** 2 + (self.length / (2 * sin(pi / self.quantity))) ** 2) + self.length * self.quantity
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя. Возвращает значение общей площади пирамиды.

        Возвращает ERROR, если введен некорректный параметр.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = (self.quantity * self.length / 2) * \
                     (self.length / (2 * tan(pi / self.quantity)) +
                      sqrt(self.height ** 2 + (self.length / (2 * tan(pi / self.quantity))) ** 2))
            return round(result, 2)
        return 'ERROR'

    def calc_volume(self):
        """
        Переопределяет метод родителя. Возвращает значение объема пирамиды.

        Возвращает ERROR, если введен некорректный параметр.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.height * self.quantity * self.length ** 2 / (12 * tan(pi / self.quantity))
            return round(result, 2)
        return 'ERROR'


class Trapeze(Shape):
    """Класс-наследник базового класса Shape. Определяет функционал трапеции."""

    title = 'Trapeze'
    names = ('Lower Base', 'Upper Base', 'Side 1', 'Side 2')
    lower_base = Param()
    upper_base = Param()
    side1 = Param()
    side2 = Param()

    def __init__(self, lower_base=0, upper_base=0, side1=0, side2=0):
        """
        Наследуется от родителя. Дополняется при инициализации четырьмя параметрами.

        :param lower_base: длина нижнего основания
        :param upper_base: длина верхнего основания
        :param side1: длина боковой стороны
        :param side2: длина другой боковой стороны
        :type lower_base: float
        :type upper_base: float
        :type side1: float
        :type side2: float
        :return: None
        """
        super().__init__()
        self.lower_base = lower_base
        self.upper_base = upper_base
        self.side1 = side1
        self.side2 = side2

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования трапеции.
        :return: bool
        """
        check_list = [self.lower_base, self.upper_base, self.side1, self.side2]
        max_side = max(check_list)
        check_list.remove(max_side)
        return (max_side < sum(check_list)) and (self.lower_base != self.upper_base) and \
               self.lower_base != 0 and self.upper_base != 0 and self.side1 != 0 and self.side2 != 0

    def calc_perimeter(self):
        """
        Переопределяет метод родителя. Возвращает значение периметра трапеции.

        Возвращает ERROR, когда значение равно нулю (присвоен некорректный параметр длины) или когда трапеция не
        существует.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.lower_base + self.upper_base + self.side1 + self.side2
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя. Возвращает значение площади трапеции через ее полупериметр.

        Возвращает ERROR, когда значение равно нулю (присвоен некорректный параметр длины) или когда трапеция не
        существует.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            p = self.calc_perimeter() / 2
            result = (self.lower_base + self.upper_base) / abs(self.lower_base - self.upper_base) * sqrt(
                (p - self.lower_base) * (p - self.upper_base) * (p - self.lower_base - self.side1) * (
                        p - self.lower_base - self.side2))
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение трапеции."""
        fig = plt.figure(figsize=(4, 4), facecolor='#eee')
        ax = fig.add_subplot()
        fig.suptitle('Trapeze')
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        pr = plt.Polygon(([0, 0], [1, 3], [3, 3], [4, 0]), facecolor='skyblue')
        ax.add_patch(pr)
        plt.axis('off')
        plt.show()


class Rhombus(Shape):
    """Класс-наследник базового класса Shape. Определяет функционал ромба."""

    title = 'Rhombus'
    names = ('Diagonal 1', 'Diagonal 1')
    diagonal1 = Param()
    diagonal2 = Param()

    def __init__(self, diagonal1=0, diagonal2=0):
        """
        Наследуется от родителя. Дополняется при инициализации двумя параметрами.

        :param diagonal1: длина одной диагонали
        :param diagonal2: длина другой диагонали
        :type diagonal1: float
        :type diagonal2: float
        :return: None
        """
        super().__init__()
        self.diagonal1 = diagonal1
        self.diagonal2 = diagonal2

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования ромба.
        :return: bool
        """
        return self.diagonal1 != 0 and self.diagonal2 != 0

    def calc_perimeter(self):
        """
        Переопределяет метод родителя. Возвращает значение периметра ромба.

        Возвращает ERROR, когда значение равно нулю (присвоен некорректный параметр) или когда ромб не
        существует.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = sqrt((self.diagonal1 / 2) ** 2 + (self.diagonal2 / 2) ** 2) * 4
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя. Возвращает значение площади ромба.

        Возвращает ERROR, когда значение равно нулю (присвоен некорректный параметр) или когда ромб не
        существует.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.diagonal1 * self.diagonal2 / 2
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение ромба."""
        fig = plt.figure(figsize=(4, 4), facecolor='#eee')
        ax = fig.add_subplot()
        fig.suptitle('Rhombus')
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        pr = plt.Polygon(([0, 1], [2, 2], [4, 1], [2, 0]), facecolor='skyblue')
        ax.add_patch(pr)
        plt.axis('off')
        plt.show()


class Triangle(Shape):
    """Класс-наследник базового класса Shape. Определяет функционал треугольника."""

    title = 'Triangle'
    names = ('Side a', 'Side b', 'Side c')
    side1 = Param()
    side2 = Param()
    side3 = Param()

    def __init__(self, side1=0, side2=0, side3=0):
        """
        Наследуется от родителя. Дополняется при инициализации тремя параметрами.

        :param side1: длина одной стороны
        :param side2: длина второй стороны
        :param side3: длина третьей стороны
        :type side1: float
        :type side2: float
        :type side3: float
        :return: None
        """
        super().__init__()
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def check_possibility(self):
        """
        Переопределяет родительский метод.

        Проверяет, что исходные данные удовлетворяют факту существования трапеции.
        :return: bool
        """
        check_list = [self.side1, self.side2, self.side3]
        max_side = max(check_list)
        check_list.remove(max_side)
        return max_side < sum(check_list) and self.side1 != 0 and self.side2 != 0 and self.side3 != 0

    def calc_perimeter(self):
        """
        Переопределяет метод родителя. Возвращает значение периметра треугольника.

        Возвращает ERROR, когда значение равно нулю (присвоен некорректный параметр длины) или когда треугольник не
        существует.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            result = self.side1 + self.side2 + self.side3
            return round(result, 2)
        return 'ERROR'

    def calc_area(self):
        """
        Переопределяет метод родителя. Возвращает значение площади треугольника через полупериметр.

        Возвращает ERROR, когда значение равно нулю (присвоен некорректный параметр длины) или когда треугольник не
        существует.
        :returns: Union[float, str]
        """
        if self.check_possibility():
            p = self.calc_perimeter() / 2
            result = sqrt(p * (p - self.side1) * (p - self.side2) * (p - self.side3))
            return round(result, 2)
        return 'ERROR'

    def draw(self):
        """Переопределяет метод родителя и отрисовывает в отдельном окне изображение треугольника."""
        fig = plt.figure(figsize=(4, 4), facecolor='#eee')
        ax = fig.add_subplot()
        fig.suptitle('Triangle')
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 4)
        pr = plt.Polygon(([0, 0], [1.5, 3], [4, 0]), facecolor='skyblue')
        ax.add_patch(pr)
        plt.axis('off')
        plt.show()
