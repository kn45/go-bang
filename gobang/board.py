# -*- coding=utf8 -*-

import common
import random
from itertools import product


class GobangBoard(object):
    def __init__(self):
        self.__width = 15
        # 0 for emply, ±1 for each player
        self.__layout = [[0] * self.__width for x in range(self.__width)]
        self.__sign = {-1: 'O', 0: '┼', +1: '█'}  # repr sign
        self.__capacity = self.__width ** 2  # how many empty point

    def __str__(self):
        str_repr = ''
        for i, row in enumerate(self.__layout):
            str_repr += '%2d ' % (self.__width - i)
            str_repr += '─'.join([self.__sign[x] for x in row]) + '\n'
        axis_x = [chr(x + ord('A')) for x in range(15)]
        str_repr += ' ' * 3 + ' '.join(axis_x)
        return str_repr

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.__layout[key]
        if isinstance(key, tuple):
            return self.__layout[key[0]][key[1]]

    def __set__layout(self, pos, val):
        # all layout set operation should use this func
        if not self.is_pos_in_board(pos):
            raise Exception('Position out of board range')
        if val not in self.__sign:
            raise Exception('Not available board value')
        i, j = pos
        self.__layout[i][j] = val
        if val != 0:
            self.__capacity -= 1

    @property
    def capacity(self):
        return self.__capacity

    def is_pos_in_board(self, pos):
        row, col = pos
        if max(row, col) >= self.__width or min(row, col) < 0:
            return False
        else:
            return True

    def place(self, pos, player):
        self.__set__layout(pos, player)

    def max_abs_subsum(self, st_pos, ed_pos):
        # return the 5-subsum in the line-shaped region with max abs
        # return +5 or -5 means winning on this line
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
        sums = [sum(data_line[offset:offset+5]) for offset in range(5)]
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
        print self.max_abs_subsum((-3, 5), (5, 5))


if __name__ == '__main__':
    board = GobangBoard()
    board.test()
    print board[3][4]
    print dir(board)
