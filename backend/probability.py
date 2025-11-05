import random

def compute_probabilities(game):
    player_win = random.uniform(0.3, 0.7)
    dealer_win = 1 - player_win
    return {
        "player_win": round(player_win, 2),
        "dealer_win": round(dealer_win, 2)
    }