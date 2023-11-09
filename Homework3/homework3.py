from math import inf as infinite

class TicTacToe:
    def __init__(self):
        self.HUMAN_PLAYER = -1
        self.COMPUTER_PLAYER = +1
        self.game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.computer_moves = []
        self.human_moves = []
        self.remaining_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def get_cell_value(self, x, y):
        if x == 0 and y == 0:
            return 2
        elif x == 0 and y == 1:
            return 7
        elif x == 0 and y == 2:
            return 6
        elif x == 1 and y == 0:
            return 9
        elif x == 1 and y == 1:
            return 5
        elif x == 1 and y == 2:
            return 1
        elif x == 2 and y == 0:
            return 4
        elif x == 2 and y == 1:
            return 3
        elif x == 2 and y == 2:
            return 8

    def evaluate_board(self, state):
        if self.is_winner(state, self.COMPUTER_PLAYER):
            score = +1
        elif self.is_winner(state, self.HUMAN_PLAYER):
            score = -1
        else:
            score = 0

        return score

    def is_winner(self, state, player):
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def is_game_over(self, state):
        return self.is_winner(state, self.HUMAN_PLAYER) or self.is_winner(state, self.COMPUTER_PLAYER)

    def get_empty_cells(self, state):
        cells = []
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])

        return cells

    def is_valid_move(self, x, y, state):
        if [x, y] in self.get_empty_cells(state):
            return True
        else:
            return False

    def make_move(self, x, y, player, state):
        if self.is_valid_move(x, y, state):
            state[x][y] = player
            return True
        else:
            return False

    def perform_minimax(self, state, depth, player):
        if player == self.COMPUTER_PLAYER:
            best = [-1, -1, -infinite]
        else:
            best = [-1, -1, infinite]

        if depth == 0 or self.is_game_over(state):
            score = self.evaluate_board(state)
            return [-1, -1, score]

        for cell in self.get_empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.perform_minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == self.COMPUTER_PLAYER:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score

        return best

    def computer_move(self):
        depth = len(self.get_empty_cells(self.game_board))
        if depth == 0 or self.is_game_over(self.game_board):
            return
        print("\n------------------------------------------")
        print("AI'S TURN")
        move = self.perform_minimax(self.game_board, depth, self.COMPUTER_PLAYER)
        x, y = move[0], move[1]
        self.make_move(x, y, self.COMPUTER_PLAYER, self.game_board)
        print("AI chooses position: ", self.get_cell_value(x, y))
        self.computer_moves.append(self.get_cell_value(x, y))
        self.remaining_values.remove(self.get_cell_value(x, y))

    def human_move(self):
        depth = len(self.get_empty_cells(self.game_board))
        if depth == 0 or self.is_game_over(self.game_board):
            return
        move = -1
        moves = {
            2: [0, 0],
            7: [0, 1],
            6: [0, 2],
            9: [1, 0],
            5: [1, 1],
            1: [1, 2],
            4: [2, 0],
            3: [2, 1],
            8: [2, 2],
        }
        print("\n------------------------------------------")
        print("Your TURN")
        print("\nValues Left: ", self.remaining_values)
        print("AI's Moves: ", self.computer_moves)
        print("Your Moves: ", self.human_moves)
        print("\n------------------------------------------")
        while move < 1 or move > 9:
            move = int(input("Chose digits from 1 to 9 please: "))
            if move < 10 and move > 0:
                coord = moves[move]
                can_move = self.make_move(coord[0], coord[1], self.HUMAN_PLAYER, self.game_board)
                if not can_move:
                    print("Invalid move. Try again.")
                    move = -1
            else:
                print("Invalid choice. Try again.")
        self.human_moves.append(self.get_cell_value(coord[0], coord[1]))
        self.remaining_values.remove(move)

    def start_game(self):
        while len(self.get_empty_cells(self.game_board)) > 0 and not self.is_game_over(self.game_board):
            self.human_move()
            self.computer_move()
        if self.is_winner(self.game_board, self.HUMAN_PLAYER):
            print("\nValues Left: ", self.remaining_values)
            print("AI's Moves: ", self.computer_moves)
            print("Your Moves: ", self.human_moves)
            print("CONGRATULATIONS! You win!")
        elif self.is_winner(self.game_board, self.COMPUTER_PLAYER):
            print("\nValues Left: ", self.remaining_values)
            print("AI's Moves: ", self.computer_moves)
            print("Your Moves: ", self.human_moves)
            print("YOU LOSE! Better luck next time.")
        else:
            print("\nValues Left: ", self.remaining_values)
            print("AI's Moves: ", self.computer_moves)
            print("Your Moves: ", self.human_moves)
            print("It's a DRAW! Good game!")

if __name__ == "__main__":
    tictactoe_game = TicTacToe()
    tictactoe_game.start_game()
