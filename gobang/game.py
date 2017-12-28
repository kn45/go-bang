# -*- coding=utf8 -*-

import common
import random
import sys
from itertools import product
from callback import AvlMoves


class Board(object):
    def __init__(self, width):
        self.__width = width
        # 0 for emply, ±1 for each player
        self.__layout = [[0] * self.__width for x in range(self.__width)]
        self.__sign = {-1: '●', 0: '┼', +1: 'o'}  # repr sign
        self.__capacity = self.__width ** 2  # how many empty positions
        self.__all_stones = set([])

    def __str__(self):
        str_repr = ''
        for i, row in enumerate(self.__layout):
            str_repr += '%2d ' % (self.__width - i)
            str_repr += '─'.join([self.__sign[x] for x in row]) + '\n'
        axis_x = [chr(x + ord('A')) for x in range(self.__width)]
        str_repr += ' ' * 3 + ' '.join(axis_x)
        return str_repr

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__layout[key]
        if isinstance(key, tuple):
            return self.__layout[key[0]][key[1]]

    def __set__layout(self, pos, val):
        # all layout set operation should use this func
        # including placing and REMOVING
        if not self.is_pos_in_board(pos):
            raise Exception('Position out of board range')
        if val not in self.__sign:
            raise ValueError('Not available board value')
        i, j = pos
        # update capacity. 0 -> ±1 or ±1 -> 0 would cause capacity change
        self.__capacity += abs(self.__layout[i][j]) - abs(val)
        # update all_ponits
        if val == 0:
            self.__all_stones.discard((i, j))
        else:
            self.__all_stones.add((i, j))
        # DO!
        self.__layout[i][j] = val

    @property
    def capacity(self):
        return self.__capacity

    @property
    def width(self):
        return self.__width

    @property
    def all_stones(self):
        return list(self.__all_stones)

    def is_pos_in_board(self, pos):
        row, col = pos
        return False if max(row, col) >= self.__width or min(row, col) < 0 else True

    def is_full(self):
        return True if self.__capacity == 0 else False

    def place(self, pos, player):
        if pos in self.__all_stones:  # already placed
            return False
        self.__set__layout(pos, player)
        return True

    def max_abs_subsum(self, st_pos, ed_pos, npos):
        # return the npos-subsum in the line-shaped region with max abs
        # return +npos or -npos means winning on this line
        # st_pos and ed_pos must be in a line (diag line is ok)
        i, j = st_pos
        ed_i, ed_j = ed_pos
        delta_x = ed_i - i
        delta_y = ed_j - j
        if delta_x != 0 and delta_y != 0 and abs(delta_x) != abs(delta_y):  # not in a line
            raise ValueError('start_pos and end_pos not in a line')
        data_line = []
        if self.is_pos_in_board(st_pos):
            data_line.append(self.__layout[i][j])
        while not (i == ed_i and j == ed_j):  # move one step to end_pos
            i = i + common.sign(ed_i - i)
            j = j + common.sign(ed_j - j)
            if self.is_pos_in_board((i, j)):
                data_line.append(self.__layout[i][j])
        sums = [sum(data_line[offset:offset+npos]) for offset in range(npos)]
        return common.max_abs(sums)

    def set_all(self, val=None):
        # set all the board to a certain value. if value is None, random all
        # mainly for test use
        for i, j in product(range(self.__width), range(self.__width)):
            if val is not None:
                self.__set__layout((i, j), val)
            else:
                self.__set__layout((i, j), int(random.random()*3)-1)

    def test(self):
        print self
        self.set_all(val=1)
        print self
        self.set_all(val=-1)
        print self
        self.set_all()
        print self
        print self.max_abs_subsum((-1, 2), (2, 2), 3)
        print self[1][2]
        print self[(1, 2)]


class GameStatus(object):
    WIN1 = -1
    DRAW = 0
    WIN2 = +1
    UNDERGOING = 2


class Game(object):
    def __init__(self, board_width, win_count):
        self.__WIN_COUNT = win_count  # how many continous stones to win
        self.__board = Board(board_width)
        self.__player = -1  # -1 or +1
        self.__game_status = GameStatus.UNDERGOING
        self.__callbacks = {'AvlMoves': AvlMoves(self.__board)}

    def __check_win_status(self, pos):
        # evaluate winner. ±1 - each winner; 0 - other case
        c_i, c_j = pos
        # check row direction
        mass_row = self.__board.max_abs_subsum((c_i, c_j-4), (c_i, c_j+4), self.__WIN_COUNT)
        mass_col = self.__board.max_abs_subsum((c_i-4, c_j), (c_i+4, c_j), self.__WIN_COUNT)
        mass_diag = self.__board.max_abs_subsum((c_i-4, c_j-4), (c_i+4, c_j+4), self.__WIN_COUNT)
        max_abs_val = common.max_abs([mass_row, mass_col, mass_diag])
        return common.sign(max_abs_val) if abs(max_abs_val) == self.__WIN_COUNT else 0

    @property
    def game_status(self):
        return self.__game_status

    @property
    def board(self):
        return self.__board

    @property
    def player(self):
        return self.__player

    def __update_game_status(self, pos):
        win_status = self.__check_win_status(pos)
        self.__game_status = win_status if win_status != 0 else \
            (GameStatus.DRAW if self.__board.is_full() else GameStatus.UNDERGOING)

    def add_callback(self, **kwargs):
        for callback_name in kwargs:
            if callback_name not in self.__callbacks:
                self.__callbacks[callback_name] = kwargs[callback_name]

    def move(self, pos):
        succ = self.__board.place(pos, self.__player)
        if not succ:
            return False
        # update game status
        self.__update_game_status(pos)
        # switch player
        self.__player *= -1
        # update callbacks
        callback_args = {'last_pos': pos}
        for callback_name in self.__callbacks:
            self.__callbacks[callback_name].update(**callback_args)
        return True

    def get_available_moves(self):
        return self.__callbacks['AvlMoves'].get_all()


class GoBang(Game):
    def __init__(self):
        super(GoBang, self).__init__(board_width=15, win_count=5)


class TicTacToe(Game):
    def __init__(self):
        super(TicTacToe, self).__init__(board_width=3, win_count=3)


if __name__ == '__main__':
    board = Board(15)
    board.test()
    board2 = Board(3)
    board2.test()

    avl_moves = AvlMoves(Board(15))
    print avl_moves.get_all()
    avl_moves._update_dbg(pos=(3, 3), min_radius=1, min_count=0)
    print avl_moves.get_all()

    game = GoBang()
    print game.get_available_moves()
    game.move((7, 7))
    print game.board
    print game.get_available_moves()
    game.move((8, 9))
    print game.board
