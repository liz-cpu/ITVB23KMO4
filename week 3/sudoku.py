import time

#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I


def cross(A: str, B: str) -> list[str]:
    """
    Concatenate each letter in A with each letter in B.

    :param A: a string
    :param B: a string
    :return: a list of strings
    """
    return [a+b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
cells = cross(rows, cols)  # 81 cells A1..9, B1..9, C1..9, ...

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +  # 9 rows
             [cross(rows, c) for c in cols] +  # 9 cols
             [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])  # 9 units


units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in cells)


def test() -> None:
    """
    Tests
    """
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unit_list) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


def display(grid: dict[str, str]) -> None:
    """
    Display the grid.

    :param grid: a dictionary with the sudoku grid e.g. grid['A1'] = '1234'
    :type grid: dict[str, str]
    """
    print()
    for r in rows:
        for c in cols:
            v = grid[r+c]
            # avoid the '123456789'
            if v == '123456789':
                v = '.'
            print(''.join(v), end=' ')
            if c == '3' or c == '6':
                print('|', end='')
        print()
        if r == 'C' or r == 'F':
            print('-------------------')
    print()


def parse_string_to_dict(grid_string: str) -> dict[str, str]:
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]
    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))


def no_conflict(grid: dict[str, str], c: str, val: str) -> bool:
    """
    Check if assignment is possible: value v not a value of a peer

    :param grid: dictionary with the sudoku grid 
    :type grid: dict[str, str]
    :param c: cell
    :type c: str
    :param val: value
    :type val: str
    :return: True if no conflict, False otherwise
    :rtype: bool
    """
    for p in peers[c]:
        if grid[p] == val:
            return False  # conflict
    return True


def solve(grid: dict[str, str], method: str = 'DFS') -> dict | None:
    """
    Solve the sudoku grid.

    :param grid: a dictionary with the sudoku grid
    :type grid: dict[str, str]
    :param method: the method to use for solving the sudoku grid, either 'DFS', 'DFS-ARCC' or 'ALG-X'
    :type method: str
    :return: a dictionary with the solved sudoku grid or None if the method is invalid
    :rtype: dict[str, str] | None
    """
    solution = grid
    if method.upper() == 'DFS':
        solution = dfs(grid)
    elif method.upper() == 'DFS-ARCC':
        solution = dfs_arc_consistent(grid)
    elif method.upper() == 'ALG-X':
        solution = alg_x(grid)
    else:
        print('Invalid method given')
        return None
    return solution


def dfs(grid: dict[str, str], solution: dict[str, str] = {}) -> dict[str, str]:
    """
    Use depth-first search to solve the sudoku grid.

    :param grid: a dictionary with the sudoku grid
    :type grid: dict[str, str]
    :param solution: a dictionary with the solution, defaults to {}
    :type solution: dict[str, str], optional
    :return: a dictionary with the solved sudoku grid
    :rtype: dict[str, str]
    """
    # depth-first search
    # order cells by the number of possible values of its peers in ascending order
    ordered_cells = sorted(grid, key=lambda c: sum(
        [len(grid[p]) for p in peers[c]]))
    for c in ordered_cells:
        if len(grid[c]) > 1:
            for val in grid[c]:
                if no_conflict(grid, c, val):
                    old_val = grid[c]
                    grid[c] = val
                    solution = dfs(grid, solution)
                    grid[c] = old_val
            return solution
    # no more empty cells
    return grid.copy()


def make_arc_consistent(grid: dict[str, str]) -> dict[str, str] | bool:
    """
    Makes grid arc-consistent by removing values from peers that are not
    possible for a cell

    :param grid: a dictionary with the sudoku grid
    :type grid: dict[str, str]
    :return: a dictionary with the arc-consistent sudoku grid or False
    :rtype: dict[str, str] | False
    """
    for c in grid:
        if len(grid[c]) == 1:
            for p in peers[c]:
                if grid[c] in grid[p]:
                    if len(grid[p]) <= 1:
                        return False
                    grid[p] = grid[p].replace(grid[c], '')
    return grid


def dfs_arc_consistent(grid: dict[str, str], solution: dict[str, str] = {}) -> dict[str, str]:
    """
    Depth-first search with arc-consistency

    :param grid: a dictionary with the sudoku grid
    :type grid: dict[str, str]
    :param solution: a dictionary with the solution, defaults to {}
    :type solution: dict[str, str], optional
    :return: a dictionary with the solved sudoku grid
    :rtype: dict[str, str]
    """
    new_grid = make_arc_consistent(grid.copy())
    if new_grid == False:
        return solution
    # order cells by the number of possible values of its peers in ascending order
    ordered_cells = sorted(grid, key=lambda c: sum(
        [len(grid[p]) for p in peers[c]]))
    for c in ordered_cells:
        if len(new_grid[c]) > 1:
            for val in new_grid[c]:
                if no_conflict(new_grid, c, val):
                    old_val = new_grid[c]
                    new_grid[c] = val
                    solution = dfs_arc_consistent(new_grid, solution)
                    new_grid[c] = old_val
            return solution
    # no more empty cells
    return new_grid.copy()


def alg_x(grid: dict[str, str]) -> dict[str, str]:
    """
    Solve the sudoku grid using Knuth's Algorithm X

    :param grid: a dictionary with the sudoku grid
    :type grid: dict[str, str]
    :return: a dictionary with the solved sudoku grid
    :rtype: dict[str, str]
    """
    pass


# minimum nr of clues for a unique solution is 17
slist = [None for x in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10] = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11] = '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12] = '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
# slist[12]= '.....6....59.....82....8....45........3........6..3.54...325..6..................'
# replaced 12 because it takes too long to solve for some reason
# TODO: find out why and fix it
slist[13] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14] = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15] = '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16] = '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17] = '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18] = '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19] = '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'

for i, sudo in enumerate(slist):
    print('*** sudoku {0} ***'.format(i))
    d = parse_string_to_dict(sudo)
    display(d)
    start_time = time.time()
    # solution = solve(d, 'DFS')
    solution = solve(d, 'DFS-ARCC')
    end_time = time.time()
    display(solution)
    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("duration [hh:mm:ss.ddd]: {:0>2}:{:0>2}:{:06.3f}".format(
        int(hours), int(minutes), seconds))
    print()


"""
1 2 9 |5 7 6 |3 4 8 
3 7 6 |4 2 8 |5 1 9
5 8 4 |3 9 1 |6 2 7
-------------------
2 9 3 |8 1 5 |7 6 4
4 1 7 |2 6 3 |8 9 5
8 6 5 |7 4 9 |1 3 2
-------------------
9 5 8 |6 3 2 |4 7 1
7 3 1 |9 8 4 |2 5 6
6 4 2 |1 5 7 |9 8 3

duration [hh:mm:ss.ddd]: 00:00:00.532
"""