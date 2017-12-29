from game import GameStatus

class Evaluate(object):
    def __init__(self, min_val, max_val):
        self.__MIN_VAL = min_val
        self.__MAX_VAL = max_val

    @property
    def MIN_VAL(self):
        return self.__MIN_VAL

    @property
    def MAX_VAL(self):
        return self.__MAX_VAL

    def evaluate(self, **kwargs):
        raise NotImplementedError


class SimpleEndEval(Evaluate):
    def __init__(self):
        super(SimpleEndEval, self).__init__(-1, +1)

    def evaluate(self, **kwargs):
        game = kwargs.get('game')
        eval_side = kwargs.get('eval_side')
        if game.game_status in [GameStatus.WIN1, GameStatus.WIN2]:
            return game.game_status * eval_side
        else:
            return 0


if __name__ == '__main__':
    s = SimpleEndEval()
    print dir(s)
    print s.MIN_VAL
