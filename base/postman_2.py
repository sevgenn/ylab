"""То же решение задачи "коммивояжера" полным перебором, как и в первом модуле.
Отличие в том, что в первом варианте программа падала при количестве точек более 11
из-за нехватки памяти, потому что сохранялись все промежуточные данные.
В этом варианте высвобождается память. Вместо перебора по списку возможных маршрутов перебор по итератору.
Текущие расчетные данные тоже не сохраняются, а перезаписываются.
Но очень медленно - 13 точек расчитывались 1 час."""


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


def find_min_combination(dist_dict, n):
    """
    Принимает словарь расстояний между точками (включая маршрут туда и обратно:
    {(0,2): 123, (2,0): 123}) и количество всех точек.
    Возвращает список из кортежа с комбинацией самого короткого маршрута, соответствующих расстояний
    между точками и суммой маршрута.
    :type dist_dict: dict
    :type n: int
    :rtype: list
    """
    base = range(n)
    matrix = []
    MIN_DIST = 1e6
    for el in filter(lambda x: x[0] == 0, permutations(base)):
        row = [el]
        last_ind = int(el[-1])
        for i in range(len(el) - 1):
            dist = dist_dict[(el[i], el[i + 1])]
            row.append(dist)
        dist = dist_dict[(0, last_ind)]
        row.append(dist)
        sum_dist = sum(row[1:])
        if sum_dist < MIN_DIST:
            row.append(sum_dist)
            MIN_DIST = sum_dist
            matrix = row[:]
    return matrix


def main(data):
    # Словарь координат точек:
    points = {x: y for x, y in enumerate(list(data.keys()))}

    # Словарь расстояний между всеми точками, чтобы в дальнейшем не считать расстояние каждый раз заново
    dist_dict = create_distance_dict(points)

    matrix = find_min_combination(dist_dict, n=len(points))

    result = format_result_string(matrix)
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

    main(DATA)
    # print(timeit.timeit("main(DATA)", setup="from __main__ import main, DATA", number=1))
    # cProfile.run('main(DATA)')
