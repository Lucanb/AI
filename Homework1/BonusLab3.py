import time
from queue import PriorityQueue
import numpy as np

class SolvePuzzle:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def Verif(self,state):
      values_matrix=[]
      for i in range(3):
       for j in range(3):
            if(state[i][j] != 0):  
               values_matrix.append(state[i][j])

      for i in range(1, len(values_matrix)):
       if values_matrix[i] < values_matrix[i - 1]:
            return False
      return True 

    def posNeigbourhood(self,state):
       neighbours = []
       row,col = None,None

       for i in range(3):
          for j in range(3):
           if state[i][j] == 0:
              row,col=i,j
       vec = [(0,1),(0,-1),(1,0),(-1,0)]
       for l,p in vec:
                 newRow = row + l
                 newCol = col + p
                 if 0<=newRow and newRow < 3 and newCol>=0  and newCol < 3:
                    newState = [row[:] for row in state]
                    newState[row][col],newState[newRow][newCol]=newState[newRow][newCol],newState[row][col]
                    neighbours.append(newState)

       return neighbours

def manhattanDistance(state):
       normalAranj = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
       distance = 0
       for i in range(3):
          for j in range(3):
             if state[i][j] != 0:
                row,col = np.where(normalAranj == state[i][j]) 
                distance += abs(i-row[0]) + abs(j-col[0])
       return distance

def a_star(puzzle, heuristic):
    def reconstruct_path(currentState, father):
        path = [currentState]
        while currentState in father:
            currentState = father[currentState]
            path.insert(0, currentState)
        return path

    father_vec = {}
    d = {}
    f = {}
    initialStateHash = puzzle.initial_state.tobytes()
    d[initialStateHash] = 0
    f[initialStateHash] = heuristic(puzzle.initial_state)
    pq = PriorityQueue()
    pq.put((f[initialStateHash], initialStateHash))

    while not pq.empty():
        _, state_bytes = pq.get()
        state = np.frombuffer(state_bytes)
        state_bytes = state.tobytes()
        if puzzle.Verif(state):
            return reconstruct_path(state_bytes, father_vec)
        for neighbor in puzzle.posNeigbourhood(state):
            neighbor_bytes = neighbor.tobytes()
            tentative_g = d[state_bytes] + 1
            if neighbor_bytes not in d or tentative_g < d[neighbor_bytes]:
                father_vec[neighbor_bytes] = state_bytes
                d[neighbor_bytes] = tentative_g
                f[neighbor_bytes] = tentative_g + heuristic(neighbor)
                pq.put((f[neighbor_bytes], neighbor_bytes))
    return None

if __name__ == '__main__':
    instances = [np.array([[2, 7, 5], [0, 8, 4], [3, 1, 6]]),
                 np.array([[5, 2, 8], [4, 1, 7], [0, 3, 6]]),
                 np.array([[8, 7, 1], [6, 0, 2], [5, 4, 3]])]

    heuristics = [manhattanDistance]

    for puzzle_instance in instances:
        puzzle = SolvePuzzle(puzzle_instance)
        for heuristic in heuristics:
            start_time = time.time()
            a_star_solution = a_star(puzzle, heuristic)
            end_time = time.time()
            if a_star_solution:
                print(heuristic.__name__)
                for state in a_star_solution:
                    print(np.frombuffer(state))
                print(len(a_star_solution))
                print(end_time - start_time)
