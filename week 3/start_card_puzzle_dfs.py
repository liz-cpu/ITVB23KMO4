# vragen:
# a)
#   1. Hoeveel (verschillende) permutaties zijn er eigenlijk? Hoe kun je dit zelf berekenen? Hou er rekening mee dat (A,A,A,A …) niet kan, je kan immers A maar 2 keer kiezen.
#     8! / (2! * 2! * 2! * 2!) = 2520 permutaties
#   2. Bij het testen is het slim om de test die het meest beperkend is het eerst te doen (‘fail fast’). Hoeveel permutaties moeten er worden getest (= iteraties) om de eerste en tweede oplossing te vinden?
#     Found valid board at iteration 699
#     Found valid board at iteration 1620
#     [{0: 'K', 1: 'Q', 2: 'J', 3: 'Q', 4: 'A', 5: 'K', 6: 'J', 7: 'A'}, {0: 'K', 1: 'Q', 2: 'J', 3: 'Q', 4: 'A', 5: 'K', 6: 'A', 7: 'J'}]
# b)
# Implementeer een betere versie door gebruik te maken van DFS en backtracking. Dit kan in ca. 70 regels, waarbij misschien het lastigste is de testen correct te implementeren. Hoeveel iteraties (recursive calls) zijn nu nodig om de eerste en de tweede oplossing te vinden?
#   Found valid board at iteration 11
#   Found valid board at iteration 12
#   [{0: 'K', 1: 'Q', 2: 'J', 3: 'Q', 4: 'A', 5: 'K', 6: 'J', 7: 'A'}, {0: 'K', 1: 'Q', 2: 'J', 3: 'Q', 4: 'A', 5: 'K', 6: 'A', 7: 'J'}]
# c)
# Je kan de puzzel ook oplossen door herhaaldelijk arc-consistency toe te passen (en wat logisch redeneren).Doe dit op papier. Beredeneer dat bord[5] een Heer moet zijn, door te laten zien dat bord[5] geen Aas, Vrouw of Boer kan zijn. Beredeneer daarna - op eenzelfde manier - dat bord[0] ook een Heer moet zijn.
#   kan worden gevonden in Q3C.xlsx

import itertools

'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
# the board has 8 cells, let’s represent the board with a list [0..7]
start_board = dict(zip(range(8), ['.'] * 8))
checked_boards = set()
dfs_iterate_count = 0
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0:[3], 1:[2], 2:[1,4,3], 3:[0,2,5], 4:[2,5], 5:[3,4,6,7], 6:[5], 7:[5]}

def is_valid(board):
    for idx, card in enumerate(board.values()):
        # If empty, continue
        if card == '.':
            continue
        current_neighbors = [board[n] for n in neighbors[idx]]
        empty_neighbors = [n for n in neighbors[idx] if board[n] == '.']
        # If Ace, check if King is in neighbors and no Queen is in neighbors
        if card == 'A':
            if 'K' not in current_neighbors and len(empty_neighbors) == 0:
                return False
            if 'Q' in current_neighbors:
                return False
        # If King, check if Queen is in neighbors
        elif card == 'K':
            if 'Q' not in current_neighbors and len(empty_neighbors) == 0:
                return False
        # If Queen, check if Jack is in neighbors
        elif card == 'Q':
            if 'J' not in current_neighbors and len(empty_neighbors) == 0:
                return False
        # If two of the same cards, check if they are not neighbors
        for n in neighbors[idx]:
            if board[n] == card:
                return False
    return True

def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ',is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('f ',is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})) # [1]
    print('f ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})) # [3]
    print('t ',is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})) # [3] 
    print('f ',is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})) # [3]
    print('f ',is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})) # [4]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})) # [5]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})) # [5]
    print('t ',is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))

def brute_force(board, cards):
    # get all possible permutations of the cards
    for i, permutation in enumerate(set(itertools.permutations(cards))):
        # assign the cards to the board
        for idx, card in enumerate(permutation):
            board[idx] = card
        # check if the board is valid
        if is_valid(board):
            print("Found valid board at iteration", i)
            yield board.copy()

def dfs_backtrack(board, cards):
    global dfs_iterate_count
    dfs_iterate_count += 1
    # uses Depth First Search with backtracking to find all valid boards
    for card in cards:
        # assign the card to the board
        board[len(board) - len(cards)] = card
        # has this board already been checked?
        if tuple(board.values()) in checked_boards:
            continue
        # if the board is valid
        if is_valid(board):
            checked_boards.add(tuple(board.values()))
            # if all cards are assigned, yield the board
            if list(board.values()).count('.') == 0:
                print("Found valid board at iteration", dfs_iterate_count)
                yield board.copy()
            # else, recursively call dfs_backtrack with the remaining cards
            else:

                yield from dfs_backtrack(board, [c for i, c in enumerate(cards) if c != card or (c == card and i != cards.index(card))])
        # remove the card from the board
        board[len(board) - len(cards)] = '.'
    

print(list(brute_force(start_board.copy(), cards.copy())))
print(list(dfs_backtrack(start_board.copy(), cards.copy())))