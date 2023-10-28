from collections import deque
import time
from queue import PriorityQueue
import numpy as np

class SolvePuzzle2:
    def __init__(self):
        self.initial_state = None
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

    def IDDFS(self,initialState):
      self.initial_state = initialState
      DepthMax = 0
      while True:
          visited = set()     
          stack = deque([(self.initial_state,0)])

          while stack:
             state,depth = stack.pop()
             visited.add(str(state))
             print(state)
             if self.Verif(state):
                  return state
             if depth < DepthMax:
                for position in self.posNeigbourhood(state):
                   if str(position) not in visited:
                      stack.append((position,depth + 1)) 
          DepthMax += 1
       
class SolvePuzzle3:
    def __init__(self,initial_state):
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
    
    @staticmethod
    def posNeigbourhood(state):
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
            
def hammingDistance(state):
        normalAranj = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        return np.sum(state != normalAranj) - 1 


def euclidDistance(state):    
       normalAranj = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
       distance = 0
       for i in range(3):
         for j in range(3):
            if state[i][j] != 0:
                row, col = np.where(normalAranj == state[i][j])
                distance += np.sqrt((i - row[0]) ** 2 + (j - col[0]) ** 2)
       return distance   

def Greedy(puzzle,heuristic):
        pq = PriorityQueue()
        initialStates = tuple(map(tuple, puzzle.initial_state))
        pq.put((heuristic(puzzle.initial_state), initialStates))
        visited = set()
        parent = {}
        while not pq.empty():
            _, state = pq.get()
            stateArray = np.array(state)
            if puzzle.Verif(stateArray):
              sol = [stateArray]
              while not np.array_equal(stateArray, puzzle.initial_state):
                stateArray = parent[stateArray]
                sol.insert(0, stateArray)
              return sol
            visited.add(state)
            for neighbor in puzzle.posNeigbourhood(stateArray):
                if neighbor is not None:
                    tupleState = tuple(map(tuple, neighbor))
                    if tupleState not in visited:
                     pq.put((heuristic(neighbor), tupleState))
                     parent[tupleState] = stateArray
        return None

def IDDFS(puzzle, max_depth):
        def road(node, depth):
            if depth == 0:
                return [node]
            for neighbor in puzzle.posNeigbourhood(node):
                if neighbor is not None:
                    path = road(neighbor, depth - 1)
                    if path is not None:
                        return [node] + path
            return None

        for depth in range(max_depth + 1):
            solution = road(puzzle.initial_state, depth)
            if solution is not None:
                return solution
        return None

if __name__ == '__main__':

    initial_state = [
        [2, 7, 5], 
        [0, 8, 4], 
        [3, 1, 6]
    ]

    puzzle = SolvePuzzle2()
    result = puzzle.IDDFS(initial_state)

    if result:
        print(result)
    else:
        print("Failure") 


    instances = [np.array([[8, 6, 7], [2, 5, 4], [0, 3, 1]]),
                 np.array([[2, 5, 3], [1, 0, 6], [4, 7, 8]]),
                 np.array([[8, 7, 1], [6, 0, 2], [5, 4, 3]])]

    heuristics = [manhattanDistance, hammingDistance, euclidDistance]

    for instances in instances:
        puzzle = SolvePuzzle3(instances)
        for heuristic in heuristics:
            start = time.time()
            greedy_solution = Greedy(puzzle, heuristic)
            timeout = time.time()
            if greedy_solution:
                print(heuristic.__name__)
                for state in greedy_solution:
                    print(state)
                print(len(greedy_solution) - 1)
                print(timeout - start)

            start = time.time()
            iddfs_solution = IDDFS(puzzle, 31)
            timeout = time.time()
            if iddfs_solution:
                print('IDDFS solution:')
                for state in iddfs_solution:
                    print(state)
                print(len(iddfs_solution) - 1)
                print(timeout - start)     