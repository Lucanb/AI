import numpy as np
def Initialisation_State() :
    matrix = np.array([[2, 7, 5], [0, 8, 4], [3, 1, 6]])
    value = [1, 0]
    return matrix, value

def Final_State_Verif(matrix):
    values_matrix=[]
    for i in range(3):
       for j in range(3):
            if(matrix[i][j] != 0):  
               values_matrix.append(matrix[i][j])

    for i in range(1, len(values_matrix)):
       if values_matrix[i] < values_matrix[i - 1]:
            return False
    return True

def isInMAtrix(i,j):
   if i>=0 and i<3 and j>=0 and j<3 :
    return True
   else :
    return False
   
def Transition(matrix, values, next):
   if isInMAtrix(next[0], next[1]):
      const = matrix[next[0]][next[1]]
      LastNumber = matrix[next[0]][next[1]] 
      matrix[next[0]][next[1]] = matrix[values[0]][values[1]]
      matrix[values[0]][values[1]] = const
      return matrix, next, LastNumber
   else:
      return None, None
   
def Memorise_State(matrix,unique_matrices):

    if matrix.tobytes() in unique_matrices:
      return False
    else:
      return True 

def LastPosition(last_number,matrix,next):
   if matrix[next[0]][next[1]] == last_number:
      return False
   return True   

def get_distances(matrix,values):
   n_up = values[0] + 1  # urc pe linie
   next_1 = [n_up,values[1]]
   n_down = values[0] - 1 #cobor pe linie
   next_2 = [n_down,values[1]]
   n_left = values [1] - 1  #stanga
   next_3 = [values[0],n_left]
   n_right = values [1] +1  #dreapta
   next_4 = [values[0],n_right]
   # daca pozitia nu este valida voi da o distanta foarte mare care sa nu fie luata in calcul
   if(isInMAtrix(n_up,values[1])):
    distance1 = ((values[0]-n_up)**2 + values[1]**2)**1/2 
   else:
    distance1 = 1000000
   if(isInMAtrix(n_down,values[1])):
    distance2 = ((values[0]-n_down)**2 + values[1]**2)**1/2
   else:
    distance2 = 1000000
   if(isInMAtrix(values[0],n_left)):
    distance3 = (values[0]**2 + (n_left-values[1])**2)**1/2
   else:
    distance3 = 1000000
   if(isInMAtrix(values[0],n_right)):
    distance4 = (values[0]**2 + (n_right-values[1])**2)**1/2    
   else:
    distance4 = 1000000  
   #print([distance1,distance2, distance3,distance4],[next_1,next_2,next_3,next_4])
   return  [distance1,distance2, distance3,distance4],[next_1,next_2,next_3,next_4]

def IDDFS(unique_matrices, matrix, values, depth, maxDepth):
   LastNumber = 0
   if depth > maxDepth:
      return None
   if Final_State_Verif(matrix):
      return matrix
   distances, positions = get_distances(matrix, values)
   for position in positions:
      if (isInMAtrix(position[0], position[1]) and
          Memorise_State(matrix, unique_matrices) and
          LastPosition(LastNumber, matrix, position)):
         unique_matrices.add(matrix.tobytes())
         matrix, values, LastNumber = Transition(matrix, values, position)
         if matrix is not None and values is not None and LastNumber is not None:
            print(matrix)
            result = IDDFS(unique_matrices, matrix, values, depth + 1, maxDepth)
            if result is not None:
               return result
   return None

def DoIDDFS(matrix, values):
   unique_matrices = set()
   maxDepth = 0
   depth = 0
   while True:
      result = IDDFS(unique_matrices, matrix, values, depth, maxDepth)
      if result is not None:
         return result
      maxDepth += 1


def GreedyAlg():
   
   return




















if __name__ == '__main__':
    matrix,values = Initialisation_State() 

    solution = DoIDDFS(matrix,values)
    # Afișarea soluției
    if solution:
        print('Puzzle solved')
    else:
        print("Puzzle cannot be solved.")            
