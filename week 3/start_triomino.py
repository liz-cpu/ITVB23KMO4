import numpy as np

# place triominoes in matrix 3 rows x 4 cols

NR_OF_COLS = 16 # 4 triominoes HB VB L RL + 12 cells
NR_OF_ROWS = 22 # 6*HB 4*VB 6*L 6*RL

triominoes = [np.array(piece) for piece in [
        # horizontal bar (HB)
        [[1,1,1]],
        # vertical bar (VB)
        [[1],[1],[1]],
        # normal L (L)
        [[1,0], [1,1]],
        # rotated L (RL)
        [[1,1], [0,1]]
    ]
]

def make_matrix(triominoes):

    # create and return matrix as input for alg-x
    # matrix has 22 rows x 16 cols
    # and has the following cols: HB VB L RL (0,0) (0,1) (0,2) (0,3) (1,0) .... (3,3)

    def all_positions(triominoes):
        # find all positions to place triomino T in matrix M (3 rows x 4 cols)
        rows, cols = triominoes.shape
        for i in range(3+1 - rows):
            for j in range(4+1 - cols):
                M = np.zeros((3, 4), dtype='int')
                # place T in M
                M[i:i+rows, j:j+cols] = triominoes
                yield M

    rows = []
    for i, P in enumerate(triominoes):
        # i points to the 4 triominoes HB VB L RL
        for A in all_positions(P):
            # add 4 zeros to each row
            A = np.append(np.zeros(4, dtype='int'), A)
            A[i] = 1
            rows.append(list(A))
    return rows


def prepare(mx):
    # note that when applying alg-x we're only interested in 1's
    # so we add 2 lists that define where the 1's are
    rows = mx    
    # note that zip(*b) is the transpose of b
    cols = [list(i) for i in zip(*rows)]

    print(np.array(rows))
    print()

    def find_ones(rows):
        """Returns indexes in rows where the ones are

        For example, given the following matrix:
        [[1, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 0]]

        The function will return, if rows is given as input:
        [[0, 3], [1, 2, 3], [1, 2], [0]]

        :return: A list of lists, where each list contains the indexes of the ones in that row
        :rtype: list[list[int]]
        """
        lv_row_has_1_at = []
        for row in rows:
            x = []
            for i in range(len(row)):
                if row[i] == 1:
                    x.append(i)
            lv_row_has_1_at.append(x.copy())
        return lv_row_has_1_at

    row_has_1_at = find_ones(rows) # read-only list; example: [[0, 3], [1, 3], [1, 2], [2]]
    col_has_1_at = find_ones(cols) # read-only list; example: [[0], [1, 2], [2, 3], [0, 1]]

    # if there's a col without ones, then there is no exact cover possible
    halt_fl = False
    for l in col_has_1_at:
        if l == []:
            print("No solution possible!")
            halt_fl = True

    row_valid = NR_OF_ROWS * [1]
    col_valid = NR_OF_COLS * [1]

    return halt_fl, row_valid, col_valid, row_has_1_at, col_has_1_at

def cover(r, row_valid, col_valid, row_has_1_at, col_has_1_at):
    # cover row r
    row_valid[r] = 0
    for c in row_has_1_at[r]:
        col_valid[c] = 0
        for r2 in col_has_1_at[c]:
            row_valid[r2] = 0
    return row_valid, col_valid

def print_solution(solution, row_has_1_at):
    # place triominoes in matrix D 3 rows x 4 cols
    D = [[0 for i in range(4)] for j in range(3)]

    for row_number in solution:
        #print(row_number) # 1 6 14 21
        row_list = row_has_1_at[row_number]
        #print(row_list)   # 0 5 6 7
        idx = row_list[0]
        assert idx in [0,1,2,3]
        symbol = ['HB','VB','L ','RL'][idx]
        for c in row_list[1:]: # skip first one
            rownr = c//4-1
            colnr = c%4
            D[rownr][colnr] = symbol
    print('------------------------')

    for i in D:
        print(i)

def solve(row_valid, col_valid, row_has_1_at, col_has_1_at, solution):
    """_summary_

    :param row_valid: List of 1's and 0's. 1 means row is valid, 0 means row is invalid
    :type row_valid: list[bool]
    :param col_valid: List of 1's and 0's. 1 means col is valid, 0 means col is invalid
    :type col_valid: list[bool]
    :param row_has_1_at: List of lists. Each list contains the indexes of the ones in that row
    :type row_has_1_at: list[list[int]]
    :type row_has_1_at: list[list[int]]
    :param col_has_1_at: List of lists. Each list contains the indexes of the ones in that col
    :type col_has_1_at: list[list[int]]
    :param solution: List of rows that are part of the solution
    :type solution: list[int]
    """

    for row in range(len(row_valid)):
        if row_valid[row]:
            row_valid2, col_valid2 = cover(row, row_valid.copy(), col_valid.copy(), row_has_1_at, col_has_1_at)
            solution2 = solution.copy()
            solution2.append(row)
            if sum(row_valid2) == 0:
                print_solution(solution2, row_has_1_at)
            else:
                solve(row_valid2, col_valid2, row_has_1_at, col_has_1_at, solution2)

mx = make_matrix(triominoes)

halt_fl, row_valid, col_valid, row_has_1_at, col_has_1_at = prepare(mx)
if not halt_fl:
    sv = solve(row_valid, col_valid, row_has_1_at, col_has_1_at, [])