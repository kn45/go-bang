from itertools import product


class AvlMoves(object):
    """Available moves is an independent strategy from the game itself.
    """
    def __init__(self, board):
        self.__avl_moves = set([])
        self.__board = board
        self.update()  # init from scratch

    def __all_in_avail(self):
        # whether all the empty positions are in available moves
        return True if len(self.__avl_moves) >= self.__board.capacity else False

    def __add_around(self, pos, radius=2):
        # update available moves around the position
        c_i, c_j = pos
        update_range = range(c_i-radius, c_i+radius+1)
        for row, col in product(update_range, update_range):
            if not self.__board.is_pos_in_board((row, col)):
                continue
            if self.__board[row][col] == 0:
                self.__avl_moves.add((row, col))

    def __update(self, pos, min_radius, min_count):
        # pos = None means search and update from scratch
        # if the board is empty, just add the center point to available_moves
        if pos is None:
            stones = self.__board.all_stones
        else:
            stones = [pos]
        if len(stones) <= 0:  # board is empty, just add center
            board_center = self.__board.width / 2
            self.__avl_moves.add((board_center, board_center))
        else:  # board is not empty, add around pos
            while True:
                for stone in stones:
                    self.__add_around(stone, min_radius)
                min_radius += 1
                # until enough avl_moves or all the empty positions are in avl_moves
                if len(self.__avl_moves) >= min_count or self.__all_in_avail():
                    break

    def update(self, **kwargs):
        # used by game. game no nothing about the strategy
        last_pos = kwargs.get('last_pos')
        mr = 2  # varies with strategy
        mc = 20  # varies with strategy
        self.__update(last_pos, mr, mc)

    def _update_dbg(self, pos=None, min_radius=2, min_count=20):
        # for debug use
        self.__update(pos, min_radius, min_count)

    def get_all(self):
        return list(self.__avl_moves)
