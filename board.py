# -*- coding=utf8 -*-
import common
import random
from itertools import product


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

    @property
    def all_availables(self):
        all_moves = set(product(range(self.__width), range(self.__width)))
        return list(all_moves - self.__all_stones)

    def is_pos_in_board(self, pos):
        return False if max(pos) >= self.__width or min(pos) < 0 else True

    def is_full(self):
        return True if self.__capacity == 0 else False

    def is_empty(self):
        return True if self.__capacity == self.__width ** 2 else False

    def place(self, pos, player):
        if pos in self.__all_stones:  # already placed
            return False
        self.__set__layout(pos, player)
        return True

    def undo_place(self, pos):
        if pos not in self.__all_stones:  # not placed
            return False
        self.__set__layout(pos, 0)
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


if __name__ == '__main__':
    board = Board(15)
    print board.max_abs_subsum((-1, 2), (2, 2), 3)
    print board[1][2]
    board2 = Board(3)
    print board2
