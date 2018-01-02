from itertools import product


class NearbyMoves(object):
    def __init__(self):
        self.__MIN_COUNT = 20
        self.__MIN_RADIUS = 2

    def __add_around(self, board, moves, pos, radius=2):
        # update available moves around the position
        c_i, c_j = pos
        update_range = range(c_i-radius, c_i+radius+1)
        for row, col in product(update_range, update_range):
            if not board.is_pos_in_board((row, col)):
                continue
            if board[row][col] == 0:
                moves.add((row, col))
        return moves

    def __all_in_avail(self, moves, board):
        # whether all the empty positions are in available moves
        return True if len(moves) >= board.capacity else False

    def gen_moves(self, board, radius=None):
        if radius is None:
            radius = self.__MIN_RADIUS
        if board.is_empty():
            center = int(board.width / 2)
            return [(center, center)]
        moves = set([])
        while True:
            for pos in board.all_stones:
                moves = self.__add_around(board, moves, pos, radius)
            if self.__all_in_avail(moves, board) or \
                    len(moves) >= self.__MIN_COUNT:
                return list(moves)
            radius += 1
