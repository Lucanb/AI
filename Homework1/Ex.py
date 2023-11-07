import math
import time


def initialize(input_array):
    return input_array.copy() + [-1]


def is_final(state) -> bool:
    length = len(state)

    for index in range(0, length - 2):
        if state[index] == 0:
            continue
        else:
            if state[index + 1] == 0 and index + 2 < length - 1:
                if state[index] >= state[index + 2]:
                    return False
            elif state[index + 1] != 0:
                if state[index] >= state[index + 1]:
                    return False
    return True


def is_final2(state) -> bool:
    length = len(state)
    if state[-2] != 0:
        return False

    for index in range(0, length - 3):
        if state[index] >= state[index + 1]:
            return False
    return True


def transition_up(state, col0, row0):
    state[-1] = state[row0 * 3 + col0] = state[(row0 - 1) * 3 + col0]
    state[(row0 - 1) * 3 + col0] = 0

    # print("up", state)
    return state


def transition_down(state, col0, row0):
    state[-1] = state[row0 * 3 + col0] = state[(row0 + 1) * 3 + col0]
    state[(row0 + 1) * 3 + col0] = 0

    # print("down", state)
    return state


def transition_left(state, col0, row0):
    state[-1] = state[row0 * 3 + col0] = state[row0 * 3 + col0 - 1]
    state[row0 * 3 + col0 - 1] = 0

    # print("left", state)
    return state


def transition_right(state, col0, row0):
    state[-1] = state[row0 * 3 + col0] = state[row0 * 3 + col0 + 1]
    state[row0 * 3 + col0 + 1] = 0

    # print("right", state)
    return state


def validate_transition_up(state, col0, row0):
    if row0 - 1 >= 0 and state[-1] != state[(row0 - 1) * 3 + col0]:
        return True
    else:
        return False


def validate_transition_down(state, col0, row0):
    if row0 + 1 < 3 and state[-1] != state[(row0 + 1) * 3 + col0]:
        return True
    else:
        return False


def validate_transition_left(state, col0, row0):
    if col0 - 1 >= 0 and state[-1] != state[row0 * 3 + col0 - 1]:
        return True
    else:
        return False


def validate_transition_right(state, col0, row0):
    if col0 + 1 < 3 and state[-1] != state[row0 * 3 + col0 + 1]:
        return True
    else:
        return False


def dls(state, current_depth, solution) -> bool:
    poz0 = state.index(0)
    col0 = poz0 % 3
    row0 = poz0 // 3

    if is_final(state):
        return True

    if current_depth <= 0:
        return False

    if validate_transition_up(state, col0, row0):
        next_transition = transition_up(state.copy(), col0, row0)
        solution += [next_transition]
        if dls(next_transition, current_depth - 1, solution):
            return True
        solution.remove(next_transition)

    if validate_transition_down(state, col0, row0):
        next_transition = transition_down(state.copy(), col0, row0)
        solution += [next_transition]
        if dls(next_transition, current_depth - 1, solution):
            return True
        solution.remove(next_transition)

    if validate_transition_left(state, col0, row0):
        next_transition = transition_left(state.copy(), col0, row0)
        solution += [next_transition]
        if dls(next_transition, current_depth - 1, solution):
            return True
        solution.remove(next_transition)

    if validate_transition_right(state, col0, row0):
        next_transition = transition_right(state.copy(), col0, row0)
        solution += [next_transition]
        if dls(next_transition, current_depth - 1, solution):
            return True
        solution.remove(next_transition)

    return False


def iddfs(state, max_depth, solution) -> bool:
    for i in range(max_depth):
        solution.clear()
        solution += [state]
        if dls(state, i, solution):
            return True
    return False


def hamming_dist(state, poz0) -> int:
    score = 0

    for i in range(0, poz0):
        if state[i] != i + 1 and state[i] != 0:
            score += 1

    if state[poz0] != 0:
        score += 1

    for i in range(poz0 + 1, len(state) - 2):
        if state[i] != i and state[i] != 0:
            score += 1

    return score


def hamming(state) -> int:
    min_score = hamming_dist(state, 0)
    for poz0 in range(1, 9):
        score = hamming_dist(state, poz0)
        if score < min_score:
            min_score = score
    return min_score


def manhattan_dist(state, poz0) -> int:
    score = 0

    for i in range(0, poz0):
        if state[i] != i + 1 and state[i] != 0:
            score += (abs(i // 3 - (state[i] - 1 * int(state[i] <= poz0)) // 3) +
                      abs(i % 3 - (state[i] - 1 * int(state[i] <= poz0)) % 3))

    if state[poz0] != 0:
        score += (abs(poz0 // 3 - (state[poz0] - 1 * int(state[poz0] <= poz0)) // 3) +
                  abs(poz0 % 3 - (state[poz0] - 1 * int(state[poz0] <= poz0)) % 3))

    for i in range(poz0 + 1, len(state) - 1):
        if state[i] != i and state[i] != 0:
            score += (abs(i // 3 - (state[i] - 1 * int(state[i] <= poz0)) // 3) +
                      abs(i % 3 - (state[i] - 1 * int(state[i] <= poz0)) % 3))

    return score


def manhattan(state) -> int:
    min_score = manhattan_dist(state, 0)
    for poz0 in range(1, 9):
        score = manhattan_dist(state, poz0)
        if score < min_score:
            min_score = score
    return min_score


def euclid_dist(state, poz0) -> int:
    score = 0

    for i in range(0, poz0):
        if state[i] != i + 1 and state[i] != 0:
            score += math.sqrt((i // 3 - (state[i] - 1 * int(state[i] <= poz0)) // 3) ** 2 +
                               (i % 3 - (state[i] - 1 * int(state[i] <= poz0)) % 3) ** 2)

    if state[poz0] != 0:
        score += math.sqrt((poz0 // 3 - (state[poz0] - 1 * int(state[poz0] <= poz0)) // 3) ** 2 +
                           (poz0 % 3 - (state[poz0] - 1 * int(state[poz0] <= poz0)) % 3) ** 2)

    for i in range(poz0 + 1, len(state) - 1):
        if state[i] != i and state[i] != 0:
            score += math.sqrt((i // 3 - (state[i] - 1 * int(state[i] <= poz0)) // 3) ** 2 +
                               (i % 3 - (state[i] - 1 * int(state[i] <= poz0)) % 3) ** 2)

    return score


def euclid(state) -> int:
    min_score = euclid_dist(state, 0)
    for poz0 in range(1, 9):
        score = euclid_dist(state, poz0)
        if score < min_score:
            min_score = score
    return min_score


def greedy(state, heuristic, solution) -> bool:
    solution += [state]

    while not is_final(state):
        poz0 = state.index(0)
        col0 = poz0 % 3
        row0 = poz0 // 3

        available_transitions = []

        if validate_transition_up(state, col0, row0):
            next_transition = transition_up(state.copy(), col0, row0)
            score = heuristic(next_transition)
            available_transitions += [(next_transition, score)]

        if validate_transition_down(state, col0, row0):
            next_transition = transition_down(state.copy(), col0, row0)
            score = heuristic(next_transition)
            available_transitions += [(next_transition, score)]

        if validate_transition_left(state, col0, row0):
            next_transition = transition_left(state.copy(), col0, row0)
            score = heuristic(next_transition)
            available_transitions += [(next_transition, score)]

        if validate_transition_right(state, col0, row0):
            next_transition = transition_right(state.copy(), col0, row0)
            score = heuristic(next_transition)
            available_transitions += [(next_transition, score)]

        if len(available_transitions) == 0:
            return False

        available_transitions = sorted(available_transitions, reverse=True, key=lambda a: a[1])

        best_transition = available_transitions.pop()[0]

        while best_transition in solution and len(available_transitions) > 0:
            best_transition = available_transitions.pop()[0]

        # print(best_transition)

        if best_transition in solution:
            return False

        state = best_transition

        solution += [best_transition]

    return True


def main():
    inputs = [[2, 5, 3, 1, 0, 6, 4, 7, 8], [2, 7, 5, 0, 8, 4, 3, 1, 6], [8, 6, 7, 2, 5, 4, 0, 3, 1]]

    for _input in inputs:
        print("\n\nINPUT: ", _input)

        for heuristic in [hamming, manhattan, euclid]:
            print(f"\nGreedy utilizand euristica {heuristic.__name__}")

            solution = []
            start_time = time.time()
            res_heuristic = greedy(initialize(_input), heuristic, solution)
            end_time = time.time()

            if res_heuristic:
                print(f"A fost gasita solutia de lungime {len(solution)} in {end_time - start_time}: \n", solution)
            else:
                print(f"Nu a fost gasita solutia. Executia algoritmului a durat {end_time - start_time}")

        print("\nIDDFS")

        solution = []
        start_time = time.time()
        res_iddfs = iddfs(initialize(_input), 30, solution)
        end_time = time.time()

        if res_iddfs:
            print(f"A fost gasita solutia de lungime {len(solution)} in {end_time - start_time}: \n", solution)
        else:
            print(f"Nu a fost gasita nici o solutie pana la adancimea 30. "
                  f"Executia algoritmului a durat {end_time - start_time}")


main()