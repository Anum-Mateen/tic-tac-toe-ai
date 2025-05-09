import math

class Game:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def display(self):
        print("\nCurrent Board:")
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, val in enumerate(self.board) if val == ' ']

    def make_move(self, pos, letter):
        if self.board[pos] == ' ':
            self.board[pos] = letter
            if self.check_winner(pos, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        row = square // 3
        if all([self.board[row*3 + i] == letter for i in range(3)]):
            return True
        col = square % 3
        if all([self.board[col + i*3] == letter for i in range(3)]):
            return True
        if square % 2 == 0:
            if all([self.board[i] == letter for i in [0, 4, 8]]):
                return True
            if all([self.board[i] == letter for i in [2, 4, 6]]):
                return True
        return False

    def is_full(self):
        return ' ' not in self.board

    def empty_squares(self):  
        return ' ' in self.board


class AI:
    def __init__(self, letter):
        self.letter = letter
        self.opponent = 'O' if letter == 'X' else 'X'
        self.nodes = 0

    def minimax(self, board, maximizing):
        self.nodes += 1
        result = self.check_terminal(board)
        if result is not None:
            return result

        if maximizing:
            best = -math.inf
            for move in self.available(board):
                board[move] = self.letter
                score = self.minimax(board, False)
                board[move] = ' '
                best = max(best, score)
            return best
        else:
            best = math.inf
            for move in self.available(board):
                board[move] = self.opponent
                score = self.minimax(board, True)
                board[move] = ' '
                best = min(best, score)
            return best

    def alpha_beta(self, board, maximizing, alpha, beta):
        self.nodes += 1
        result = self.check_terminal(board)
        if result is not None:
            return result

        if maximizing:
            best = -math.inf
            for move in self.available(board):
                board[move] = self.letter
                score = self.alpha_beta(board, False, alpha, beta)
                board[move] = ' '
                best = max(best, score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = math.inf
            for move in self.available(board):
                board[move] = self.opponent
                score = self.alpha_beta(board, True, alpha, beta)
                board[move] = ' '
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

    def get_move(self, board, use_alpha_beta=False):
        best_score = -math.inf
        best_move = None
        self.nodes = 0

        for move in self.available(board):
            board[move] = self.letter
            if use_alpha_beta:
                score = self.alpha_beta(board, False, -math.inf, math.inf)
            else:
                score = self.minimax(board, False)
            board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move

        return best_move, self.nodes

    def check_terminal(self, board):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in lines:
            if board[line[0]] == board[line[1]] == board[line[2]] != ' ':
                return 1 if board[line[0]] == self.letter else -1
        return 0 if ' ' not in board else None

    def available(self, board):
        return [i for i, v in enumerate(board) if v == ' ']


def play_game():
    print("Welcome to Tic-Tac-Toe!")
    algo = input("Choose AI algorithm (1 = Minimax, 2 = Alpha-Beta): ")

    ai_algo = False if algo == '1' else True
    game = Game()
    ai = AI('O')  # AI plays O, human is X

    game.display()

    while game.empty_squares():
        move = None
        while move not in game.available_moves():
            try:
                move = int(input("Your move (0–8): "))
            except:
                continue

        game.make_move(move, 'X')
        game.display()

        if game.current_winner:
            print("You win!")
            return

        if not game.empty_squares():
            print("It's a draw!")
            return

        print("AI is thinking...")
        ai_move, nodes = ai.get_move(game.board, use_alpha_beta=ai_algo)

        if ai_move is not None:
            game.make_move(ai_move, 'O')
            game.display()
            print(f"AI moved at position {ai_move} (nodes evaluated: {nodes})")

            if game.current_winner:
                print("AI (O) wins!")
                return
        else:
            print("It's a draw!")
            return

    print("It's a draw!")

if __name__ == "__main__":
    play_game()