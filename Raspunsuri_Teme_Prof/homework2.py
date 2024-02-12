class Cell:
    # Aceasta clasa reprezinta un element din matrice.
    # Salvam numarul pus pe acea pozitie, domeniul si pozitia numerelor
    # care au sters elemente din domeniu. Acest lucru ne va ajuta cand ne intoarcem inapoi
    # la Backtracking, sa putem schimba inapoi domeniul.
    def __init__(self, number):
        self.number = number
        self.domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        # Modified ne ajuta sa putem lucra cu acelasi state in algoritmul de backtracking, fara sa mai trebuiasca
        # facute copie la state de multe ori in algoritm
        self.modified = set()

    def remove_from_domain(self, *numbers):
        for number in numbers:
            if number in self.domain:
                self.domain.remove(number)

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return self.__str__()


class State:
    def __init__(self, table: list, even: list):
        self.table = []
        for row in table:
            row_table = []
            for element in row:
                cell = Cell(element)
                row_table.append(cell)
            self.table.append(row_table)
        for i, j in even:
            self.table[i][j].remove_from_domain(1, 3, 5, 7, 9)
        # Pentru numerele deja setate, vom merge la vecini lor si o sa le schimbam domeniul sa nu aibe numarul
        # deja pus in domeniu
        for i in range(9):
            for j in range(9):
                if self.table[i][j].number != 0:
                    self.change_neighbours_domain(i, j)

    # Functie folosita pentru a elimina un numar din domeniul veciniilor acelui numar
    def change_neighbours_domain(self, i, j):
        number = self.table[i][j].number
        for column_index in range(1, 9):  # coloane
            # Daca este deja setat, nu mai are rost sa modificam domeniul
            if self.table[i][(j + column_index) % 9].number == 0:
                # Daca numarul curent este in domeniul vecinului
                if number in self.table[i][(j + column_index) % 9].domain:
                    # Scoatem numarul curent din domeniu
                    self.table[i][(j + column_index) % 9].remove_from_domain(number)
                    # Adaugam pozitia numarului curent in modified de vecin.
                    self.table[i][(j + column_index) % 9].modified.add((i, j))
                    # Daca domeniul vecinului o devenit null, atunci returnam false (Forward Checking) si numarul curent in backtracking
                    # nu o fost o idee buna si nu vom continua cu el
                    if len(self.table[i][(j + column_index) % 9].domain) == 0:
                        return False
        for row_index in range(1, 9):  # linii
            if self.table[(i + row_index) % 9][j].number == 0:
                if number in self.table[(i + row_index) % 9][j].domain:
                    self.table[(i + row_index) % 9][j].remove_from_domain(number)
                    self.table[(i + row_index) % 9][j].modified.add((i, j))
                    if len(self.table[(i + row_index) % 9][j].domain) == 0:
                        return False
        start_row, start_col = 3 * (i // 3), 3 * (j // 3)
        for row_index in range(3):  # acelasi patrat
            for column_index in range(3):
                if self.table[row_index + start_row][column_index + start_col].number == 0:
                    if number in self.table[row_index + start_row][column_index + start_col].domain:
                        self.table[row_index + start_row][column_index + start_col].remove_from_domain(number)
                        self.table[row_index + start_row][column_index + start_col].modified.add((i, j))
                        if len(self.table[row_index + start_row][column_index + start_col].domain) == 0:
                            return False
        return True

    def revert_neighbours_domain(self, i, j):
        number = self.table[i][j].number
        for column_index in range(1, 9):
            # Verificam daca vecinul nu este deja setat
            if self.table[i][(j + column_index) % 9].number == 0:
                # Daca numarul curent este in modified de vecin atunci adaugam inapoi.
                # Folosim modified deoarece ste posibil ca vecinul curent sa aibe numarul curent
                # sters din domeniu, de un alt vecin al sau. Exemplu:
                # 0 5 0
                # 0 6 5 <- cel curent
                # In acest exemplu, daca eu ma intorc pe pozitia 1 2, adica la numarul 5 si vreau sa fac ca state-ul sa fie
                # inainte sa fi adaugat 5 acolo, trebuie sa merg pe vecinii sai si sa adaug 5 inapoi in domeniu dar este posibil
                # ca 5-ul din domeniul unui vecin sa fi scos din vina unui alt vecin al sau ca in exemplu
                if (i, j) in self.table[i][(j + column_index) % 9].modified:
                    self.table[i][(j + column_index) % 9].domain.add(number)
                    self.table[i][(j + column_index) % 9].modified.remove((i, j))
        for row_index in range(1, 9):
            if self.table[(i + row_index) % 9][j].number == 0:
                if (i, j) in self.table[(i + row_index) % 9][j].modified:
                    self.table[(i + row_index) % 9][j].domain.add(number)
                    self.table[(i + row_index) % 9][j].modified.remove((i, j))
        start_row, start_col = 3 * (i // 3), 3 * (j // 3)
        for row_index in range(3):
            for column_index in range(3):
                if self.table[row_index + start_row][column_index + start_col].number == 0:
                    if (i, j) in self.table[row_index + start_row][column_index + start_col].modified:
                        self.table[row_index + start_row][column_index + start_col].domain.add(number)
                        self.table[row_index + start_row][column_index + start_col].modified.remove((i, j))

    # Returneaza minimum remaining value
    def get_mrv(self):
        last = (-1, -1)
        mini = 10
        for i in range(9):
            for j in range(9):
                if self.table[i][j].number == 0:
                    if len(self.table[i][j].domain) < mini:
                        mini = len(self.table[i][j].domain)
                        last = (i, j)
        return last


# Arc Consistency, folosit inainte de algoritm pentru a face domeniile de start a celulelor mai mici
def ac_3(state: State):
    # Fac o lista cu fiecare combinatie de celule care sunt vecini
    queue = [((i, j), neighbour) for i in range(9) for j in range(9) for neighbour in get_neighbours(i, j)]

    while queue:
        x_i, x_j = queue.pop(0)
        # remove_inconsistent_values returneaza true daca exista cel putin un element din
        # domeniu care a fost sters deoarece in celula x_j nu am fi avut ce pune pentru a
        # satisface regulile jocului
        if remove_inconsistent_values(state, x_i, x_j):
            for x_k in get_neighbours(x_i[0], x_i[1]):
                queue.append((x_k, x_i))


# Cauta pentru fiecare valoare din domeniul celulei x_i daca celula x_j are cel putin o valoare care satisface regulile jocului
def remove_inconsistent_values(state: State, x_i, x_j):
    removed = False
    to_delete = []
    for x in state.table[x_i[0]][x_i[1]].domain:
        any = False
        for y in state.table[x_j[0]][x_j[1]].domain:
            if x != y:
                any = True
        if not any:
            to_delete.append(x)
            removed = True

    if removed:
        for x in to_delete:
            state.table[x_i[0]][x_i[1]].domain.remove(x)

    return removed


# Returneaza vecinii unei celule
def get_neighbours(row_index, column_index):
    neighbours = []
    for i in range(1, 9):  # Linii si coloane
        neighbours.append((row_index, (column_index + i) % 9))
        neighbours.append(((row_index + i) % 9, column_index))
    start_row, start_col = 3 * (row_index // 3), 3 * (column_index // 3)
    for i in range(0, 3):  # Acelasi patrat
        for j in range(0, 3):
            if start_row + i == row_index and start_col + j == column_index:
                continue
            neighbours.append((start_row + i, start_col + j))

    return neighbours


# Algoritmul in sine care este recursiv si se foloseste de toate functiile de pana acum
def forward_checking_find_solution(state: State):
    i, j = state.get_mrv()  # Luam cell-ul (patratica) cu cel mai putine numere in domeniu

    if (i, j) == (-1, -1):  # Daca am primit -1, -1 inseamna ca toate celulele au un numar in ele adica am gasit solutia
        return True

    for number in state.table[i][j].domain:  # Luam fiecare numar din domeniul curent
        state.table[i][j].number = number  # Punem in celula, numarul din domeniu

        # Daca change_neighbours_domain ne-a returnat false, nu vom continua cu acest numar. (Forward Checking)
        # Aceasta functie schimba domeniul veciniilor (sterge daca au in domeniu numarul pus) si daca domeniul devine null returneaza false.
        # Nu ar mai avea logica sa continuam deoarece nu am avea ce pune mai tarziu pe pozitia acelui vecin care domeniu a devenit null
        if state.change_neighbours_domain(i, j) and forward_checking_find_solution(state):  # Apelam recursiv functia
            return True

        # Daca am ajuns aicea inseamna ca numarul ales nu o fost o alegere buna si
        # Vom da revert la domeniul veciniilor sai, ca sa ajungem in starea in care am fost si inainte
        state.revert_neighbours_domain(i, j)
        state.table[i][j].number = 0

    return False


start_state = State([
    [8, 4, 0, 0, 5, 0, 0, 0, 0],
    [3, 0, 0, 6, 0, 8, 0, 4, 0],
    [0, 0, 0, 4, 0, 9, 0, 0, 0],
    [0, 2, 3, 0, 0, 0, 9, 8, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 9, 8, 0, 0, 0, 1, 6, 0],
    [0, 0, 0, 5, 0, 3, 0, 0, 0],
    [0, 3, 0, 1, 0, 6, 0, 0, 7],
    [0, 0, 0, 0, 2, 0, 0, 1, 3]],
    [(0, 6), (2, 2), (2, 8), (3, 4), (4, 3), (4, 5), (5, 4), (6, 0), (6, 6), (8, 2)])

ac_3(start_state)
if not forward_checking_find_solution(start_state):
    print("Solution not found!")
else:
    for i in range(9):
        print(start_state.table[i])
