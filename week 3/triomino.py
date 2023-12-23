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

