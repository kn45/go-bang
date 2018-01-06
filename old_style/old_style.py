# -*- coding=utf8 -*-

import common
import conf
import copy
import random
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
            max_depth=conf.tictactoe_minmax_depth)

    def choose_best_move(self, game, *args):
        return self.__search.search_best_move(game, eval_side=self.PLAYER)


class GoBangPlayer(Player):
    def __init__(self, player_idx):
        super(GoBangPlayer, self).__init__(player_idx)
        self.__search = search.MinMax(
            evaluate.SimpleEndEval(),
            max_depth=conf.gobang_minmax_depth)

    def choose_best_move(self, game, *args):
        common.dprint('considering...')
        pos, value = self.__search.search_best_move(game, eval_side=self.PLAYER)
        common.dprint('\t'.join(['my move:', common.pos2h(pos, game.board.width), str(value)]))
        return pos, value


class Search(object):
    def search_best_move(self, game, eval_side):
        raise NotImplementedError


class MinMax(Search):
    def __init__(self, evaluate, max_depth):
        self.__MIN_VAL = evaluate.MIN_VAL
        self.__MAX_VAL = evaluate.MAX_VAL
        self.__MAX_DEPTH = max_depth
        self.__evaluate = evaluate

    def __max_move(self, game, level, alpha, beta):
        # return the pos and best(max) value
        # alpha is the best_value for now in a max_move
        # beta is the best_value for now in a min_move
        best_pos = None
        best_value = self.__MIN_VAL
        if game.game_status != GameStatus.UNDERGOING or abs(level) > self.__MAX_DEPTH:
            return best_pos, self.__evaluate.evaluate(game=game, eval_side=self.__eval_side)
        moves = game.board.nearby_availables
        if level == 0:
            common.dprint(
                'avl moves: ' + ' '.join([common.pos2h(p, game.board.width) for p in moves]))
        for pos in moves:
            if level == 0:
                common.dprint(common.pos2h(pos, game.board.width) + ' ', False)
            game.move(pos)
            min_value = self.__min_move(game, level-1, alpha, beta)
            game.undo_move()
            if min_value > best_value:
                best_pos = pos
                best_value = min_value
            alpha = max(best_value, alpha)
            if alpha >= beta:
                break
        return best_pos, best_value

    def __min_move(self, game, level, alpha, beta):
        # return the best(min) value
        best_pos = None
        best_value = self.__MAX_VAL
        if game.game_status != GameStatus.UNDERGOING or abs(level) > self.__MAX_DEPTH:
            return self.__evaluate.evaluate(game=game, eval_side=self.__eval_side)
        moves = game.board.nearby_availables
        for pos in moves:
            game.move(pos)
            _, max_value = self.__max_move(game, level-1, alpha, beta)
            game.undo_move()
            # update best value and beta
            if max_value < best_value:
                best_pos = pos
                best_value = max_value
            beta = min(best_value, beta)
            if beta <= alpha:
                break
        return best_value

    def search_best_move(self, game, eval_side):
        self.__eval_side = eval_side
        res = self.__max_move(game, level=0, alpha=self.__MIN_VAL, beta=self.__MAX_VAL)
        common.dprint(str(res))
        return res


class Evaluate(object):
    def __init__(self, min_val, max_val):
        self.__MIN_VAL = min_val
        self.__MAX_VAL = max_val

    @property
    def MIN_VAL(self):
        return self.__MIN_VAL

    @property
    def MAX_VAL(self):
        return self.__MAX_VAL

    def evaluate(self, **kwargs):
        raise NotImplementedError


class SimpleEndEval(Evaluate):
    def __init__(self):
        super(SimpleEndEval, self).__init__(-1, +1)

    def evaluate(self, **kwargs):
        game = kwargs.get('game')
        eval_side = kwargs.get('eval_side')
        if game.game_status in [GameStatus.WIN1, GameStatus.WIN2]:
            return game.game_status * eval_side
        else:
            return 0

