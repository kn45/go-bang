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

    def get_value(self, view_idx):
        # in view of player
        stat = self.get_status()
        res = stat * 10 * view_idx if abs(stat) == 1 else 0
        return res


class MinMaxABPlayer(object):
    def __init__(self, player_idx):
        self.PLAYER = player_idx
        self.MIN_VAL = -100
        self.MAX_VAL = +100

    def get_best_move(self, game):
        res = self.max_move(game, level=0, alpha=self.MIN_VAL, beta=self.MAX_VAL)
        return res

    def max_move(self, game, level, alpha, beta):
        # return the pos and value i.e. max value
        best_pos = None
        best_value = self.MIN_VAL
        if game.is_end():  # there's winner or full-board
            return best_pos, game.get_value(self.PLAYER)
        moves = game.get_available_moves()
        # if moves is empty, return best_value = current_value
        for ntrial, pos in enumerate(moves):
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            min_value = self.min_move(game_after_move, level - 1, alpha, beta)
            if min_value > best_value:
                best_pos = pos
                best_value = min_value
            alpha = max(best_value, alpha)
            if alpha >= beta:
                break
        return best_pos, best_value

    def min_move(self, game, level, alpha, beta):
        # return the pos and value i.e. min value
        # alpha is the best_value for now in a max_move
        # beta is the best_value for now in a min_move
        best_pos = None
        best_value = self.MAX_VAL
        if game.is_end():  # there's winner or full-board
            return game.get_value(self.PLAYER)
        moves = game.get_available_moves()
        for ntrial, pos in enumerate(moves):
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            _, max_value = self.max_move(game_after_move, level - 1, alpha, beta)
            # update value
            if max_value < best_value:
                best_pos = pos
                best_value = max_value
            # update beta
            beta = min(best_value, beta)
            if beta <= alpha:  # < or <= ?
                break
        return best_value


class MinMaxBasicPlayer(object):
    def __init__(self, player_idx):
        self.player = player_idx

    def get_best_move(self, game):
        return self.max_move(game)

    def max_move(self, game):
        # return the pos and value i.e. max value
        best_pos = None
        best_value = None
        if game.is_end():  # there's winner or full-board
            return best_pos, game.get_value(self.player)
        moves = game.get_available_moves()
        # if moves is empty, return best_value = current_value
        for pos in moves:
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            min_value = self.min_move(game_after_move)
            if (best_value is None) or min_value > best_value:
                best_pos = pos
                best_value = min_value
        return best_pos, best_value

    def min_move(self, game):
        # return the pos and value i.e. min value
        best_pos = None
        best_value = None
        if game.is_end():  # there's winner or full-board
            return game.get_value(self.player)
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
        return move, -999


class ManualPlayer(object):
    def get_best_move(self, game):
        move = raw_input('input position, e.g. 0,1\n')
        pos = map(int, move.split(','))
        return tuple(pos), -999


def mmab_vs_mmab():
    players = [MinMaxABPlayer(player_idx=-1), MinMaxABPlayer(player_idx=+1)]
    ttt = TikTokToe()
    while not ttt.is_end():
        player_idx = (ttt.player + 1) / 2
        move, val = players[player_idx].get_best_move(ttt)
        ttt.move(move)
    print 'res: ', ttt.get_status()


def random_vs_mmab(random_first=True):
    if random_first:
        players = [RandomPlayer(), MinMaxABPlayer(player_idx=+1)]
    else:
        players = [MinMaxABPlayer(player_idx=-1), RandomPlayer()]
    ttt = TikTokToe()
    while not ttt.is_end():
        player_idx = (ttt.player + 1) / 2
        move, val = players[player_idx].get_best_move(ttt)
        ttt.move(move)
    print 'res: ', ttt.get_status()


def manual_vs_mmbasic():
    players = [ManualPlayer(), MinMaxBasicPlayer(player_idx=1)]
    ttt = TikTokToe()
    print ttt
    while not ttt.is_end():
        player_idx = (ttt.player + 1) / 2
        move, val = players[player_idx].get_best_move(ttt)
        ttt.move(move)
        print ttt
        print val
    print 'res: ', ttt.get_status()


def manual_vs_mmab():
    players = [ManualPlayer(), MinMaxABPlayer(player_idx=1)]
    ttt = TikTokToe()
    print ttt
    print ''
    while not ttt.is_end():
        player_idx = (ttt.player + 1) / 2
        move, val = players[player_idx].get_best_move(ttt)
        ttt.move(move)
        print ttt
        print 'p', ttt.player * (-1), val
        print ''
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
    for _ in range(100):
        # random_vs_mmbasic()
        # manual_vs_mmbasic()
        # manual_vs_mmab()
        # random_vs_mmab()
        mmab_vs_mmab()
