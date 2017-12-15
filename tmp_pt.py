import copy
import itertools
import random


class PlaceT(object):
    def __init__(self, width=7):
        self.width = width
        self.board = [[0] * self.width for x in range(self.width)]
        self.nround = 1
        self.pointmoves = {}
        self.available_moves = {}

        self._set_all_available_moves()

    def _in_board(self, points):
        ret = True
        for i, j in points:
            if i < 0 or i >= self.width or j < 0 or j >= self.width:
                ret = False
                break
        return ret

    def points_of_move(self, move):
        i, j, k = move
        res = []
        res.append((i, j))
        if k != 0:
            res.append((i - 1, j))
        else:
            res.append((i + 2, j))
        if k != 1:
            res.append((i, j - 1))
        else:
            res.append((i, j + 2))
        if k != 2:
            res.append((i + 1, j))
        else:
            res.append((i - 2, j))
        if k != 3:
            res.append((i, j + 1))
        else:
            res.append((i, j - 2))
        return res

    def _set_all_available_moves(self):
        for center in itertools.product(range(self.width), range(self.width)):
            for direc in range(4):
                points = self.points_of_move((center[0], center[1], direc))
                if self._in_board(points):
                    self.available_moves[(center[0], center[1], direc)] = ''
                    for point in points:
                        if point not in self.pointmoves:
                            self.pointmoves[point] = []
                        self.pointmoves[point].append((center[0], center[1], direc))

    def __str__(self):
        sign = [' ', 'A']
        res = ''
        res += '-' * (2 * self.width - 1) + '\n'
        for row in self.board:
            res += '|'.join([chr(ord('A') + x - 1) if x > 0 else ' ' for x in row]) + '\n'
        res += '-' * (2 * self.width - 1)
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


if __name__ == '__main__':
    pt = PlaceT(5)
    print pt
    print pt.get_available_moves()
    print pt.pointmoves
