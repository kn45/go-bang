# -*- coding=utf8 -*-
import random

class GobangBoard(object):
    def __init__(self):
        self._width = 15
        # 0 for emply, ±1 for each player
        self._layout = [[0] * self._width for x in range(self._width)]
        self._sign = {-1: 'O', 0: '┼', +1: '█'}  # repr ign

    def __str__(self):
        str_repr = ''
        for i, row in enumerate(self._layout):
            str_repr += '%2d ' % (self._width - i)
            str_repr += '─'.join([self._sign[x] for x in row]) + '\n'
        axis_x = [chr(x + ord('A')) for x in range(15)]
        str_repr += ' ' * 3 + ' '.join(axis_x)
        return str_repr

    def _rand_set(self):
        for i in range(self._width):
            for j in range(self._width):
                self._layout[i][j] = int(random.random() * 3) - 1

    def _set_all(self, val):
        if val not in self._sign:
            raise Exception('Not available board value')
        self._layout = [[val] * self._width for x in range(self._width)]

    def set(self, pos, player):
        if player not in self._sign:
            raise Exception('Not available board value')
        row, col = pos
        self.layout[row][col] = player

    def test(self):
        print self
        self._set_all(1)
        print self
        self._set_all(-1)
        print self
        self._rand_set()
        print self


if __name__ == '__main__':
    board = GobangBoard()
    board.test()
