import numpy as np
import random
#  Avem o matrice 3x3 cu 8 dintre celule numerotate de la 1 la 8 și una goală. 
# Știind că poziția inițială a celulelor este aleatoare și că putem muta o 
# celulă doar în locul celulei goale și doar dacă este adiacentă acesteia, 
# să se găsească, dacă există, o secvență de mutări ale celulelor astfel 
# încât toate să fie plasate în ordine crescătoare în matrice. După mutarea unei
# celule, ea nu mai poate fi mutată din nou decât după ce unul din vecinii săi a fost mutat. 
# Poziția celulei goale nu contează pentru validarea stării finale.


# 1.Reprezentarea   : Matrice cu valori(locul liber va avea valoarea 0) -- memorarea este la fel ca la vector si ar fi O(n),n = nr-ul de valori --> 8 cazul nostru (si valorile sunt unice 0 - 8 ) 
# + indicele in care se afla 0 pentru a nu face cautarea in fiecare tranzitie
# 2.Starea Initiala : Matrice cu valori dispuse dupa datele de intrare ()
#   Starea Finala   : Matrice care are valorile ordonate in felul urmator (#3*i+j+1 == valoarea) pentru toate valorile din matrice si valoarea 0 se afla pe pozitia 9

def Initialisation_State() :
    value = [0, 0]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(values)
    matrix = [[values[0], values[1], values[2]], [values[3], values[4], values[5]], [values[6], values[7], values[8]]]
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == 0:
                value = [i, j]
                break
    return matrix, value

def Final_State_Verif(matrix):

    for i in range(3):
       for j in range(3):
            if(matrix[i][j] != 3*i +j+1):  
             return False
    return True

# 3. Tranzitia este reprezentata de o actiune de schimb intre valoriile de pe pozitia in care am valoarea 0 si un vecin (up,down,left,rights)
# Ca parametrii vom avea locatiile in care se pot face aceste schimbari(interiorul matricii) (am pozitia lui 0,am si vecinii lui), pot sa mai adaug si o distanta dupa care sa fa decizia 
def isInMAtrix(i,j):
   if i>=0 and i<3 and j>=0 and j<3 :
    return True
   else :
    return False

def get_distances(matrix,values):
   n_up = values[0] + 1
   next_1 = [n_up,values[1]]
   n_down = values[0] - 1
   next_2 = [n_down,values[1]]
   n_left = values [1] - 1
   next_3 = [values[0],n_left]
   n_right = values [1] +1
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
   return  [distance1,distance2, distance3,distance4],[next_1,next_2,next_3,next_4]

def getMinimum_distance(matrix,values):   #asta e in cazul unei abordari greedy (iau cea mai buna distanta)
   distances,positions = get_distances(matrix,values)
   return min(distances),positions[distances.index(min(values))]   

def Transition(matrix,values,next):
   if(isInMAtrix(next[0],next[1])):
    const = matrix[next[0]][next[1]] 
    matrix[next[0]][next[1]] = matrix[values[0]][values[1]]
    matrix[values[0]][values[1]] = const
    values=next 
    return matrix,values
   else:
    return None,None 
   
def Heuristic(matrix,values):  
   n_up = values[0] + 1
   n_down = values[0] - 1
   n_left = values [1] - 1
   n_right = values [1] + 1
   distances,positions = get_distances(matrix,values)
  # best_distance,next = getMinimum_distance(matrix,values)
  # fac o alegere arbitrara
   move = random.randint(0, 3)
   if(isInMAtrix(positions[0]) and move == 0):
    Transition(matrix,values,positions[0])
   if(isInMAtrix(positions[1]) and move == 1):
    Transition(matrix,values,positions[1])
   if(isInMAtrix(positions[2]) and move == 2):
    Transition(matrix,values,positions[2])   
   if(isInMAtrix(positions[3]) and move == 3):
    Transition(matrix,values,positions[3])

#Pt un greedy
    # const = matrix[next[0],next[1]] 
    # matrix[next[0],next[1]] = matrix[values[0],values[1]]
    # matrix[values[0],values[1]] = const  

    return matrix,values

#4. Strategia IDFS : Se alege in mod iterativ cate o adancime maxima si se exploreaza vecinii pana la acea adancime. Daca am dat peste o solutie,algorithmul se incheie.

def IDDFS(matrix,values,depth,maxDepth):
        if depth > maxDepth:
            return None
        if(Final_State_Verif(matrix)) :
            return matrix
        distances,positions = get_distances(matrix,values)
        for position in positions:
           if isInMAtrix(position[0],position[1]):
            matrix,values = Transition(matrix,values,position)
            if matrix is not None and values is not None:  
                 result = IDDFS(matrix,values, depth + 1, maxDepth)
            else:
                return 
        return None   

def Solve_IDDFS(matrix,values):
        
        maxDepth = 0
        depth = 0
        while True :
          result = IDDFS(matrix,values,depth,maxDepth)
          if result is not None :
            return result
          maxDepth += 1 

if __name__ == '__main__':
    matrix,values = Initialisation_State() 
    solution = Solve_IDDFS(matrix,values)

    # Afișarea soluției
    if solution:
        print('Puzzle solved')
    else:
        print("Puzzle cannot be solved.")