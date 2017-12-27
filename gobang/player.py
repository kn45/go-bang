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


if __name__ == '__main__':
    game = gobang.Gobang()
    p1 = RandomPlayer(-1)
    p2 = RandomPlayer(+1)
    print p1.choose_best_move(game)
