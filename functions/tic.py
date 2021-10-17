import random
import sys
import time
import argparse


def display_info():
    """Выводит информацию об игре."""
    print('Задача по очереди заполнить поле символами "Х" или "0".\n'
          'Право первого хода определяется случайным образом.\n'
          'Первый игрок использует "Х". Проигрывает тот, кто выстроит в ряд\n(по горизонтали, вертикали или диагонали) '
          '5 одинаковых символов.\nРазмерность поля ограничена от 3х3 до 26х26. Можно выбрать уровень компьютера.\n')


def change_level():
    """Проверяет корректность ввода данных при выборе уровня."""
    while True:
        try:
            level = int(input('Выберите уровень игры (от 0 до 2) > '))
            if level not in range(3):
                continue
        except ValueError:
            print('Введите цифры от 0 до 2')
        else:
            break


def draw_board(board, alpha_list, n):
    """Отрисовывает квадратную матрицу размера nxn с буквенно-цифровым обозначением ячеек."""
    print()
    print(' ' * 5, end='')
    for item in alpha_list:
        print(f' {item}  ', end='')
    print()
    print(' ' * 4 + '-' * 4 * n + '-')
    for i in range(n):
        print(f'{i + 1:>3} |', end='')
        for j in range(n):
            print(f' {board[i][j]} |', end='')
        print()
        print(' ' * 4 + '-' * 4 * n + '-')


def let_me_see(timeout=0.02):
    """Декорирует вывод компьютера."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('Один момент...')
            for i in range(40):
                print('>', end='')
                time.sleep(timeout)
            print()
            res = func(*args, **kwargs)
            return res
        return wrapper
    return decorator


@let_me_see()
def choose_first_step(players):
    """Рандомно выбирает, кто ходит первый и возвращает его индекс в списке.
        :rtype: int"""
    ind = random.choice((0, 1))
    print(f'{players[ind]} ходит первым. Его знак - "X"\n')
    return ind


def change_flags(flags, current_ind):
    """Возвращает список игровых символов в таком виде, чтобы первый игрок всегда ходил с "Х".
        :rtype: list"""
    if flags[current_ind] != 'X':
        flags = flags[::-1]
    return flags


def transform_input(alpha_list, inp_str):
    """Возвращае адрес ячейки, преобразованный в матричные индексы i, j, или False, если адрес вне диапазона.
        :rtype: tuple"""
    s = inp_str.replace(' ', '').upper()
    if s[0] in alpha_list and int(s[1:]) in range(1, 11):
        h_ind = int(s[1:]) - 1
        v_ind = alpha_list.index(s[0])
        return h_ind, v_ind
    else:
        return False


def is_cell_occupied(board, cell):
    """Возвращает булево значение в зависимости от того, пробел в ячейке или другой символ.
        :rtype: bool"""
    return not board[cell[0]][cell[1]].isspace()


def input_user_cell(board, alpha_list):
    """Возвращает корректный адрес ячейки, введенной пользователем.
        :rtype: tuple"""
    while True:
        user_input = input('Введите позицию в формате "e 2"\nили "ex", чтобы выйти > ')
        if user_input == "ex".lower() or user_input == "уч".lower():
            print('Игрок покинул игру.')
            sys.exit()
        cell = transform_input(alpha_list, user_input)
        if not cell:
            print('Некорректный индекс. Будьте внимательны.')
            continue
        if is_cell_occupied(board, cell):
            print('Ячейка уже занята.')
            continue
        break
    return cell


def print_comment_to_step(player, alpha_list, cell):
    """Выводит информацию, кто и какой ход сделал."""
    alpha = alpha_list[cell[1]]
    num = cell[0] + 1
    print(f'{player} пошел на {alpha}{num}')


def make_step(board, cell, flag):
    """Помещает символ игрока в выбранную ячейку и возвращает измененную матрицу.
        :rtype: list"""
    board[cell[0]][cell[1]] = flag
    return board


def get_main_diagonal_of_matrix(board, cell):
    """Возвращает диагональ, проходящую через заданную ячейку параллельно главной диагонали."""
    len_row = len(board)
    i_top_left = cell[0] - cell[1]
    i_top_left = i_top_left if i_top_left >= 0 else 0
    j_top_left = cell[1] - cell[0]
    j_top_left = j_top_left if j_top_left >= 0 else 0
    i_down_right = (len_row - 1) - j_top_left
    length = i_down_right - i_top_left + 1
    return (board[i_top_left + k][j_top_left + k] for k in range(length))


def get_side_diagonal_of_matrix(board, cell):
    """Возвращает диагональ, проходящую через заданную ячейку параллельно побочной диагонали."""
    len_row = len(board)
    i_top_right = cell[0] + cell[1] - (len_row - 1)
    i_top_right = i_top_right if i_top_right >= 0 else 0
    j_top_right = cell[0] + cell[1]
    j_top_right = j_top_right if j_top_right <= (len_row - 1) else (len_row - 1)
    i_down_left = j_top_right
    length = i_down_left - i_top_right + 1
    return (board[i_top_right + k][j_top_right - k] for k in range(length))


def is_lost(board, cell, flag, q):
    """"Проверяет повторение q раз подряд заданного символа в ряду, столбце и диагоналях матрицы,
        проходящих через заданную ячейку, и возвращает результат в виде булева значения.
        :rtype: bool"""
    result = False

    if flag * q in ''.join(board[cell[0]]):
        result = True
    board_t = list(zip(*board))
    if flag * q in ''.join(board_t[cell[1]]):
        result = True
    if flag * q in ''.join(get_main_diagonal_of_matrix(board, cell)):
        result = True
    if flag * q in ''.join(get_side_diagonal_of_matrix(board, cell)):
        result = True
    return result


def test_losing(board, cell, flag, q):
    """Присваивает значение ячейке и проверяет будет ли в этом положении проигрыш."""
    board[cell[0]][cell[1]] = flag
    return is_lost(board, cell, flag, q)


def form_step_list(board, flags, pc_ind, q, level):
    """Возвращает список непроигрышных ячеек, которые не перекрывают слабые позиции противника.
        При отсутствии таковых возвращает список непроигрышных ячеек.
        Если и таких нет, возвращает список свободных ячеек. Уровень формируемого списка
        определяется значением уровня level."""
    empty_list = []
    possible_list = []
    the_best_list = []
    board_test = [row[:] for row in board]
    opponent_ind = (pc_ind + 1) % 2
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                cell = (i, j)
                empty_list.append(cell)
                if (level == 1 or level == 2) and not test_losing(board_test, cell, flags[pc_ind], q):
                    possible_list.append(cell)
                    if level == 2 and not test_losing(board_test, cell, flags[opponent_ind], q):
                        the_best_list.append(cell)
                board_test[i][j] = ' '
    if the_best_list:
        return the_best_list
    if possible_list:
        return possible_list
    return empty_list


@let_me_see()
def choose_random_cell(step_list):
    """Возвращает рандомно выбранную свободную ячейку."""
    return random.choice(step_list)


def is_game_over():
    """Возвращает отказ или согласие игрока на рестарт игры.
     :rtype: bool"""
    restart = input('Сыграем еще раз? (y/n) > ')
    return restart == 'y'


def count_the_points(scores, lost_player):
    """Возвращает итоговое значение очков и распечатывает результат"""
    scores[lost_player] += 1
    print('<<<<< ОБЩИЙ СЧЕТ ПОРАЖЕНИЙ: >>>>>')
    print(f'       PC - {scores["PC"]}  :  human - {scores["HUMAN"]}')
    print('<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>\n')
    return scores


def play(board, players, scores, flags, alpha_list, current_ind, running, n, q, level):
    """Внутренний игровой функционал игры от начала до конца. Возвращает булево значение,
        указывающее на возобновление цикла (рестарт игры) или завершение."""
    step = 0
    game = True
    while game:
        if players[current_ind] == 'PC':
            step_list = form_step_list(board, flags, current_ind, q, level)
            cell = choose_random_cell(step_list)
        else:
            cell = input_user_cell(board, alpha_list)

        print_comment_to_step(players[current_ind], alpha_list, cell)
        make_step(board, cell, flags[current_ind])
        draw_board(board, alpha_list, n)
        print('\n' * 5)

        if is_lost(board, cell, flags[current_ind], q):
            print(f'"{flags[current_ind]}" проиграли.')
            print('Game over\n')
            scores = count_the_points(scores, players[current_ind])
            game = False

        step += 1
        if game and step == n * n:
            print('Ничья')
            game = False

        current_ind = (current_ind + 1) % 2
        if not game:
            running = is_game_over()
            print('\n' * 5)
    return running


def run(n=10, q=5):
    """Функция выполняет инициализацию параметров игры и запускает процесс выполнения."""
    if n > 26:
        n = 26
    if n < 3:
        n = 3
    if n < q:
        q = n
    running = True
    players = ('PC', 'HUMAN')
    scores = {'PC': 0, 'HUMAN': 0}
    flags = ['0', 'X']
    alpha_list = list(chr(i) for i in range(65, 65 + n))

    while running:
        level = 0
        running = False
        board = [[' ' for _ in range(n)] for _ in range(n)]

        display_info()
        draw_board(board, alpha_list, n)
        change_level()
        print('\n<<<<<<<<<< Start Game >>>>>>>>>>>\n')
        if input('Нажмите Enter, чтобы начать, или "ex", чтобы завершить игру > ') == 'ex':
            sys.exit(0)
        print('Давайте кинем жребий, кто начнет...\n')
        current_ind = choose_first_step(players)
        flags = change_flags(flags, current_ind)
        running = play(board, players, scores, flags, alpha_list, current_ind, running, n, q, level)


if __name__ == '__main__':
    run()
