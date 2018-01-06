# -*- coding=utf8 -*-

import board
import common
import random
import sys
from itertools import product


class GameStatus(object):
    WIN1 = -1
    DRAW = 0
    WIN2 = +1
    UNDERGOING = 2


class Game(object):
    def __init__(self, board_width, win_count):
        self.__WIN_COUNT = win_count  # how many continous stones to win
        self.player = -1  # -1 or +1
        self.stone_history = []
        self.board = board.Board(board_width)

    def __check_win_status(self, pos):
        # evaluate winner. ±1 - each winner; 0 - other case
        c_i, c_j = pos
        # check row direction
        mass_row = self.board.max_abs_subsum(
            (c_i, c_j-self.__WIN_COUNT+1), (c_i, c_j+self.__WIN_COUNT-1), self.__WIN_COUNT)
        if abs(mass_row) == self.__WIN_COUNT:
            return common.sign(mass_row)

        mass_col = self.board.max_abs_subsum(
            (c_i-self.__WIN_COUNT+1, c_j), (c_i+self.__WIN_COUNT-1, c_j), self.__WIN_COUNT)
        if abs(mass_col) == self.__WIN_COUNT:
            return common.sign(mass_col)

        mass_diag1 = self.board.max_abs_subsum(
            (c_i-self.__WIN_COUNT+1, c_j-self.__WIN_COUNT+1),
            (c_i+self.__WIN_COUNT-1, c_j+self.__WIN_COUNT-1), self.__WIN_COUNT)
        if abs(mass_diag1) == self.__WIN_COUNT:
            return common.sign(mass_diag1)

        mass_diag2 = self.board.max_abs_subsum(
            (c_i+self.__WIN_COUNT-1, c_j-self.__WIN_COUNT+1),
            (c_i-self.__WIN_COUNT+1, c_j+self.__WIN_COUNT-1), self.__WIN_COUNT)
        if abs(mass_diag2) == self.__WIN_COUNT:
            return common.sign(mass_diag2)

        return 0

    @property
    def game_status(self):
        if len(self.stone_history) == 0:
            return GameStatus.UNDERGOING
        else:
            return self._get_game_status(self.stone_history[-1])

    def _get_game_status(self, pos):
        win_status = self.__check_win_status(pos)
        return win_status if win_status != 0 else \
            (GameStatus.DRAW if self.board.is_full() else GameStatus.UNDERGOING)

    def move(self, pos):
        succ = self.board.place(pos, self.player)
        if not succ:
            return False
        self.stone_history.append(pos)
        # switch player
        self.player *= -1
        return True


class GoBang(Game):
    def __init__(self):
        super(GoBang, self).__init__(board_width=15, win_count=5)


class TicTacToe(Game):
    def __init__(self):
        super(TicTacToe, self).__init__(board_width=3, win_count=3)
