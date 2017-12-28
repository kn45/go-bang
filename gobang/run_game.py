#!/usr/bin/env python

from game import *
from player import *
from common import cprint


def play_game(game, p1, p2, verbose=True):
    players = [p1, p2]
    gprint = cprint(verbose)
    gprint(game.board)
    while game.game_status == GameStatus.UNDERGOING:
        player_idx = (game.player + 1) / 2  # (-1,+1) -> (0,1)
        move, value = players[player_idx].choose_best_move(game)
        succ = game.move(move)
        if not succ:
            gprint('Not available move')
            continue
        gprint(game.board)
    gprint('Res:' + str(game.game_status))
    return game.game_status


def play_gobang_rounds(p1, p2, nround=100):
    res_count = [0] * 3  # np1win, ndraw, np2win
    for _ in range(nround):
        res = play_game(GoBang(), p1, p2, verbose=False)
        res_count[res+1] += 1
    return res_count


if __name__ == '__main__':
    # play_game(GoBang(), RandomPlayer(), ManualPlayer())
    play_game(TicTacToe(), RandomPlayer(), ManualPlayer())
    print play_gobang_rounds(RandomPlayer(), RandomPlayer(), nround=100)
