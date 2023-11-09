from math import inf as infinite

class TicTacToe:
    def __init__(self):
        self.PLAYER = -1
        self.AI = +1
        self.matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.aiChosenValues = []
        self.playerChosenValues = []
        self.values_domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

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
        if self.is_winner(state, self.AI):
            score = +1
        elif self.is_winner(state, self.PLAYER):
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
        return self.is_winner(state, self.PLAYER) or self.is_winner(state, self.AI)

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

    def evaluate(self, state):
        return self.evaluate_board(state)

    def perform_minimax(self, state, depth, player):

            if player == self.AI:
                best = [-1, -1, -infinite]
            else:
                best = [-1, -1, infinite]

            if depth == 0 or self.is_game_over(state):
                score = self.evaluate(state)
                return [-1, -1, score]

            for cell in self.get_empty_cells(state):
                x, y = cell[0], cell[1]
                state[x][y] = player
                score = self.perform_minimax(state, depth - 1, -player)
                state[x][y] = 0
                score[0], score[1] = x, y

                if player == self.AI:
                    if best[2] <= score[2]:
                        best = score
                else:
                    if best[2] >= score[2]:
                        best = score

            return best

    def aiMove(self):
        depth = len(self.get_empty_cells(self.matrix))
        if depth == 0 or self.is_game_over(self.matrix):
            return
        print("\n------------------------------------------")
        print("AI'S TURN")
        move = self.perform_minimax(self.matrix, depth, self.AI)
        x, y = move[0], move[1]
        self.make_move(x, y, self.AI, self.matrix)
        print("AI chooses position: ", self.get_cell_value(x, y))
        self.aiChosenValues.append(self.get_cell_value(x, y))
        self.values_domain.remove(self.get_cell_value(x, y))

    def playerMove(self):
        depth = len(self.get_empty_cells(self.matrix))
        if depth == 0 or self.is_game_over(self.matrix):
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
        print("\nValues Left: ", self.values_domain)
        print("AI's Moves: ", self.aiChosenValues)
        print("Your Moves: ", self.playerChosenValues)
        print("\n------------------------------------------")
        while move < 1 or move > 9:
            move = int(input("Chose digits from 1 to 9 please: "))
            if move < 10 and move > 0:
                coord = moves[move]
                can_move = self.make_move(coord[0], coord[1], self.PLAYER, self.matrix)
                if not can_move:
                    print("Invalid move. Try again.")
                    move = -1
            else:
                print("Invalid choice. Try again.")
        self.playerChosenValues.append(self.get_cell_value(coord[0], coord[1]))
        self.values_domain.remove(move)

    def start_game(self):
        while len(self.get_empty_cells(self.matrix)) > 0 and not self.is_game_over(self.matrix):
            self.playerMove()
            self.aiMove()
        if self.is_winner(self.matrix, self.PLAYER):
            print("\nValues Left: ", self.values_domain)
            print("AI's Moves: ", self.aiChosenValues)
            print("Your Moves: ", self.playerChosenValues)
            print("CONGRATULATIONS! You win!")
        elif self.is_winner(self.matrix, self.AI):
            print("\nValues Left: ", self.values_domain)
            print("AI's Moves: ", self.aiChosenValues)
            print("Your Moves: ", self.playerChosenValues)
            print("YOU LOSE! Better luck next time.")
        else:
            print("\nValues Left: ", self.values_domain)
            print("AI's Moves: ", self.aiChosenValues)
            print("Your Moves: ", self.playerChosenValues)
            print("It's a DRAW! Good game!")

if __name__ == "__main__":
    tictactoe_game = TicTacToe()
    tictactoe_game.start_game()
