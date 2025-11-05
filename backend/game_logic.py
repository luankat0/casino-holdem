import random

suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def create_deck():
    return ["f{r}{s}" for s in suits for r in ranks]

def deal_hand():
    deck = create_deck()
    random.shuffle(deck)

    player_cards = deck[:2]
    dealer_cards = deck[2:4]
    table_cards = deck[4:9]

    return {
        "player_cards": player_cards,
        "dealer_cards": dealer_cards,
        "table_cards": table_cards
    }

def evaluate_winner(game):
    # Lógica simplificada pra ilustrar
    return {
        "winner": random.choice(["player", "dealer", "tie"])
    }