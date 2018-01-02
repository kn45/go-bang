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
        self.__board = board.Board(board_width)
        self.__player = -1  # -1 or +1
        self.__game_status = GameStatus.UNDERGOING

    def __check_win_status(self, pos):
        # evaluate winner. ±1 - each winner; 0 - other case
        c_i, c_j = pos
        # check row direction
        mass_row = self.__board.max_abs_subsum(
            (c_i, c_j-self.__WIN_COUNT+1),
            (c_i, c_j+self.__WIN_COUNT-1),
            self.__WIN_COUNT)
        mass_col = self.__board.max_abs_subsum(
            (c_i-self.__WIN_COUNT+1, c_j),
            (c_i+self.__WIN_COUNT-1, c_j),
            self.__WIN_COUNT)
        mass_diag1 = self.__board.max_abs_subsum(
            (c_i-self.__WIN_COUNT+1, c_j-self.__WIN_COUNT+1),
            (c_i+self.__WIN_COUNT-1, c_j+self.__WIN_COUNT-1),
            self.__WIN_COUNT)
        mass_diag2 = self.__board.max_abs_subsum(
            (c_i+self.__WIN_COUNT-1, c_j-self.__WIN_COUNT+1),
            (c_i-self.__WIN_COUNT+1, c_j+self.__WIN_COUNT-1),
            self.__WIN_COUNT)
        max_abs_val = common.max_abs([mass_row, mass_col, mass_diag1, mass_diag2])
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

    def move(self, pos):
        succ = self.__board.place(pos, self.__player)
        if not succ:
            return False
        # update game status
        self.__update_game_status(pos)
        # switch player
        self.__player *= -1
        return True


class GoBang(Game):
    def __init__(self):
        super(GoBang, self).__init__(board_width=15, win_count=5)


class TicTacToe(Game):
    def __init__(self):
        super(TicTacToe, self).__init__(board_width=3, win_count=3)


if __name__ == '__main__':
    game = GoBang()
    game.move((7, 7))
    print game.board
    game.move((8, 9))
    print game.board
