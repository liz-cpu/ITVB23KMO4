"""
Task 3: CARD PUZZLE

A card puzzle is as follows. There are eight cards: two Aces, two Kings,
two Queens, and two Jacks. The eight cards must be placed on the board
(grid) as shown below, so that:

    1. every Ace borders a King
    2. every King borders a Queen
    3. every Queen borders a Jack
    4. no Ace borders a Queen
    5. no two of the same cards border each other

┌───┬───┬───┬───┐
│   │   │ 0 │   │
├───┼───┼───┼───┤
│ 1 │ 2 │ 3 │   │
├───┼───┼───┼───┤
│   │ 4 │ 5 │ 6 │
├───┼───┼───┼───┤
│   │   │ 7 │   │
└───┴───┴───┴───┘

Adjacent means here: horizontally or vertically.

a) Let's assign an index to all positions on the board and represent the board
with a dictionary (key=index, value=card). Create a program that returns both
solutions to the puzzle based on brute force, generating all permutations and
testing them one by one. On Blackboard, you can find the file card_puzzle.py
to start with.

    1. How many (different) permutations are there actually? How can you
    calculate this yourself? Keep in mind that (A, A, A, A, ...) is not
    possible, as you can only choose A twice.

    2. When testing, it's wise to perform the most restrictive test first
    ('FALSEail fast'). How many permutations need to be tested (= iterations)
    to find the first and second solutions?

b) Implement a better version using DFS and backtracking. This can be done in
about 70 lines, with the most challenging part being to implement the tests
correctly. How many iterations (recursive calls) are now needed to find the
first and second solutions?

Tip: You can reuse the tests from (a) in (b), but in (b), you need to consider
that a square can also be empty, which is only filled later (deeper in the DFS
tree). The permutations in (a) are the leaf nodes of the DFS tree in (b).

c) You can also solve the puzzle by repeatedly applying arc-consistency (and
some logical reasoning). Do this on paper. Argue that board[5] must be a King
by showing that board[5] cannot be an Ace, Queen, or Jack. Then, argue in the
same way that board[0] must also be a King.

A (starting) example of how you can write this is as follows.
Assume 5 is an Ace.
• 3,4,6,7 cannot be A due to [5]
• 3,4,6,7 cannot be Q due to [4]
• So, 3,4,6,7 must be a K or J
• There are only 2xK and 2xJ cards, so 0,1,2 must be an A or Q.
```
┌─────────┬─────────┬─────────┬─────────┐
│         │         │ A,𝙆,Q,𝙅 │         │
├─────────┼─────────┼─────────┼─────────┤
│ A,𝙆,Q,𝙅 │ A,𝙆,Q,𝙅 │ 𝘼,K,𝙌,J │         │
├─────────┼─────────┼─────────┼─────────┤
│         │ 𝘼,K,𝙌,J │    A    │ 𝘼,K,𝙌,J │
├─────────┼─────────┼─────────┼─────────┤
│         │         │ 𝘼,K,𝙌,J │         │
└─────────┴─────────┴─────────┴─────────┘
```

"""

from copy import deepcopy
from itertools import permutations

import colorama
colorama.init()

# the board has 8 cells, let’s represent the board with a list [0..7]
start_board = ['.'] * 8
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0: [3], 1: [2], 2: [1, 4, 3], 3: [0, 2, 5],
             4: [2, 5], 5: [3, 4, 6, 7], 6: [5], 7: [5]}


def print_board(board: dict):
    b = [board[i] if board[i] != '.' else ' ' for i in range(8)]
    print(f"""
          ┌───┬───┬───┬───┐
          │▓▓▓│▓▓▓│ {b[0]} │▓▓▓│
          ├───┼───┼───┼───┤
          │ {b[1]} │ {b[2]} │ {b[3]} │▓▓▓│
          ├───┼───┼───┼───┤
          │▓▓▓│ {b[4]} │ {b[5]} │ {b[6]} │
          ├───┼───┼───┼───┤
          │▓▓▓│▓▓▓│ {b[7]} │▓▓▓│
          └───┴───┴───┴───┘
          """)


constraints = {
    'A': {'yes': ['K'], 'no': ['Q']},
    'K': {'yes': ['Q'], 'no': []},
    'Q': {'yes': ['J'], 'no': ['A']},
    'J': {'yes': [], 'no': []}
}


def priny(any):
    print(colorama.Fore.YELLOW + str(any) + colorama.Fore.RESET)


def princ(any):
    print(colorama.Fore.CYAN + str(any) + colorama.Fore.RESET)


def prinr(any):
    print(colorama.Fore.RED + str(any) + colorama.Fore.RESET)


def pring(any):
    print(colorama.Fore.GREEN + str(any) + colorama.Fore.RESET)


def is_valid(board):
    # print_board(board)
    count = {"A": 0, "K": 0, "Q": 0, "J": 0}

    for i in range(len(board)):
        card = board[i]
        if card == '.':
            continue

        # princ(f"Checking card {card}")

        count[card] += 1
        nya = deepcopy(constraints[card]['yes'])
        meow = len(nya)

        for neighbor in neighbors[i]:
            # priny(f"Checking neighbor {neighbor}")

            if board[neighbor] in constraints[card]['no']:
                return False

            if board[neighbor] == card:
                return False

            if board[neighbor] in nya:
                nya.remove(board[neighbor])
                meow -= 1

            if board[neighbor] == '.':
                meow -= 1

        if meow > 0:
            return False

    return True if all(count[card] <= 2 for card in count) else False


def solve_brute_force(board: dict, cards: list):
    board = deepcopy(board)
    cards = [card for card in cards if card not in board.values()]
    indices = [i for i in board.keys() if board.get(i) == '.']
    if len(indices) == 0:
        print_board(board)
        return
    given = {key: value for key, value in board.items() if value != '.'}

    perms = permutations(cards, len(indices))

    for perm in perms:

        new_board = {i: perm[imdex] for imdex, i in enumerate(indices)}
        new_board.update(given)
        princ(new_board)
        if is_valid(new_board):
            print_board(new_board)
            return
    prinr("No solution found")


def test():
    tru = colorama.Fore.GREEN + 'True' + colorama.Fore.RESET
    fal = colorama.Fore.RED + 'False' + colorama.Fore.RESET
    # is_valid(board) checks all cards, returns False if any card is invalid
    print(fal, is_valid({0: 'J', 1: 'K', 2: 'Q',
          3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print(fal, is_valid({0: 'J', 1: 'J', 2: 'Q',
          3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print(tru, is_valid({0: '.', 1: '.', 2: '.',
          3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print(tru, is_valid({0: 'J', 1: '.', 2: '.',
          3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print(fal, is_valid({0: '.', 1: '.', 2: '.', 3: 'J',
          4: 'J', 5: 'A', 6: 'J', 7: 'J'}))  # [1]
    print(fal, is_valid({0: 'J', 1: '.', 2: '.', 3: '.',
          4: 'J', 5: 'K', 6: 'J', 7: 'Q'}))  # [3]
    print(tru, is_valid({0: '.', 1: 'Q', 2: '.', 3: '.',
          4: 'Q', 5: 'J', 6: '.', 7: '.'}))  # [3]
    print(fal, is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K',
          4: '.', 5: '.', 6: '.', 7: '.'}))  # [3]
    print(fal, is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.',
          4: '.', 5: 'Q', 6: '.', 7: '.'}))  # [4]
    print(fal, is_valid({0: '.', 1: '.', 2: '.', 3: '.',
          4: 'J', 5: 'J', 6: '.', 7: '.'}))  # [5]
    print(fal, is_valid({0: '.', 1: '.', 2: '.', 3: '.',
          4: '.', 5: 'Q', 6: '.', 7: 'Q'}))  # [5]
    print(tru, is_valid({0: 'Q', 1: 'Q', 2: '.',
          3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))


def test_brute_force():
    board_test = {0: 'Q', 1: 'Q', 2: '.',
          3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}
    cards_test = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
    solve_brute_force(board_test, cards_test)
    # board_test = {0: 'J', 1: '.', 2: '.',
    #       3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}
    # solve_brute_force(board_test, cards_test)

test_brute_force()