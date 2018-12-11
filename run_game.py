#!/usr/bin/env python

from uct import *
from game import *
from player import *
from common import cprint, pos2h


def play_game(game, p1, p2, verbose=True):
    players = [p1, p2]
    gprint = cprint(verbose)
    gprint(game.board)
    while game.game_status == GameStatus.UNDERGOING:
        player_idx = (game.player + 1) / 2  # (-1,+1) -> (0,1)
        move, value = players[player_idx].choose_best_move(game, True)
        game.move(move)
        gprint(game.board)
        print 'last move:', pos2h(move, 15)
    gprint('Res:' + str(game.game_status))
    return game.game_status


def play_gobang_rounds(p1, p2, nround=100):
    res_count = [0] * 3  # np1win, ndraw, np2win
    for _ in range(nround):
        res = play_game(GoBang(), p1, p2, verbose=False)
        res_count[res+1] += 1
    return res_count


def play_tictactoe_rounds(p1, p2, nround=100):
    res_count = [0] * 3  # np1win, ndraw, np2win
    for _ in range(nround):
        res = play_game(TicTacToe(), p1, p2, verbose=False)
        res_count[res+1] += 1
    return res_count


if __name__ == '__main__':
    # play_game(GoBang(), RandomPlayer(), ManualPlayer())
    # play_game(GoBang(), RandomPlayer(), GoBangPlayer())
    # play_game(GoBang(), RandomPlayer(), UCTPlayer())
    # play_game(GoBang(), ManualPlayer(), UCTPlayer())
    # play_game(GoBang(), UCTPlayer(), UCTPlayer())
    play_game(GoBang(), UCTPlayer(), ManualPlayer())
    # print play_gobang_rounds(RandomPlayer(), GoBangPlayer(), nround=10)

    # play_game(TicTacToe(), ManualPlayer(), TicTacToePlayer())
    # play_game(TicTacToe(), RandomPlayer(), TicTacToePlayer())
    # play_game(TicTacToe(), UCTPlayer(), RandomPlayer())
    # play_game(TicTacToe(), ManualPlayer(), UCTPlayer())
    # print play_tictactoe_rounds(RandomPlayer(), TicTacToePlayer(), nround=100)
    # print play_tictactoe_rounds(UCTPlayer(), RandomPlayer(), nround=100)
