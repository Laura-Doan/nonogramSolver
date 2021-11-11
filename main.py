from copy import deepcopy

def driver():
    width = int(input("how wide is the nonogram?"))
    height = int(input("how tall is the nonogram?"))
    clues = populate_clues(width, height)
    grid = create_grid(width, height)

    old_grid = grid
    grid = initial_solve_pass(grid, clues, width, height)
    grid = solve_pass(grid, clues, width, height)

    while not_solved(grid, height, width) and changed(grid, old_grid):
        old_grid = grid
        grid = solve_pass(grid, clues, width, height)

    for row in range(height):
        print(grid[row])


def populate_clues(width, height):
    clues = [[], []]

    # gets vertical clues
    for column in range(width):
        clues[0].append([])
        num_clues = int(input("how many numbers are in the next column"))
        for location in range(num_clues):
            clues[0][column].append(int(input("what is the next number")))

    # gets horizontal clues
    for row in range(height):
        clues[1].append([])
        num_clues = int(input("how many numbers are in the next row"))
        for location in range(num_clues):
            clues[1][row].append(int(input("what is the next number")))

    return clues


# creates an grid that is width by height filled with *. This symbol will be used to denote a undecided square
def create_grid(width, height):
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            grid[row].append("*")
    return grid


# returns true if any squares still contain *, returns false otherwise
def not_solved(grid, height, width):
    for row in range(height):
        for column in range(width):
            if grid[row][column] == "*":
                return True
    return False


def changed(grid, old_grid):
    if grid == old_grid:
        return False
    else:
        return True


# fills in any rows and columns with only 1 possible solution
def initial_solve_pass(grid, clues, width, height):
    # checks if column has one solution
    for column in range(width):
        column_clue_total = total_of_clues_column(clues, column)
        column_clue_total += len(clues[0][column]) - 1

        # fills in column if it has one solution
        if column_clue_total == height:
            location = 0
            for clue in clues[0][column]:
                for i in range(clue):
                    grid[location][column] = 1
                    location += 1
                if location < height:
                    grid[location][column] = "0"
                    location += 1

    # checks if row has one solution
    for row in range(height):
        row_clue_total = total_of_clues_row(clues, row)
        row_clue_total += len(clues[1][row])-1

        # fills in column if it has one solution
        if row_clue_total == width:
            location = 0
            for clue in clues[1][row]:
                for i in range(clue):
                    grid[row][location] = 1
                    location += 1
                if location < width:
                    grid[row][location] = 0
                    location += 1
    return grid


def solve_pass(grid, clues, width, height):
    for column_num in range(width):
        grid = column_pass(grid, clues, column_num, height)
    for row_num in range(height):
        grid = row_pass(grid, clues, row_num, width)
    for column_num in range(width):
        grid = column_pass(grid, clues, column_num, height)
    for row_num in range(height):
        grid = row_pass(grid, clues, row_num, width)
    return grid


def column_pass(grid, clues, column_num, height):
    column_clues = []
    column = []
    for clue in clues[0][column_num]:
        column_clues.append(clue)
    for row in range(height):
        column.append(grid[row][column_num])

    possible = create_possible(column_clues, height)
    possible = strike_possibilities(possible, column)

    for item in range(len(possible[0])):
        the_same = True
        for possibility in range(len(possible)):
            if possible[possibility][item] != possible[0][item]:
                the_same = False
        if the_same:
            grid[item][column_num] = possible[0][item]

    return grid


def row_pass(grid, clues, row_num, width):
    row_clues = []
    row = []
    for clue in clues[1][row_num]:
        row_clues.append(clue)
    for column_num in range(width):
        row.append(grid[row_num][column_num])

    possible = create_possible(row_clues, width)
    possible = strike_possibilities(possible, row)

    for item in range(len(possible[0])):
        the_same = True
        for possibility in range(len(possible)):
            if possible[possibility][item] != possible[0][item]:
                the_same = False
        if the_same:
            grid[row_num][item] = possible[0][item]

    return grid


def strike_possibilities(possible, line):
    item = 0
    num_possibilities = len(possible)-1
    while item <= num_possibilities:
        possibility = possible[item]
        for location in range(len(line)):
            if line[location] != '*' and possibility[location] != line[location]:
                del possible[item]
                item -= 1
                num_possibilities -= 1
                break
        item += 1
    return possible


def create_possible(line_clues, length):
    possible = []
    empty_possibility = create_empty_possibility(length)
    spaces = create_empty_spaces(len(line_clues))
    at = len(spaces)-1

    clue_total = 0
    for clue in line_clues:
        clue_total += clue
    max_spaces = length - clue_total - (len(line_clues)-1)

    while spaces[0] < max_spaces:
        new_possibility = empty_possibility.copy()
        location = 0

        # creates a possibility based on the current values of spaces
        for item in range(len(spaces)):
            location += spaces[item]
            for clue in range(line_clues[item]):
                new_possibility[location] = 1
                location += 1
        possible.append(new_possibility)

        # updates spaces
        if location < length:
            spaces[-1] += 1
            continue
        else:
            i = len(spaces)-2
            cont = True
            while i >= at:
                if spaces[i+1] > 1:
                    spaces[i] += 1
                    for i2 in range(i+1, len(spaces)):
                        spaces[i2] = 1
                    cont = False
                    break
                else:
                    i -= 1
            if cont:
                if max_spaces == 0:
                    break
                at -= 1
                for i in range(len(spaces)):
                    spaces[i] = 1
                if at > 0:
                    spaces[0] = 0
                    spaces[at] = 2
                else:
                    spaces[0] = 1

    # creates a final possibility based on the current values of spaces
    location = 0
    new_possibility = empty_possibility.copy()
    for item in range(len(spaces)):
        location += spaces[item]
        for clue in range(line_clues[item]):
            new_possibility[location] = 1
            location += 1
    possible.append(new_possibility)
    return possible

def create_empty_spaces(size):
    spaces = []
    for i in range(size):
        spaces.append(1)
    spaces[0] = 0
    return spaces


def create_empty_possibility(length):
    empty_possibility = []
    for i in range(length):
        empty_possibility.append(0)
    return empty_possibility


def total_of_clues_column(clues, column):
    column_clue_total = 0
    for clue in clues[0][column]:
        column_clue_total += clue
    return column_clue_total


def total_of_clues_row(clues, row):
    row_clue_total = 0
    for clue in clues[1][row]:
        row_clue_total += clue
    return row_clue_total


def temp_driver():
    width = 6
    height = 6
    clues = [[[1], [5], [2], [5], [2, 1], [2]], [[2, 1], [1, 3], [1, 2], [3], [4], [1]]]
    grid = create_grid(width, height)

    old_grid = deepcopy(grid)
    grid = initial_solve_pass(grid, clues, width, height)
    grid = solve_pass(grid, clues, width, height)

    while not_solved(grid, height, width) and changed(grid, old_grid):

        old_grid = deepcopy(grid)
        grid = solve_pass(grid, clues, width, height)

    for row in range(height):
        print(grid[row])


temp_driver()