from collections import deque
import time
from queue import PriorityQueue
import numpy as np

class SolvePuzzle:
    def __init__(self,initial_state):
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
        initial_state_tuple = tuple(map(tuple, puzzle.initial_state))
        pq.put((heuristic(puzzle.initial_state), initial_state_tuple))
        visited = set()
        parent = {}
        while not pq.empty():
            _, state = pq.get()
            state_array = np.array(state)
            if puzzle.is_final(state_array):
              solution = [state_array]
              while not np.array_equal(state_array, puzzle.initial_state):
                state_array = parent[state_array]
                solution.insert(0, state_array)
              return solution
            visited.add(state)
            for neighbor in puzzle.get_neighbors(state_array):
                if neighbor is not None:
                    tuple_state = tuple(map(tuple, neighbor))
                    if tuple_state not in visited:
                     pq.put((heuristic(neighbor), tuple_state))
                     parent[tuple_state] = state_array
        return None

def IDDFS(puzzle, max_depth):
        def dls(node, depth):
            if depth == 0:
                return [node]
            for neighbor in puzzle.get_neighbors(node):
                if neighbor is not None:
                    path = dls(neighbor, depth - 1)
                    if path is not None:
                        return [node] + path
            return None

        for depth in range(max_depth + 1):
            solution = dls(puzzle.initial_state, depth)
            if solution is not None:
                return solution
        return None

def printState(self,state):
        for row in state:
                print(' '.join(map(str,row)))

if __name__ == '__main__':
    # Inițializați instanțele de puzzle și euristicile
    instances = [np.array([[8, 6, 7], [2, 5, 4], [0, 3, 1]]),
                 np.array([[2, 5, 3], [1, 0, 6], [4, 7, 8]]),
                 np.array([[8, 7, 1], [6, 0, 2], [5, 4, 3]])]

    heuristics = [manhattanDistance, hammingDistance, euclidDistance]

    for puzzle_instance in instances:
        puzzle = SolvePuzzle(puzzle_instance)
        for heuristic in heuristics:
            start_time = time.time()
            greedy_solution = Greedy(puzzle, heuristic)
            end_time = time.time()
            if greedy_solution:
                print(f'Greedy {heuristic.__name__} heuristic:')
                for state in greedy_solution:
                    print(state)
                print(f'Solution length: {len(greedy_solution) - 1}')
                print(f'Time: {end_time - start_time:.4f} seconds')
            # else:
            #     print(f'No solution {heuristic.__name__} heuristic.')

            start_time = time.time()
            iddfs_solution = IDDFS(puzzle, 31)  # 31 is the maximum depth for 8-puzzle
            end_time = time.time()
            if iddfs_solution:
                print('IDDFS solution:')
                for state in iddfs_solution:
                    print(state)
                print(f'Solution length: {len(iddfs_solution) - 1}')
                print(f'Time : {end_time - start_time:.4f} seconds')
            else:
                print('No solution found using IDDFS.')
            print('-' * 30)        