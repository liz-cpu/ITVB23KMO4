"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    """
    List all the valid squares on the board.

    Returns:
        list: A list of valid integers [11, 12, ...]; e.g., 19, 20, 21 are invalid.
              11 means the first row, first col because the board size is 10x10.
    """
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    """
    Create a new board with the initial black and white positions filled.

    Returns:
        list: A list representing the initial board state.
    """
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # The middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    """
    Get a string representation of the board.

    Args:
        board (list): The current board state.

    Returns:
        str: A string representation of the board.
    """
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    """
    Check if the move is a square on the board.

    Args:
        move (int): The move to be checked.

    Returns:
        bool: True if the move is a square on the board; False otherwise.
    """
    return isinstance(move, int) and move in squares()

def opponent(player):
    """
    Get the player's opponent piece.

    Args:
        player (str): The current player.

    Returns:
        str: The opponent's piece.
    """
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    """
    Find and return the square that forms a bracket with a given square for the player
    in the given direction; returns None if no such square exists.

    Args:
        square (int): The square to find the bracket for.
        player (str): The current player.
        board (list): The current board state.
        direction (int): The direction to search for a bracket.

    Returns:
        int or None: The square that forms a bracket or None if no bracket exists.
    """
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    """
    Check if the move is legal for the player.

    Args:
        move (int): The move to be checked.
        player (str): The current player.
        board (list): The current board state.

    Returns:
        bool: True if the move is legal; False otherwise.
    """
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

def make_move(move, player, board):
    """
    Update the board and flip all bracketed pieces when the player makes a valid move.

    Args:
        move (int): The move to be applied.
        player (str): The current player.
        board (list): The current board state.

    Returns:
        list: The updated board state.
    """
    board[move] = player
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    """
    Flip pieces in the given direction as a result of the move by the player.

    Args:
        move (int): The move made by the player.
        player (str): The current player.
        board (list): The current board state.
        direction (int): The direction to flip pieces.
    """
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

# Monitoring players

# Define an exception
class IllegalMoveError(Exception):
    """
    Exception raised for illegal moves.

    Attributes:
        player (str): The player attempting the illegal move.
        move (int): The illegal move.
        board (list): The current board state.
    """

    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
    
    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    """
    Get a list of all legal moves for the player.

    Args:
        player (str): The current player.
        board (list): The current board state.

    Returns:
        list: A list of legal moves.
    """
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    """
    Check if the player can make any legal moves.

    Args:
        player (str): The current player.
        board (list): The current board state.

    Returns:
        bool: True if the player can make any legal moves; False otherwise.
    """
    return any(is_legal(sq, player, board) for sq in squares())

# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy: callable, white_strategy: callable):
    """
    Play a game of Othello and return the final board and score.

    Args:
        black_strategy (function): The strategy for the black player.
        white_strategy (function): The strategy for the white player.

    Returns:
        tuple: A tuple containing the final board and score.
    """
    board = initial_board()
    player = BLACK
    strategy = black_strategy if player == BLACK else white_strategy
    while player is not None:
        print(print_board(board))
        move = get_move(strategy, player, board)
        if move is not None:
            make_move(move, player, board)
        player = next_player(board, player)
    return board, score(BLACK, board)


def next_player(board, prev_player):
    """
    Determine which player should move next.

    Args:
        board (list): The current board state.
        prev_player (str): The player who made the last move.

    Returns:
        str or None: The next player or None if no legal moves exist.
    """
    opp = opponent(prev_player)
    if any_legal_move(opp, board):
        return opp
    elif any_legal_move(prev_player, board):
        return prev_player
    return None


def get_move(strategy, player, board):
    """
    Call strategy(player, board) to get a move.

    Args:
        strategy (function): The strategy function for getting a move.
        player (str): The current player.
        board (list): The current board state.

    Returns:
        int: The move obtained from the strategy.
    """
    copy = list(board)  # copy the board to prevent cheating
    move = strategy(player, copy)
    if not is_valid(move) or not is_legal(move, player, board):
        raise IllegalMoveError(player, move, copy)
    return move


def score(player, board):
    """
    Compute the player's score (number of player's pieces minus opponent's).

    Args:
        player (str): The current player.
        board (list): The current board state.

    Returns:
        int: The player's score.
    """
    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player:
            mine += 1
        elif piece == opp:
            theirs += 1
    return mine - theirs

def play_othello(black_strategy: callable = None, white_strategy: callable = None) -> None:
    """
    Play a game of Othello against the computer.
    """
    strategies = {
        BLACK: lambda who, board: random.choice(legal_moves(who, board)) if black_strategy is None else black_strategy(who, board),
        WHITE: lambda who, board: random.choice(legal_moves(who, board)) if white_strategy is None else white_strategy(who, board)
    }
    board, score = play(strategies[BLACK], strategies[WHITE])
    print_board(board)
    print('Winner: %s' %
          ('Black' if score > 0 else 'White' if score < 0 else 'Tie'))
    print('%s wins by %d points' %
          (PLAYERS[BLACK] if score > 0 else PLAYERS[WHITE], abs(score)))

play_othello()

class Node:
    def __init__(self, player, board):
        self.player = player
        self.board = board

    def is_terminal(self):
        return not any_legal_move(self.player, self.board)

    def value(self):
        return score(self.player, self.board)

    def children(self):
        for move in legal_moves(self.player, self.board):
            child_board = list(self.board)
            make_move(move, self.player, child_board)
            yield Node(opponent(self.player), child_board)

def minimax(player, board):
    """
    Return the move that minimizes the maximum loss for the current player.

    Args:
        player (str): The current player.
        board (list): The current board state.

    Returns:
        int: The move that minimizes the maximum loss.
    """
    def min_max(node, depth, max_player):
        """
        Minimax algorithm using the score() function as the heuristic.
        """
        if depth == 0 or node.is_terminal():
            return node.value()

        if max_player:
            value = -math.inf
            for child in node.children():
                value = max(value, min_max(child, depth - 1, False))
            return value
        else:
            value = math.inf
            for child in node.children():
                value = min(value, min_max(child, depth - 1, True))
            return value

    return max(legal_moves(player, board), key=lambda move: min_max(Node(player, board), 4, False))

play_othello(minimax, None)


def score_diff(player, board):
    """
    Compute the score difference (player - opponent) for the given player.

    Args:
        player (str): The current player.
        board (list): The current board state.

    Returns:
        int: The heuristic value of the board for the player.
    """
    opp = opponent(player)
    total = 0
    for sq in squares():
        piece = board[sq]
        if piece == player:
            total += 1
        elif piece == opp:
            total -= 1
    return total

def mobility(player, board):
    """
    Compute the difference in the number of legal moves available to the player and
    the opponent.

    Args:
        player (str): The current player.
        board (list): The current board state.

    Returns:
        int: The heuristic value of the board for the player.
    """
    opp = opponent(player)
    return len(legal_moves(player, board)) - len(legal_moves(opp, board))

def heuristic(player, board):
    """
    Compute the heuristic value of the board for the player.

    Args:
        player (str): The current player.
        board (list): The current board state.

    Returns:
        int: The heuristic value of the board for the player.
    """
    return score_diff(player, board) + mobility(player, board)


def optimized_minimax(player, board):
    """
    Return the move that minimizes the maximum loss for the current player.
    Optimized using a new heuristic() function (see above)

    Args:
        player (str): The current player.
        board (list): The current board state.

    Returns:
        int: The move that minimizes the maximum loss.
    """
    def min_max(node, depth, max_player):
        """
        Minimax algorithm using the heuristic() function as the heuristic.
        """
        if depth == 0 or node.is_terminal():
            return heuristic(player, node.board)

        if max_player:
            value = -math.inf
            for child in node.children():
                value = max(value, min_max(child, depth - 1, False))
            return value
        else:
            value = math.inf
            for child in node.children():
                value = min(value, min_max(child, depth - 1, True))
            return value

    return max(legal_moves(player, board), key=lambda move: min_max(Node(player, board), 4, False))

play_othello(optimized_minimax, None)