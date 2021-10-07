"""Решение методом Литтла.
Математику давно забыл, поэтому решение вышло корявое"""


import numpy as np
import timeit


def calculate_distance(p1, p2):
    """
    Принимает координаты двух точек на плоскости и возвращает расстояние между ними
    :type p1: (int, int)
    :type p2: (int, int)
    :rtype: float
    """
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def get_min_row(m, el):
    """
    Принимает двумерную матрицу и координаты ячейки. Возвращает минимальное значение
    из всех соседних ячеек в ряду.
    :param m: двумерная матрица
    :param el: список координат точки
    :rtype: float or int
    """
    return min(x for ind, x in enumerate(m[el[0]]) if ind != el[1])


def get_min_column(m, el):
    """
    Принимает двумерную матрицу и координаты ячейки. Возвращает минимальное значение
    из всех соседних ячеек в столбце.
    :param m: двумерная матрица
    :param el: список координат точки
    :rtype: float or int
    """
    return min(x for ind, x in enumerate(m[:, el[1]]) if ind != el[0])


def subtract_min_from_rows(matrix):
    """
    Вычисляет минимальное значение в каждой строке двумерной матрицы
    и вычитает это значение из строки
    :param matrix: двумерная матрица
    :return: None
    """
    for i in range(len(matrix)):
        minimum = min(matrix[i])
        matrix[i] -= minimum


def subtract_min_from_columns(matrix):
    """
    Вычисляет минимальное значение в каждом столбце двумерной матрицы
    и вычитает это значение из столбца
    :param matrix: двумерная матрица
    :return: None
    """
    for i in range(len(matrix)):
        minimum = min(matrix[:, i])
        matrix[:, i] -= minimum


def find_max_weight_element(matrix, lst):
    """
    Принимает матрицу и список нулевых элементов (координаты).
    Возвращает координаты ячейки с максимальным весом
    :param matrix: двумерная матрица
    :param lst: список нулевых элементов
    :rtype: tuple
    """
    max_zero = 0
    max_x = 0
    max_y = 0
    for el in lst:
        min_sum = get_min_row(matrix, el) + get_min_column(matrix, el)
        if min_sum > max_zero:
            max_zero = min_sum
            max_x = el[0]
            max_y = el[1]
    return max_x, max_y


def find_min_distance(matrix, row, col, result=[]):
    """
    Принимает двумерную матрицу и списки точек обхода. Рекурсивно возвращает список элементов,
    соответствующих минимальным дугам обхода.
    :type matrix: numpy.ndarray
    :type row: list
    :type col: list
    :type result: list
    :rtype: list
    """
    if len(matrix) < 2:
        result.append((row[0], col[0]))
        return result
    # Вычитаем из строк минимальные значения:
    subtract_min_from_rows(matrix)
    # Вычитаем из столбцов минимальные значения:
    subtract_min_from_columns(matrix)
    # Получаем индексы нулевых элементов:
    ind_zero = np.argwhere(matrix == 0)
    # Находим нулевую клетку с максимальной оценкой:
    max_x, max_y = find_max_weight_element(matrix, ind_zero)
    # Добавляем путь:
    result.append((row[max_x], col[max_y]))
    # Расставляем запреты:
    matrix[max_y][max_x] = np.inf
    # Удаляем строку и столбец:
    matrix = np.delete(matrix, max_x, axis=0)
    matrix = np.delete(matrix, max_y, axis=1)
    # Удаляем использованные точки:
    del row[max_x]
    del col[max_y]
    return find_min_distance(matrix, row, col)


def sort_list_by_tuples(lst):
    """
    Возвращает список кортежей отсортированный по возрастанию так, что первый элемент последующего
    равен последнем элементу предыдущего
    :type lst: list
    :rtype: list
    """
    if len(lst) == 1:
        return lst
    lst.sort()
    result_lst = [lst[0]]
    lst.remove(lst[0])
    k = 0
    while len(lst) > 0:
        for el in lst:
            if el[0] == result_lst[k][1]:
                result_lst.append(el)
                lst.remove(el)
                k += 1
    return result_lst


def fill_distance_list(matrix, lst):
    """
    Возвращает список элментов (расстояний) матрицы, соответствующих переданному списку обхода
    :param matrix: двумерный массив
    :param lst: список дуг обхода
    :rtype: list
    """
    dist_lst = []
    for item in lst:
        dist = matrix[item[0]][item[1]]
        dist_lst.append(dist)
    return dist_lst


def format_result_string(lst_1, lst_2):
    """
    Принимает список и возвращает стоку в формате для данной задачи
    :type lst_1: list
    :type lst_2: list
    :rtype: str
    """
    result_str = ''
    for i in range(len(lst_1)-1):
        result_str += f'{lst_1[i]}[{lst_2[i]}] --> '
    result_str += f'{lst_1[-1]}[{lst_2[-1]}] = {sum(lst_2)}'
    return result_str


def create_matrix(points, n):
    """
    Принимает словарь точек с координатами и возвращает двумерную матрицу размерностью nxn
    :type points: dict
    :type n: int
    :rtype: numpy.ndarray
    """
    m = np.zeros((n, n))
    m[np.diag_indices_from(m)] = np.inf
    for i in range(n-1):
        for j in range(i+1, n):
            m[i][j] = calculate_distance(points[i], points[j])
    matrix = m + m.transpose()
    return matrix


def main(data):
    # Словарь координат точек:
    points = {x: y for x, y in enumerate(list(data.keys()))}
    # Формирование рабочей матрицы:
    n = len(points)
    matrix = create_matrix(points, n)
    # Неизменяемая копия матрицы:
    start_matrix = matrix.copy()
    # Списки точек маршрута:
    row = list(range(n))
    col = list(range(n))
    # Список минимальных дуг обхода:
    result = find_min_distance(matrix, row, col)
    result_lst = sort_list_by_tuples(result)
    # Список соответсвующмх расстояний:
    dist_lst = fill_distance_list(start_matrix, result_lst)
    result_str = format_result_string(result_lst, dist_lst)
    print(result_str)


if __name__ == '__main__':

    DATA = {
        (0, 2): 'Почтовое отделение',
        (2, 5): 'Ул. Грибоедова',
        (5, 2): 'Ул. Бейкер стрит',
        (6, 6): 'Ул. Большая Садовая',
        (8, 3): 'Вечнозелёная Аллея',
    }

    # start_time = timeit.default_timer()
    main(DATA)
    # print(timeit.default_timer() - start_time)
