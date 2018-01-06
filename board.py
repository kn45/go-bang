# -*- coding=utf8 -*-
import common
import random
from itertools import product


class Board(object):
    def __init__(self, width):
        self.width = width
        self.capacity = self.width ** 2  # how many empty positions
        # 0 for emply, ±1 for each player
        self._layout = [[0] * self.width for x in range(self.width)]
        self.all_stones = set([])

    def __str__(self):
        SIGN = {-1: '●', 0: '┼', +1: 'o'}  # repr sign
        str_repr = ''
        for i, row in enumerate(self._layout):
            str_repr += '%2d ' % (self.width - i)
            str_repr += '─'.join([SIGN[x] for x in row]) + '\n'
        axis_x = [chr(x + ord('A')) for x in range(self.width)]
        str_repr += ' ' * 3 + ' '.join(axis_x)
        return str_repr

    def __hash__(self):
        return hash('|'.join(['|'.join(map(str, x)) for x in self._layout]))

    @property
    def all_availables(self):
        all_moves = set(product(range(self.width), range(self.width)))
        return list(all_moves - self.all_stones)

    def is_pos_in_board(self, pos):
        return True if 0 <= pos[0] < self.width and 0 <= pos[1] < self.width else False

    def is_full(self):
        return True if self.capacity == 0 else False

    def is_empty(self):
        return True if self.capacity == self.width ** 2 else False

    def place(self, pos, player):
        i, j = pos
        self.capacity -= 1
        self.all_stones.add((i, j))
        # DO!
        self._layout[i][j] = player
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
            data_line.append(self._layout[i][j])
        while not (i == ed_i and j == ed_j):  # move one step to end_pos
            i = i + common.sign(ed_i - i)
            j = j + common.sign(ed_j - j)
            if self.is_pos_in_board((i, j)):
                data_line.append(self._layout[i][j])
        sums = [sum(data_line[offset:offset+npos]) for offset in range(npos)]
        return common.max_abs(sums)

    def _add_around(self, moves, pos, radius):
        # update available moves around the position
        i, j = pos
        for row, col in product(range(i-radius, i+radius+1), range(j-radius, j+radius+1)):
            if not self.is_pos_in_board((row, col)):
                continue
            if self._layout[row][col] == 0:
                moves.add((row, col))
        return moves

    @property
    def nearby_availables(self):
        MIN_COUNT = 8
        radius = 1
        if self.is_empty():
            center = int(self.width / 2)
            return [(center, center)]
        moves = set([])
        while True:
            for pos in self.all_stones:
                moves = self._add_around(moves, pos, radius)
            if len(moves) >= self.capacity or len(moves) >= MIN_COUNT:
                return list(moves)
            radius += 1
