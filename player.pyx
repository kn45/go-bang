# -*- coding=utf8 -*-

import common
import random


class RandomPlayer(object):
    def choose_best_move(self, game, *args):
        avail_moves = game.board.nearby_availables
        value = -999
        return avail_moves[int(random.random()*len(avail_moves))], value


class ManualPlayer(object):
    def choose_best_move(self, game, *args):
        move = raw_input('Input position, e.g. f11\n')
        pos = common.h2pos(move, game.board.width)
        if not game.board.is_pos_in_board(pos):
            print 'Position should be within board'
            return self.choose_best_move(game)
        value = -999
        return pos, value
