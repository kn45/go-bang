#!/usr/bin/env python

from board import *
from gobang import *
from player import *


def rand_vs_rand():
    p1 = RandomPlayer()
    game = Gobang()
    while game.game_status == 2:
        move, value = p1.choose_best_move(game)
        game.move(move)
        print game.board
    print 'res:', game.game_status


if __name__ == '__main__':
    rand_vs_rand()
