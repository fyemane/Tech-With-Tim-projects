board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]
test_board = [
    [0, 0, 0, 0, 7, 0, 5, 0, 0],
    [4, 0, 0, 0, 0, 1, 3, 0, 0],
    [2, 9, 0, 0, 5, 0, 0, 0, 0],
    [8, 0, 0, 9, 0, 0, 0, 0, 2],
    [0, 0, 9, 0, 1, 0, 4, 0, 0],
    [5, 0, 0, 0, 0, 6, 0, 0, 7],
    [0, 0, 0, 0, 3, 0, 0, 9, 6],
    [0, 0, 4, 7, 0, 0, 0, 0, 8],
    [0, 0, 8, 0, 9, 0, 0, 0, 0]
]

def solve(bo):
    find = find_empty(bo)

    if not find:
        return True
    else:
        row, col = find
    # repeatedly check all numbers from 1-9
    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            # add number into board
            bo[row][col] = i
            # keep checking if board is finished
            if solve(bo):
                return True
            # backtrack to last element and change it to 0
            bo[row][col] = 0
    return False


# is a number on a specific position valid or not
def valid(bo, num, pos):
    # check row
    for i in range(len(bo[0])):
        # check in each column (each element in row) is equal to num we just added in
        # check if checked position is pos we just inserted a num
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    # check column
    # loop through every row
    for i in range(len(bo)):
        # check if any column is same that we just inserted
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    # check box (// is integer division)
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    # pos[0] is row,
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


# prints nicely formatted sudoku board
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            # print horizontal line every 3 rows
            print("- - - - - - - - - - -")
        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                # end=" " -- doesn't make new line
                print("|", end=" ")
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + "", end=" ")


# finds empty square and returns its coordinates
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                # returns a tuple [row, col]
                return i, j
    # return False is also an option
    return None
