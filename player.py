# -*- coding=utf8 -*-

import evaluate
import random
import search
from itertools import product
from game import *


class Player(object):
    def __init__(self, player_idx=None):
        self.PLAYER = player_idx

    def choose_best_move(self, game):
        raise NotImplementedError


class TicTacToePlayer(Player):
    def __init__(self, player_idx):
        super(TicTacToePlayer, self).__init__(player_idx)
        self.__search = search.MinMax(evaluate.SimpleEndEval(), max_depth=9)

    def choose_best_move(self, game):
        return self.__search.search_best_move(game, eval_side=self.PLAYER)


class GoBangPlayer(Player):
    def __init__(self, player_idx):
        super(GoBangPlayer, self).__init__(player_idx)
        self.__search = search.MinMax(evaluate.SimpleEndEval(), max_depth=3)

    def choose_best_move(self, game):
        return self.__search.search_best_move(game, eval_side=self.PLAYER)


class RandomPlayer(Player):
    def choose_best_move(self, game):
        avail_moves = game.get_available_moves()
        value = -999
        return avail_moves[int(random.random()*len(avail_moves))], value


class ManualPlayer(Player):
    def choose_best_move(self, game):
        move = raw_input('Input position, e.g. f11\n')
        row = int(move[1:])
        if row < 1 or row > game.board.width:
            print 'Row should be within board'
            return self.choose_best_move(game)
        col = move[0].lower()
        if col < 'a' or col > chr(ord('a')+game.board.width):
            print 'Column should be within board'
            return self.choose_best_move(game)
        pos = (game.board.width-row, ord(col)-ord('a'))
        value = -999
        return pos, value


if __name__ == '__main__':
    game = TicTacToe()
    p1 = RandomPlayer()
    p3 = TicTacToePlayer(-1)
    print dir(p3)
    print p3.choose_best_move(game)
