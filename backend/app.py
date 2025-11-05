from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from game_logic import deal_hand, evaluate_winner
from probability import compute_probabilities

app = Flask(__name__)
CORS(app)

current_game = {
    "player_cards": [],
    "dealer_cards": [],
    "table_cards": []
}

@app.route("/start", methods=["POST"])
def start_game():
    global current_game
    current_game = deal_hand()
    return jsonify(current_game)

@app.route("/probabilities", methods=["GET"])
def get_probabilities():
    probs = compute_probabilities(current_game)
    return jsonify(probs)

@app.route("/evaluate", methods=["POST"])
def evaluate():
    result = evaluate_winner(current_game)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)