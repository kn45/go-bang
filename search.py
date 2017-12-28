import copy
from game import GameStatus


class Search(object):
    # @override
    def search_best_move(self, game, eval_side):
        pass


class MinMax(Search):
    def __init__(self, evaluate, max_depth):
        self.__MIN_VAL = evaluate.MIN_VAL
        self.__MAX_VAL = evaluate.MAX_VAL
        self.__evaluate = evaluate
        self.__MAX_DEPTH = max_depth

    def __max_move(self, game, level, alpha, beta):
        # return the pos and best(max) value
        # alpha is the best_value for now in a max_move
        # beta is the best_value for now in a min_move
        best_pos = None
        best_value = self.__MIN_VAL
        if game.game_status != GameStatus.UNDERGOING or abs(level) > self.__MAX_DEPTH:
            return best_pos, self.__evaluate.evaluate(game=game, eval_side=self.__eval_side)
        moves = game.get_available_moves()
        for pos in moves:
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            min_value = self.__min_move(game_after_move, level-1, alpha, beta)
            if min_value > best_value:
                best_pos = pos
                best_value = min_value
            alpha = max(best_value, alpha)
            if alpha >= beta:
                break
        return best_pos, best_value

    def __min_move(self, game, level, alpha, beta):
        # return the best(min) value
        best_pos = None
        best_value = self.__MAX_VAL
        if game.game_status != GameStatus.UNDERGOING or abs(level) > self.__MAX_DEPTH:
            return self.__evaluate.evaluate(game=game, eval_side=self.__eval_side)
        moves = game.get_available_moves()
        for pos in moves:
            game_after_move = copy.deepcopy(game)
            game_after_move.move(pos)
            _, max_value = self.__max_move(game_after_move, level-1, alpha, beta)
            # update best value and beta
            if max_value < best_value:
                best_pos = pos
                best_value = max_value
            beta = min(best_value, beta)
            if beta <= alpha:
                break
        return best_value

    def search_best_move(self, game, eval_side):
        self.__eval_side = eval_side
        return self.__max_move(game, level=0, alpha=self.__MIN_VAL, beta=self.__MAX_VAL)
