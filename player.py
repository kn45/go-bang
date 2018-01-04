# -*- coding=utf8 -*-

import common
import conf
import evaluate
import random
import search
import policy
from itertools import product
from game import *


class Player(object):
    def __init__(self, player_idx=None):
        self.PLAYER = player_idx

    def choose_best_move(self, game, *args):
        raise NotImplementedError


class TicTacToePlayer(Player):
    def __init__(self, player_idx):
        super(TicTacToePlayer, self).__init__(player_idx)
        self.__search = search.MinMax(
            evaluate.SimpleEndEval(),
            policy.NearbyMoves(),
            max_depth=conf.tictactoe_minmax_depth)

    def choose_best_move(self, game, *args):
        return self.__search.search_best_move(game, eval_side=self.PLAYER)


class GoBangPlayer(Player):
    def __init__(self, player_idx):
        super(GoBangPlayer, self).__init__(player_idx)
        self.__search = search.MinMax(
            evaluate.SimpleEndEval(),
            policy.NearbyMoves(),
            max_depth=conf.gobang_minmax_depth)

    def choose_best_move(self, game, *args):
        common.dprint('considering...')
        pos, value = self.__search.search_best_move(game, eval_side=self.PLAYER)
        common.dprint('\t'.join(['my move:', common.pos2h(pos, game.board.width), str(value)]))
        return pos, value


class RandomPlayer(Player):
    def choose_best_move(self, game, *args):
        avail_moves = policy.NearbyMoves().gen_moves(game.board)
        value = -999
        return avail_moves[int(random.random()*len(avail_moves))], value


class ManualPlayer(Player):
    def choose_best_move(self, game, *args):
        move = raw_input('Input position, e.g. f11\n')
        pos = common.h2pos(move, game.board.width)
        if not game.board.is_pos_in_board(pos):
            print 'Position should be within board'
            return self.choose_best_move(game)
        value = -999
        return pos, value


if __name__ == '__main__':
    game = TicTacToe()
    p1 = RandomPlayer()
    p3 = TicTacToePlayer(-1)
    print dir(p3)
    print p3.choose_best_move(game)
