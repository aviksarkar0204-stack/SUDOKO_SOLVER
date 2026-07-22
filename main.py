grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def is_valid(grid, row, col, num):
    # Check the row
    for c in range(9):
        if grid[row][c] == num:
            return False

    # Check the column
    for r in range(9):
        if grid[r][col] == num:
            return False

    # Check the 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] == num:
                return False

    return True

#print(is_valid(grid, 0, 2, 5))
#print(is_valid(grid, 0, 2, 4))

def find_empty(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None

#print(find_empty(grid))

def solve(grid):
    empty = find_empty(grid)
    if empty is None:
        return True  # no empty cells left, solved!

    row, col = empty

    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            grid[row][col] = num  # place it

            if solve(grid):  # recursively try to solve the rest
                return True

            grid[row][col] = 0  # undo (backtrack) — didn't work out

    return False  # no number worked here, trigger backtrack in caller

def print_grid(grid):
    for row in range(9):
        if row % 3 == 0 and row != 0:
            print("- - - - - - - - - - - -")

        for col in range(9):
            if col % 3 == 0 and col != 0:
                print("|", end=" ")

            if col == 8:
                print(grid[row][col])
            else:
                print(grid[row][col], end=" ")