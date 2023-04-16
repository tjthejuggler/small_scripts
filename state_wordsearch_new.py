import time
from ortools.sat.python import cp_model
from itertools import product

from collections import defaultdict
from termcolor import colored

# states = [
#     "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
#     "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
#     "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
#     "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
#     "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
# ]




def print_colored_puzzle(puzzle, overlaps):
    colors = ['white', 'green', 'yellow', 'red', 'blue', 'magenta', 'cyan']

    for row, overlap_row in zip(puzzle, overlaps):
        for cell, overlap in zip(row, overlap_row):
            color = colors[min(overlap, len(colors) - 1)]
            print(colored(cell, color), end=' ')
        print()

class ProgressPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, state_positions):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.state_positions = state_positions
        self.start_time = time.time()
        self.solution_count = 0

    def on_solution_callback(self):
        self.solution_count += 1
        print(f"Time: {time.time() - self.start_time:.2f}s | Solutions found: {self.solution_count}")

def create_puzzle(states):
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    size = model.NewIntVar(2, 20, 'size')

    state_vars = []
    for state in states:
        state_len = len(state)

        row_start = model.NewIntVar(0, 20 - state_len + 1, f'row_start_{state}')
        col_start = model.NewIntVar(0, 20 - state_len + 1, f'col_start_{state}')



        direction = model.NewIntVar(0, 3, f'direction_{state}')

        model.AddAllDifferent([row_start, col_start])

        state_vars.append((row_start, col_start, direction))

    for (state1, state_vars1), (state2, state_vars2) in product(enumerate(state_vars), repeat=2):
        if state1 < state2:
            row_start1, col_start1, direction1 = state_vars1
            row_start2, col_start2, direction2 = state_vars2

            for i, j in product(range(len(states[state1])), range(len(states[state2]))):
                model.Add((row_start1 + i != row_start2 + j) | (col_start1 + i != col_start2 + j))

    model.Add(row_start <= size - state_len + 1)
    model.Add(col_start <= size - state_len + 1)


    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        puzzle_size = solver.Value(size)

        puzzle = [['.' for _ in range(puzzle_size)] for _ in range(puzzle_size)]

        for state, (row_start, col_start, direction) in zip(states, state_vars):
            row = solver.Value(row_start)
            col = solver.Value(col_start)
            dir_idx = solver.Value(direction)

            for i, letter in enumerate(state):
                if dir_idx == 0:
                    puzzle[row][col + i] = letter
                elif dir_idx == 1:
                    puzzle[row + i][col] = letter
                elif dir_idx == 2:
                    puzzle[row + i][col + i] = letter
                else:
                    puzzle[row - i][col + i] = letter

        return puzzle

    return None

states = [
    "AA", "BB", "CC", "DD", "AB", "AC", "AD", "BC" , "BD", "CD"
]

puzzle = create_puzzle(states)

if puzzle:
    for row in puzzle:
        print(' '.join(row))
    print(len(row), len(puzzle))
else:
    print("No solution found.")

