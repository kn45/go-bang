# -*- coding=utf8 -*-

import gobang
import random


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
        move = raw_input('input position, e.g. f11\n')
        col = int(move[1:])
        if col < 1 or col > 15:
            print 'column should be within [1, 15]'
            return self.choose_best_move(game)
        row = move[0].lower()
        if row < 'a' or row > 'f':
            print 'row should be within [a, f]'
            return self.choose_best_move(game)
        pos = (ord(row)-ord('a'), col-1)
        value = -999
        return pos, value


if __name__ == '__main__':
    game = gobang.Gobang()
    p1 = RandomPlayer(-1)
    p2 = RandomPlayer(+1)
    print p1.choose_best_move(game)
