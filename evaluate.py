def evaluate_simple_end(game, p_idx):
    if abs(game.game_status) == 1:
        return game.game_status * p_idx
    else:
        return 0
