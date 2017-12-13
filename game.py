import copy
import itertools
import random


class TikTokToe(object):
    def __init__(self):
        self.board = [[0] * 3 for x in range(3)]
        self.player = -1  # -1 or +1
        self.line_sum = [0] * 8  # r1, r2, r3, c1, c2, c3, d1, d2
        self.win_status = 0
        self.available_moves = []
        _ = [self.available_moves.append(x) for x in itertools.product(range(3), range(3))]

    def __hash__(self):
        stat = '|'.join(['|'.join(map(str, x)) for x in self.board])
        stat += stat + ',' + str(self.player)
        return hash(stat)

    def __str__(self):
        sign = ['X', ' ', 'O']
        res = ''
        res += '-----' + '\n'
        for row in self.board:
            res += '|'.join([sign[x + 1] for x in row]) + '\n'
        res += '-----'
        return res

    def get_available_moves(self):
        return self.available_moves

    def is_end(self):
        return True if self.get_status() != 2 else False

    def get_status(self):
        # -1 win, 1 win, 0 draw, 2 undergoing
        if self.win_status:
            return self.win_status
        elif len(self.available_moves) <= 0:
            return 0
        else:
            return 2

    def move(self, pos):
        i, j = pos
        if self.board[i][j] != 0:
            raise Exception('not available move!')
        self.board[i][j] = self.player
        # update status
        self.line_sum[i] += self.player
        if self.line_sum[i] == self.player * 3:
            self.win_status = self.player
        self.line_sum[3 + j] += self.player
        if self.line_sum[3 + j] == self.player * 3:
            self.win_status = self.player
        if i == j:
            self.line_sum[6] += self.player
            if self.line_sum[6] == self.player * 3:
                self.win_status = self.player
        if i + j == 2:
            self.line_sum[7] += self.player
            if self.line_sum[7] == self.player * 3:
                self.win_status = self.player
        self.available_moves.remove(pos)
        # change player
        self.player = self.player * (-1)

    def get_eval(self, view_idx):
        # in view of player
        stat = self.get_status()
        res = stat * 10 * view_idx if abs(stat) == 1 else 0
        # print res
        return res


class MinMaxSimplePlayer(object):
    def __init__(self, player_idx):
        self.player = player_idx

    def get_best_move(self, game):
        return self.max_move(game)

    def max_move(self, game):
        # return the pos and value i.e. max value
        best_pos = None
        best_value = game.get_eval(self.player)
        if game.is_end():  # there's winner or full-board
            return best_pos, best_value
        moves = game.get_available_moves()
        # if moves is empty, return best_value = current_value
        for pos in moves:
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            min_value = self.min_move(game_after_move)
            if (best_pos is None) or min_value > best_value:
                best_pos = pos
                best_value = min_value
        return best_pos, best_value

    def min_move(self, game):
        # return the pos and value i.e. min value
        best_pos = None
        best_value = game.get_eval(self.player)
        if game.is_end():  # there's winner or full-board
            return best_value
        moves = game.get_available_moves()
        for pos in moves:
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            _, max_value = self.max_move(game_after_move)
            if (best_pos is None) or max_value < best_value:
                best_pos = pos
                best_value = max_value
        return best_value


class RandomPlayer(object):
    def get_best_move(self, game):
        moves = game.get_available_moves()
        move = moves[int(random.random() * len(moves))]
        return move, 0


class ManualPlayer(object):
    def get_best_move(self, game):
        move = raw_input('input position, e.g. 0,1\n')
        pos = map(int, move.split(','))
        return tuple(pos), 0


def random_vs_mmsimple():
    # players = [RandomPlayer(), MinMaxSimplePlayer(player_idx=1)]
    players = [MinMaxSimplePlayer(player_idx=-1), RandomPlayer()]
    ttt = TikTokToe()
    print ttt
    while not ttt.is_end():
        player_idx = (ttt.player + 1) / 2
        move, val = players[player_idx].get_best_move(ttt)
        ttt.move(move)
        print val
        print ttt
    print 'res: ', ttt.get_status()


def manual_vs_mmsimple():
    players = [ManualPlayer(), MinMaxSimplePlayer(player_idx=1)]
    ttt = TikTokToe()
    print ttt
    while not ttt.is_end():
        player_idx = (ttt.player + 1) / 2
        move, val = players[player_idx].get_best_move(ttt)
        ttt.move(move)
        print val
        print ttt
    print 'res: ', ttt.get_status()

def random_vs_random():
    p1 = RandomPlayer()
    ttt = TikTokToe()
    print ttt
    while not ttt.is_end():
        move, val = p1.get_best_move(ttt)
        ttt.move(move)
        print ttt


if __name__ == '__main__':
    # random_vs_mmsimple()
    manual_vs_mmsimple()
