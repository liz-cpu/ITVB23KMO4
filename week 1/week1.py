class NumbrixBoard(object):
    def __init__(self, hints: list[list[str]]):
        self.board = hints
        self.size = len(hints)
        self.start = self.find_in_board("1")
        self.end = self.find_in_board(str(self.size**2))

    def __str__(self):
        cols = len(self.board[0])
        line = f'┌{"───┬" * (cols - 1)}───┐\n'
        separator = f'├{"───┼" * (cols - 1)}───┤\n'
        end_line = f'└{"───┴" * (cols - 1)}───┘'

        rows = [f'│ {" │ ".join(row)} │\n' for row in self.board]

        return line + separator.join(rows) + end_line

    def __repr__(self):
        return f"NumbrixBoard(hints={self.board})"

    def find_in_board(self, num: str) -> tuple[int, int] | None:
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == num:
                    return (i, j)
        return None

    def get_neighbors(self, i: int, j: int) -> list[tuple[int, int]]:
        neighbors = []
        for x, y in [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]:  # O(1).
            if 0 <= x < self.size and 0 <= y < self.size:
                neighbors.append((x, y))
        return neighbors

    def dfs(
        self,
        visited: list[tuple[int, int]] = [],
        num: int = 1,
        coords: tuple[int, int] = None,
        current_board: list[list[str]] = None,
    ) -> bool:
        i, j = coords or self.start
        current_board = current_board or [
            [self.board[i][j] for j in range(self.size)] for i in range(self.size)
        ]  # deep copy n^2
        for x, y in self.get_neighbors(i, j):
            if (x, y) in visited:
                continue
            if (x, y) == self.end and num == self.size**2 - 1:
                return current_board
            neigh_num = int(self.board[x][y]) if self.board[x][y] != " " else num + 1
            if (x, y) not in visited and neigh_num == num + 1:
                current_board[x][y] = str(num + 1)
                visited.append((x, y))
                if b := self.dfs(visited, num + 1, (x, y), current_board):
                    return b
                visited.pop()
        return False

    @classmethod
    def print_2d(cls, board: list[list[str]]) -> str:
        cols = len(board[0])
        line = f'┌{"───┬" * (cols - 1)}───┐\n'
        separator = f'├{"───┼" * (cols - 1)}───┤\n'
        end_line = f'└{"───┴" * (cols - 1)}───┘'

        rows = [f'│ {" │ ".join(row)} │\n' for row in board]
        if board[2][1] == "8":
            print("here")
        print(line + separator.join(rows) + end_line)


b = NumbrixBoard([["1", " ", " "], [" ", "5", " "], [" ", " ", "9"]])

print(NumbrixBoard.print_2d(b.dfs()))
