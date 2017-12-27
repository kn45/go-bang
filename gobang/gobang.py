# -*- coding=utf8 -*-

import common
import sys
from board import GobangBoard
from itertools import product


class AvlMoves(object):
    """Available moves is an independent strategy from the game itself.
    """
    def __init__(self, board):
        self.__avl_moves = set([])
        self.__board = board
        self.update()  # init from scratch

    def __all_in_avail(self):
        # whether all the empty points are in available moves
        return True if len(self.__avl_moves) >= self.__board.capacity else False

    def __add_around(self, pos, radius=2):
        # update available moves around the position
        c_i, c_j = pos
        update_range = range(c_i-radius, c_i+radius+1)
        for row, col in product(update_range, update_range):
            if not self.__board.is_pos_in_board((row, col)):
                continue
            if self.__board[row][col] == 0:
                self.__avl_moves.add((row, col))

    def __update(self, pos, min_radius, min_count):
        # pos = None means search and update from scratch
        # if the board is empty, just add the center point to available_moves
        if pos is None:
            center_poss = self.__board.all_points
        else:
            center_poss = [pos]
        if len(center_poss) <= 0:  # board is empty, just add center
            board_center = self.__board.width / 2
            self.__avl_moves.add((board_center, board_center))
        else:  # board is not empty, add around pos
            while True:
                for point in center_poss:
                    self.__add_around(point, min_radius)
                min_radius += 1
                # until enough avl_moves or all the empty points are in avl_moves
                if len(self.__avl_moves) >= min_count or self.__all_in_avail():
                    break

    def update(self, pos=None):
        # used by game. game no nothing about the strategy
        mr = 2  # varies with strategy
        mc = 20  # varies with strategy
        self.__update(pos, mr, mc)

    def _update_dbg(self, pos=None, min_radius=2, min_count=20):
        # for debug use
        self.__update(pos, min_radius, min_count)

    def get_all(self):
        return list(self.__avl_moves)


class Gobang(object):
    def __init__(self):
        self.__board = GobangBoard()
        self.__player = -1  # -1 or +1
        self.__game_status = 2  # ±1 for each winner, 0 for draw, 2 for undergoing
        self.__avl_move = AvlMoves(self.__board)

    def __check_win_status(self, pos):
        # evaluate winner
        # ±1 - each winner
        #  0 - other case
        c_i, c_j = pos
        # check row direction
        mass_row = self.__board.max_abs_subsum((c_i, c_j-4), (c_i, c_j+4))
        mass_col = self.__board.max_abs_subsum((c_i-4, c_j), (c_i+4, c_j))
        mass_diag = self.__board.max_abs_subsum((c_i-4, c_j-4), (c_i+4, c_j+4))
        max_abs_val = common.max_abs([mass_row, mass_col, mass_diag])
        return common.sign(max_abs_val) if abs(max_abs_val) == 5 else 0

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
        # ±1 each winner
        #  0 draw
        #  2 undergoing
        win_status = self.__check_win_status(pos)
        self.__game_status = win_status if win_status != 0 else \
            (0 if self.__board.is_full() else 2)

    def move(self, pos):
        succ = self.__board.place(pos, self.__player)
        if not succ:
            return False
        # update available moves
        self.__avl_move.update(pos)
        # update game status
        self.__update_game_status(pos)
        # switch player
        self.__player *= -1
        return True

    def get_available_moves(self):
        return self.__avl_move.get_all()


if __name__ == '__main__':
    avl_moves = AvlMoves(GobangBoard())
    print avl_moves.get_all()
    avl_moves._update_dbg(pos=(3, 3), min_radius=1, min_count=0)
    print avl_moves.get_all()

    game = Gobang()
    print game.get_available_moves()
    game.move((7, 7))
    print game.board
    print game.get_available_moves()
    game.move((8, 9))
    print game.board
