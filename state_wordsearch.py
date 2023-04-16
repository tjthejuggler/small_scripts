states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]



import random
from itertools import product
from termcolor import colored

def add_state(puzzle, state, overlaps):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    state_len = len(state)

    for row, col in product(range(len(puzzle)), range(len(puzzle[0]))):
        for direction in directions:
            fit = True
            for i in range(state_len):
                r, c = row + i * direction[0], col + i * direction[1]
                if r < 0 or r >= len(puzzle) or c < 0 or c >= len(puzzle[0]):
                    fit = False
                    break
                if puzzle[r][c] != '.' and puzzle[r][c] != state[i]:
                    fit = False
                    break

            if fit:
                for i in range(state_len):
                    r, c = row + i * direction[0], col + i * direction[1]
                    if puzzle[r][c] == state[i]:
                        overlaps[r][c] += 1
                    else:
                        overlaps[r][c] = 1
                    puzzle[r][c] = state[i]
                return True
    return False

def create_puzzle(states):
    puzzle_size = 21
    puzzle = [['.' for _ in range(puzzle_size)] for _ in range(puzzle_size)]
    overlaps = [[0 for _ in range(puzzle_size)] for _ in range(puzzle_size)]

    states_sorted = sorted(states, key=len, reverse=True)
    success = False
    while not success:
        success = True
        puzzle = [['.' for _ in range(puzzle_size)] for _ in range(puzzle_size)]
        overlaps = [[0 for _ in range(puzzle_size)] for _ in range(puzzle_size)]
        for state in states_sorted:
            if not add_state(puzzle, state.upper(), overlaps):
                success = False
                break
    return puzzle, overlaps

def print_colored_puzzle(puzzle, overlaps):
    colors = ['white', 'green', 'yellow', 'red', 'blue', 'magenta', 'cyan']

    for row, overlap_row in zip(puzzle, overlaps):
        for cell, overlap in zip(row, overlap_row):
            color = colors[min(overlap, len(colors) - 1)]
            print(colored(cell, color), end=' ')
        print()

random.shuffle(states)
puzzle, overlaps = create_puzzle(states)

print_colored_puzzle(puzzle, overlaps)

print(len(puzzle[0]), len(puzzle))

total_cells = len(puzzle[0]) * len(puzzle)
filled_cells = sum([1 for row in puzzle for cell in row if cell != '.'])
percentage_filled = (filled_cells / total_cells) * 100

print(f"{percentage_filled:.2f}% of the letters are used by states in the total puzzle")


