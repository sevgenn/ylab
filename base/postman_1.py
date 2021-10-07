"""Решение задачи "коммивояжера" полным перебором."""


import math
from itertools import permutations
import timeit
import cProfile


def calculate_distance(p1, p2):
    """
    Принимает координаты двух точек на плоскости и возвращает расстояние между ними
    :type p1: (int, int)
    :type p2: (int, int)
    :rtype: float
    """
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def create_distance_dict(points):
    """
    Принимает словарь с координатами точек и возвращает словарь расстояний между ними
    :type points: dict
    :rtype: dict
    """
    dist_dict = {}
    for i in range(len(points)-1):
        for j in range(i+1, len(points)):
            dist_dict[(i, j)] = dist_dict[(j, i)] = calculate_distance(points[i], points[j])
    return dist_dict


def find_min_row(matr, ind=-1):
    """Принимает двумерную матрицу и возвращает строку с наименьшим элементом по индексу ind"""
    res = ''
    min_dist = math.inf
    for i in range(len(matr)):
        if matr[i][ind] < min_dist:
            min_dist = matr[i][ind]
            res = i
    return matr[res]


def format_result_string(lst):
    """
    Принимает список и возвращает стоку в формате для данной задачи
    :type lst: list
    :rtype: str
    """
    result_str = ''
    for i in range(len(lst)-2):
        if i < (len(lst[0]) - 1):
            result_str += f'({lst[0][i]}, {lst[0][i+1]})[{lst[i+1]}] --> '
        else:
            result_str += f'({lst[0][-1]}, {lst[0][0]})[{lst[i+1]}] = {lst[i+2]}'
    return result_str


def main(data):
    # Словарь координат точек:
    points = {x: y for x, y in enumerate(list(data.keys()))}

    # Словарь расстояний между всеми точками, чтобы в дальнейшем не считать расстояние каждый раз заново
    # своего рода мемоизация:)
    dist_dict = create_distance_dict(points)

    # Список всех возможных комбинаций маршрута между точками:
    base = range(len(points))
    comb = permutations(base)
    possible_lst = list(filter(lambda x: x[0] == 0, comb))

    matrix = []
    for el in possible_lst:
        row = [el]
        last_ind = int(el[-1])
        for i in range(len(el)-1):
            dist = dist_dict[(el[i], el[i+1])]
            row.append(dist)
        dist = dist_dict[(0, last_ind)]
        row.append(dist)
        sum_dist = sum(row[1:])
        row.append(sum_dist)
        matrix.append(row)
    result_lst = find_min_row(matrix)
    result = format_result_string(result_lst)
    print(result)


if __name__ == '__main__':
    ###################### Исходные данные: ##########################
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
    # print(timeit.timeit("main(DATA)", setup="from __main__ import main, DATA", number=1))
    # cProfile.run('main(DATA)')
