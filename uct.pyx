import common
import copy
import numpy as np
import random
from game import GameStatus


class UCTNode(object):
    def __init__(self, parent=None):
        self._parent = parent
        self._children = {}
        self._nvisit = 0.0
        self._nwin = 0.0  # in the view of self's father
        self._C = 1.4

    def _update(self, nwin):
        self._nvisit += 1
        self._nwin += nwin

    def select(self):
        return max(self._children.items(), key=lambda child: child[1].score)

    def expand(self, actions):
        for action in actions:
            if action not in self._children:
                self._children[action] = UCTNode(parent=self)

    def backpropagate(self, nwin):
        p = self
        while p:
            p._update(nwin)
            nwin = 1.0 - nwin
            p = p._parent

    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None

    @property
    def score(self):
        # ret :  ucb in view of self's father
        if self._nvisit == 0:
            return 1e5
        else:
            return self._nwin/self._nvisit + \
                self._C * np.sqrt(np.log(self._parent._nvisit)/(self._nvisit))


class UCT(object):
    def __init__(self, nrollout):
        self._nrollout = nrollout
        self._root = UCTNode(None)

    def _search(self, game):
        # selection -> expansion -> simulation -> backpropagation
        node = self._root
        # selection
        while not node.is_leaf():
            act, node = node.select()
            game.move(act)
        if game.game_status != GameStatus.UNDERGOING:
            node2explore = node
            value = (game.player*game.game_status + 1.0) / 2.0  # self win probability
        else:  # not end
            # expansion
            node.expand(game.board.nearby_availables)
            children = node._children.items()
            act, node2explore = children[int(random.random()*len(children))]
            # simulation
            game.move(act)
            value = self._get_simulate_value(game)
        # backpropagation
        node2explore.backpropagate(1.0-value)

    def _get_simulate_value(self, game):
        # self win probability
        player = game.player
        while game.game_status == GameStatus.UNDERGOING:
            actions = game.board.nearby_availables
            act = actions[int(random.random()*len(actions))]
            game.move(act)
        return (player*game.game_status + 1.0) / 2.0

    def get_visit_prob(self, game):
        for n in range(self._nrollout):  # do nround of MC search
            common.draw_progress(n, self._nrollout, pref='AI thinking:', barlen=30)
            self._search(copy.deepcopy(game))
        print ''
        return [(act, child._nvisit/self._root._nvisit)
                for act, child in self._root._children.items()]

    def reset(self):
        self._root = UCTNode(None)


class UCTPlayer(object):
    def __init__(self):
        self._uct = UCT(nrollout=10000)

    def choose_best_move(self, game, *args):
        move_probs = self._uct.get_visit_prob(game)
        move, prob = max(move_probs, key=lambda x: x[1])
        self._uct.reset()
        return move, prob
