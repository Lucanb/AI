import random

class NumberScrabble:
    def __init__(self):
        self.state = []  # Inițial niciun număr nu este ales
        self.current_player = 0  # Jucătorul curent (0 pentru A, 1 pentru B)

    def is_game_over(self):
        # Verificăm dacă jocul s-a încheiat (nu mai pot fi alese numere)
        return len(self.state) == 9

    def is_winner(self, player):
        # Verificăm dac un jucător a câștigat (suma numerelor alese este 15)
        for i in range(len(self.state)):
            for j in range(i + 1, len(self.state)):
                for k in range(j + 1, len(self.state)):
                    if (
                        self.state[i] + self.state[j] + self.state[k] == 15
                        and player == self.current_player
                    ):
                        return True
        return False

    def make_move(self, number):
        if number in self.state:
            print("Numărul a fost deja ales.")
            return False
        if not (1 <= number <= 9):
            print("Numărul trebuie să fie între 1 și 9.")
            return False
        if self.is_game_over():
            print("Jocul s-a încheiat cu remiză.")
            return False

        self.state.append(number)
        if self.is_winner(self.current_player):
            self.display_board()
            print(f"Jucătorul {self.current_player} a câștigat!")
            return True

        self.current_player = 1 - self.current_player  # Schimbăm jucătorul curent
        return True

    def display_board(self):
        print("Starea jocului:")
        for i in range(1, 10):
            if i in self.state:
                print("X", end=" ")
            else:
                print(i, end=" ")
            if i % 3 == 0:
                print()

    def minimax(self, depth, is_maximizing):
        if self.is_winner(0):
            return -1
        if self.is_winner(1):
            return 1
        if self.is_game_over():
            return 0

        if is_maximizing:
            max_eval = -float("inf")
            for number in range(1, 10):
                if number not in self.state:
                    self.state.append(number)
                    eval = self.minimax(depth + 1, False)
                    self.state.remove(number)
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for number in range(1, 10):
                if number not in self.state:
                    self.state.append(number)
                    eval = self.minimax(depth + 1, True)
                    self.state.remove(number)
                    min_eval = min(min_eval, eval)
            return min_eval

    def best_move(self):
        best_eval = -float("inf")
        best_move = None
        for number in range(1, 10):
            if number not in self.state:
                self.state.append(number)
                eval = self.minimax(0, False)
                self.state.remove(number)
                if eval > best_eval:
                    best_eval = eval
                    best_move = number
        return best_move

    def play(self):
        while not self.is_game_over():
            self.display_board()
            player = "A" if self.current_player == 0 else "B"
            if player == "A":
                number = int(input(f"Jucător {player}, alege un număr: "))
            else:
                number = self.best_move()
                print(f"Calculatorul a ales numărul {number}.")
            if self.make_move(number):
                break
        if not self.is_winner(0) and not self.is_winner(1):
            print("Jocul s-a încheiat cu remiză.")

if __name__ == "__main__":
    game = NumberScrabble()
    game.play()
