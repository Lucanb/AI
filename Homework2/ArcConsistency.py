class SudokuSolverArcConsistency:
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

    def ArcConsistency(self):
        queue = []

        for row in range(self.N):
            for col in range(self.N):
                if self.assignment[row][col] == 0:
                    for i in range(self.N):
                        if i != col:
                            queue.append(((row, col), (row, i)))
                        if i != row:
                            queue.append(((row, col), (i, col)))
        
        while queue:
            (row1, col1), (row2, col2) = queue.pop(0)
            
            if self.revise(row1, col1, row2, col2):
                if self.assignment[row1][col1] == 0:
                    return False
                for i in range(self.N):
                    if i != col1 and self.assignment[row1][i] == 0:
                        queue.append(((row1, i), (row2, col2)))
                    if i != row1 and self.assignment[i][col1] == 0:
                        queue.append(((i, col1), (row2, col2)))
        
        return True

    def revise(self, row1, col1, row2, col2):
        revised = False
        domain1 = self.validValues(row1, col1)
        
        for value in self.validValues(row2, col2):
            if len(domain1) == 1 and value in domain1:
                self.assignment[row2][col2] = value
                revised = True
        
        return revised

    def validValues(self, row, col):
        domain = set(range(1, 10))
        for i in range(self.N):
            domain.discard(self.assignment[row][i])
            domain.discard(self.assignment[i][col])

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                domain.discard(self.assignment[start_row + i][start_col + j])

        return list(domain)

assignment = [[8, 4, 0, 0, 5, 0, 0, 0, 0],
             [3, 0, 0, 6, 0, 8, 0, 4, 0],
             [0, 0, 0, 4, 0, 9, 0, 0, 0],
             [0, 2, 3, 0, 0, 0, 9, 8, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 4],
             [0, 9, 8, 0, 0, 0, 1, 6, 0],
             [0, 0, 0, 5, 0, 3, 0, 0, 0],
             [0, 3, 0, 1, 0, 6, 0, 0, 7],
             [0, 0, 0, 0, 2, 0, 0, 1, 3]]

solver = SudokuSolverArcConsistency(assignment)
if solver.ArcConsistency():
    print("Solutia cu Arc Consistency Alg:")
    solver.assignment()
else:
    print("Nu am gasit solutie")
