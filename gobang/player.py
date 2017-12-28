# -*- coding=utf8 -*-

import game
import random
from itertools import product


class AvlMoves(object):
    """Available moves is an independent strategy from the game itself.
    """
    def __init__(self, board):
        self.__avl_moves = set([])
        self.__board = board
        self.update()  # init from scratch

    def __all_in_avail(self):
        # whether all the empty positions are in available moves
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
            stones = self.__board.all_stones
        else:
            stones = [pos]
        if len(stones) <= 0:  # board is empty, just add center
            board_center = self.__board.width / 2
            self.__avl_moves.add((board_center, board_center))
        else:  # board is not empty, add around pos
            while True:
                for stone in stones:
                    self.__add_around(stone, min_radius)
                min_radius += 1
                # until enough avl_moves or all the empty positions are in avl_moves
                if len(self.__avl_moves) >= min_count or self.__all_in_avail():
                    break

    def update(self, **kwargs):
        # used by game. game no nothing about the strategy
        last_pos = kwargs.get('last_pos')
        mr = 2  # varies with strategy
        mc = 20  # varies with strategy
        self.__update(last_pos, mr, mc)

    def _update_dbg(self, pos=None, min_radius=2, min_count=20):
        # for debug use
        self.__update(pos, min_radius, min_count)

    def get_all(self):
        return list(self.__avl_moves)


class Player(object):
    def __init__(self, player_idx=None):
        self.player_idx = player_idx

    # @override
    def choose_best_move(self, game):
        pass


class RandomPlayer(Player):
    def choose_best_move(self, game):
        avail_moves = game.get_available_moves()
        value = -999
        return avail_moves[int(random.random()*len(avail_moves))], value


class ManualPlayer(Player):
    def choose_best_move(self, game):
        move = raw_input('Input position, e.g. f11\n')
        row = int(move[1:])
        if row < 1 or row > 15:
            print 'Row should be within [1, 15]'
            return self.choose_best_move(game)
        col = move[0].lower()
        if col < 'a' or col > 'o':
            print 'Column should be within [a, o]'
            return self.choose_best_move(game)
        pos = (15-row, ord(col)-ord('a'))
        value = -999
        return pos, value


if __name__ == '__main__':
    game = game.Gobang()
    p1 = RandomPlayer(-1)
    p2 = RandomPlayer(+1)
    print p1.choose_best_move(game)
