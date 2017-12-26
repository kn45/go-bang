# -*- coding=utf8 -*-

import sys
from board import GobangBoard
from itertools import product


class AvailMove(object):
    """Available moves is an independent strategy with the game itself.
    """
    def __init__(self, board):
        self.avail_moves = set([])
        self.board = board

    def update(self, pos, radius=2):
        c_i, c_j = pos
        up_range = range(c_i-radius, c_i+radius+1)
        for row, col in product(up_range, up_range):
            if not self.board.pos_in_board((row, col)):
                continue
            if self.board[row][col] == 0:
                self.avail_moves.add((row, col))
        self.avail_moves.remove((c_i, c_j))
        # if there are few available moves around
        if len(self.avail_moves) < 20 and not self._all_in_avail(self.board):
            self.update(self, pos, radius+1)

    def get_all(self):
        return self.avail_moves

    def _all_in_avail(self):
        # whether all the empty points are in available moves
        if len(self.avail_moves) + self.board.point_count \
                >= self.board.width ** 2:
            return True
        else False


class Gobang(object):
    def __init__(self):
        self._board = GobangBoard()
        self.player = -1  # -1 or +1
        self.win_status = 0  # ±1 for each winner, 0 for {draw, undergoing}
        self.avail_move = AvailMove(self._board)
        self.acc_cnt = 0  # how many positions on board is used

    def move(self, pos):
        self._board.place(pos, self.player)
        # update available moves
        self.avail_move.update(pos)
        # switch player
        self.player *= -1

    def check_win(self, pos):
        # evaluate winner
        c_i, c_j = pos
        # check row direction
        maxsum = self._board.max_abs_subsum((c_i, c_j-4), (c_i, c_j+4))
        if abs(maxsum) == 5:
            self.win_status = sign(maxsum)
        # check col direction
        maxsub, minsub = self._board.max_min_subsum((c_i-4, c_j), (c_i+4, c_j))
        if abs(maxsum) == 5:
            self.win_status = sign(maxsum)
        # check diag direction
        maxsub, minsub = self._board.max_min_subsum(
            (c_i-4, c_j-4), (c_i+4, c_j+4))

    def check_full(self):
        if self._board.point_count >= self._board.width ** 2:
            return True
        else:
            False
