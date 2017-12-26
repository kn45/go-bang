# -*- coding=utf8 -*-

import common
import sys
from board import GobangBoard
from itertools import product


class AvlMove(object):
    """Available moves is an independent strategy from the game itself.
    """
    def __init__(self, board):
        self.__avl_moves = set([])
        self.board = board

    def __all_in_avail(self):
        # whether all the empty points are in available moves
        return True if len(self.__avl_moves) >= self.board.capacity else False

    def update(self, pos, radius=2):
        c_i, c_j = pos
        up_range = range(c_i-radius, c_i+radius+1)
        for row, col in product(up_range, up_range):
            if not self.board.pos_inboard((row, col)):
                continue
            if self.board[row][col] == 0:
                self.__avl_moves.add((row, col))
        self.__avl_moves.remove((c_i, c_j))
        # if there are too few available moves around
        if len(self.__avl_moves) < 20 and not self.__all_in_avail(self.board):
            self.update(self, pos, radius+1)

    def get_all(self):
        return self.__avl_moves


class Gobang(object):
    def __init__(self):
        self.board = GobangBoard()
        self.player = -1  # -1 or +1
        self.__game_status = 2  # ±1 for each winner, 0 for draw, 2 for undergoing
        self.__avl_move = AvlMove(self.board)

    def __check_win_status(self, pos):
        # evaluate winner
        # ±1 - each winner
        #  0 - other case
        c_i, c_j = pos
        # check row direction
        mass_row = self.board.max_abs_subsum((c_i, c_j-4), (c_i, c_j+4))
        mass_col = self.board.max_abs_subsum((c_i-4, c_j), (c_i+4, c_j))
        mass_diag = self.board.max_abs_subsum((c_i-4, c_j-4), (c_i+4, c_j+4))
        max_abs_val = common.max_abs_sum([mass_row, mass_col, mass_diag])
        return common.sign(max_abs_val) if abs(max_abs_val) == 5 else 0

    def __is_full(self):
        return True if self.board.capacity <= 0 else False

    def _update_game_status(self, pos):
        # ±1 each winner
        #  0 draw
        #  2 undergoing
        win_status = self.__check_win_status(pos)
        self.__game_status = win_status if win_status != 0 else \
            (0 if self.__check_full_status else 2)

    def move(self, pos):
        self.board.place(pos, self.player)
        # update available moves
        self.__avl_move.update(pos)
        # update game status
        self._update_game_status(pos)
        # switch player
        self.player *= -1

    def get_game_status(self):
        return self.__game_status

    def get_available_moves(self):
        return self.__avl_move.get_all()
