# -*- coding=utf8 -*-
import common
import random
from itertools import product


class Board(object):
    def __init__(self, width):
        self.width = width
        self.capacity = self.width ** 2  # how many empty positions
        # 0 for emply, ±1 for each player
        self.layout = [[0] * self.width for x in range(self.width)]
        self.all_stones = set([])
        self._nearby_availables = set([])

    def __str__(self):
        SIGN = {-1: '●', 0: '┼', +1: 'o'}  # repr sign
        str_repr = ''
        for i, row in enumerate(self.layout):
            str_repr += '%2d ' % (self.width - i)
            str_repr += '─'.join([SIGN[x] for x in row]) + '\n'
        axis_x = [chr(x + ord('A')) for x in range(self.width)]
        str_repr += ' ' * 3 + ' '.join(axis_x)
        return str_repr

    def __hash__(self):
        return hash('|'.join(['|'.join(map(str, x)) for x in self.layout]))

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
        self.layout[i][j] = player
        self.capacity -= 1
        self.all_stones.add((i, j))
        self._update_nearby(pos)

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
            data_line.append(self.layout[i][j])
        while not (i == ed_i and j == ed_j):  # move one step to end_pos
            i = i + common.sign(ed_i - i)
            j = j + common.sign(ed_j - j)
            if self.is_pos_in_board((i, j)):
                data_line.append(self.layout[i][j])
        sums = [sum(data_line[offset:offset+npos]) for offset in range(npos)]
        return common.max_abs(sums)

    @property
    def nearby_availables(self):
        if len(self._nearby_availables) == 0:
            return [(int(self.width/2), int(self.width/2))]
        return list(self._nearby_availables)

    def _update_nearby(self, pos):
        radius = 1
        self._nearby_availables.discard(pos)
        i, j = pos
        for row, col in product(range(i-radius, i+radius+1), range(j-radius, j+radius+1)):
            if self.is_pos_in_board((row, col)) and self.layout[row][col] == 0:
                self._nearby_availables.add((row, col))
