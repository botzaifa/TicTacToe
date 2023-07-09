from flask import Flask, render_template, jsonify, request
from random import randint

app = Flask(__name__)

class Player():
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker

class Game:
    p1 = Player('Player', 'X')
    p2 = Player('Computer', 'O')
    is_p1_turn = True
    game_over = False
    game_board = [' '] * 9

    def __init__(self):
        self.count = 0

    def make_move(self, index):
        if self.game_board[index] == ' ' and not self.game_over:
            self.game_board[index] = self.p1.marker if self.is_p1_turn else self.p2.marker
            self.count += 1
            self.check_result(self.p1 if self.is_p1_turn else self.p2)
            if self.count != 9 and not self.game_over and not self.is_p1_turn:
                self.computer_move()

            return True
        return False

    def computer_move(self):
        while True:
            index = randint(0, 8)
            if self.game_board[index] == ' ':
                self.make_move(index)
                break

    def check_result(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combination in winning_combinations:
            a, b, c = combination
            if (
                self.game_board[a] == self.game_board[b] == self.game_board[c] == player.marker
            ):
                self.game_over = True
                return

        if self.count == 9:
            self.game_over = True

game = Game()  # Move this line here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    index = int(request.form['index'])
    if game.make_move(index):
        return jsonify(success=True, marker=game.game_board[index])
    else:
        return jsonify(success=False, message="Invalid move.")

if __name__ == '__main__':
    app.run(debug=True)
