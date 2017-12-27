# -*- coding=utf8 -*-


class Player(object):
    def __init__(self, player_idx):
        self.player_idx = player_idx


class RandomPlayer(Player):
    def get_move(self):
