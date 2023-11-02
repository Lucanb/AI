import random

class SudokuSolver:
    def __init__(self, assignment):
        self.N = 9
        self.assignment = assignment

    def printRes(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.assignment[i][j], end=" ")
            print('\n')
        print('-------------------')
        print('\n')  

    def emptyColouredCells(self):
        variableList = []
        for row in range(self.N):
            for col in range(self.N):
                if self.assignment[row][col] == 0 or self.assignment[row][col] == -1:
                    variableList.append((row, col))
        return variableList

    def verifAtrib(self, row, col, num):
        if self.assignment[row][col] == -1:
            if num % 2 != 0:
                return False

        for i in range(self.N):
            if self.assignment[row][i] == num or self.assignment[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.assignment[start_row + i][start_col + j] == num:
                    return False

        return True

    def BktFC(self):
        if not self.emptyColouredCells():
            return True
        variableList = self.emptyColouredCells()
        for cell in variableList:
            row, col = cell
            if self.assignment[row][col] == 0:
                domain = list(range(1, 10))
                random.shuffle(domain)

                for num in domain:
                    if self.verifAtrib(row, col, num):
                        self.assignment[row][col] = num
                        self.printRes()
                        if self.BktFC():
                            return True
                        self.assignment[row][col] = 0
                return False

            elif self.assignment[row][col] == -1:
                domainp = list([2, 4, 6, 8])
                random.shuffle(domainp)

                for num in domainp:
                    if self.verifAtrib(row, col, num):
                        self.assignment[row][col] = num
                        self.printRes()
                        if self.BktFC():
                            return True
                        self.assignment[row][col] = -1

                return False
        return True

if __name__ == "__main__":
    assignment = [[8, 4, 0, 0, 5, 0, -1, 0, 0],
                  [3, 0, 0, 6, 0, 8, 0, 4, 0],
                  [0, 0, -1, 4, 0, 9, 0, 0, -1],
                  [0, 2, 3, 0, -1, 0, 9, 8, 0],
                  [1, 0, 0, -1, 0, -1, 0, 0, 4],
                  [0, 9, 8, 0, -1, 0, 1, 6, 0],
                  [-1, 0, 0, 5, 0, 3, -1, 0, 0],
                  [0, 3, 0, 1, 0, 6, 0, 0, 7],
                  [0, 0, -1, 0, 2, 0, 0, 1, 3]]

    solver = SudokuSolver(assignment)
    if solver.BktFC():
        print("Solutia Sudocu cu Forward Checking :")
        solver.printRes()
    else:
        print("Nu am gasit solutie")
