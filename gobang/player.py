# -*- coding=utf8 -*-

import copy
import random
from itertools import product
from game import *


class Player(object):
    def __init__(self, player_idx=None):
        self.PLAYER = player_idx

    # @override
    def choose_best_move(self, game):
        pass


class AiPlayer(Player):
    def __init__(self, player_idx):
        super(AiPlayer, self).__init__(player_idx)
        self.MIN_VAL = -100
        self.MAX_VAL = +100
        self.MAX_DEPTH = 4
        self.__evaluate = lambda x, y: random.random()

    def __max_move(self, game, level, alpha, beta):
        # return the pos and best(max) value
        # alpha is the best_value for now in a max_move
        # beta is the best_value for now in a min_move
        best_pos = None
        best_value = self.MIN_VAL
        if game.game_status != GameStatus.UNDERGOING or abs(level) > self.MAX_DEPTH:
            return best_pos, self.__evaluate(game.board, self.PLAYER)
        moves = game.get_available_moves()
        for pos in moves:
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            min_value = self.__min_move(game_after_move, level-1, alpha, beta)
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
        best_value = self.MAX_VAL
        if game.game_status != GameStatus.UNDERGOING or abs(level) > self.MAX_DEPTH:
            return self.__evaluate(game.board, self.PLAYER)
        moves = game.get_available_moves()
        for pos in moves:
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            _, max_value = self.__max_move(game_after_move, level-1, alpha, beta)
            # update best value and beta
            if max_value < best_value:
                best_pos = pos
                best_value = max_value
            beta = min(best_value, beta)
            if beta <= alpha:
                break
        return best_value

    def choose_best_move(self, game):
        return self.__max_move(game, level=0, alpha=self.MIN_VAL, beta=self.MAX_VAL)


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
    game = GoBang()
    p1 = RandomPlayer()
    p3 = AiPlayer(-1)
    print p3.choose_best_move(game)
