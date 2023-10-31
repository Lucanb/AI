
def completedMatrix(assignment):
    return all(all(cell != 0 for cell in row) for row in assignment)

def valid_row(assignment, row, domain_value):
    return domain_value not in assignment[row]

def valid_column(assignment,column,domain_value):
    return domain_value not in [assignment[i][column] for i in range(9)]

def valid_zone(assignment,row,column,value):
    row_k = 3 * (row // 3)
    column_k = 3 * (column // 3)
    for i in range(3):
        for j in range(3):
            if assignment[row_k + i][column_k + j] == value:
                return False
    return True 

def parity_position(assignment, row, col, value):
    return value % 2 == 0 and assignment[row][col] == -1

def consistentAssign(assignment, row, col, value, constraint_list):
    for func in constraint_list:
        if func == valid_column:
            if not func(assignment, col, value):
                return False
        elif func == valid_row:
            if not func(assignment, row, value):
                return False
        else:
            if not func(assignment, row, col, value):
                return False
    return True


def domainElement_Repartion(assignment):
  for i in range(9):
    for j in range(9):  
        if assignment[i][j] == 0 or assignment[i][j] == -1 :
            return i,j
  return None

def domainUpdate(domain_list,var,value):
    domain_llist = domain_list.copy()
    row,column = var
    for i in range(9):
        if i != column :
            domain_llist[(row,i)] = domain_llist[(row,i)] - {value}
        if i != row:
            domain_llist[(i,column)] = domain_llist[(i,column)] - {value}     
    row_k = 3 * (row // 3)
    column_k = 3 * (column // 3)
    for i in range(3):
        for j in range(3):
            r, c = row_k + i, column_k + j
            if (r, c) != var:
                domain_llist[(r, c)] = domain_llist[(r, c)] - {value}
    return domain_llist

def BKT_with_ForwardC(assignment,domain_list,constraint_functions):  
    if completedMatrix(assignment):
        return assignment
    location =   domainElement_Repartion(assignment)
    if location is None :
        return assignment
          
    row,column = location
    for element in  domain_list[location]:
        if consistentAssign(assignment,row,column,element,constraint_functions):
            assignment[row][column] = element
            domainUp = domainUpdate(domain_list,location,element)
            state = BKT_with_ForwardC(assignment,domainUp,constraint_functions)
            if state is not None:
              return state
            assignment[row][column] = 0
    return None

if __name__ == "__main__":
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, -1, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
  # Inițializarea domeniilor
    variables = [(i, j) for i in range(9) for j in range(9)]
    domains = {var: set(range(1, 10)) for var in variables}

    # Lista de funcții pentru restricții
    constraint_functions = [valid_row, valid_column, valid_zone, parity_position]

    result = BKT_with_ForwardC(puzzle, domains, constraint_functions)

    if result is not None:
        print("Soluția este:")
        print(result)
    else:
        print("Nu există soluție pentru acest puzzle.")
