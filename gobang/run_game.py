#!/usr/bin/env python

from board import *
from gobang import *
from player import *


def play_game(p1_cls, p2_cls):
    players = [RandomPlayer(), ManualPlayer()]
    return game.game_status

def rand_vs_rand():
    p1 = RandomPlayer()
    game = Gobang()
    print game.board
    while game.game_status == 2:
        move, value = p1.choose_best_move(game)
        game.move(move)
        print game.board
    print 'res:', game.game_status


def rand_vs_manual():
    players = [RandomPlayer(), ManualPlayer()]
    game = Gobang()
    print game.board
    while game.game_status == 2:
        player_idx = (ttt.player + 1) / 2  # (-1,+1) -> (0,1)
        move, value = players[player_idx].choose_best_move(game)
        game.move(move)
        print game.board
    print 'res:', game.game_status


if __name__ == '__main__':
    print type(RandomPlayer)
    #rand_vs_rand()
