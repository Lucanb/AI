from collections import deque

class SolvePuzzle:
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

    def printState(self,state):
       for row in state:
            print(' '.join(map(str,row)))

if __name__ == '__main__':
    initial_state = [
        [2, 7, 5], 
        [0, 8, 4], 
        [3, 1, 6]
    ]

    puzzle = SolvePuzzle()
    result = puzzle.IDDFS(initial_state)

    if result:
        print("Soluție găsită:")
        puzzle.print_state(result)
    else:
        print("Nu există soluție.")        




                    