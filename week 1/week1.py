import sys
import colorama as color
color.init(autoreset=True)
sys.path.insert(0, '../')


class Node(object):
    prohibited = [set("🐐🥬"), set("🐐🐺")]

    def __init__(self, top: set[chr], bottom: set[chr], farmer: bool, parent: bool = None):
        self.top = top
        self.bottom = bottom
        self.farmer = farmer
        self.parent = parent

    def __str__(self):
        return "".join(self.top) + ("👨|" if self.farmer else "|👨") + "".join(self.bottom)

    def __eq__(self, __value: object) -> bool:
        return self.top == __value.top and self.bottom == __value.bottom and self.farmer == __value.farmer

    def move(self, item: chr):
        if self.farmer:
            self.top.remove(item)
            self.bottom.add(item)
        else:
            self.bottom.remove(item)
            self.top.add(item)
        self.farmer = not self.farmer

    def is_valid(self) -> bool:
        items_on_shore = self.bottom if self.farmer else self.top
        return not any(p.issubset(items_on_shore) for p in self.prohibited)

    def get_children(self) -> list:
        children = []
        for item in self.top if self.farmer else self.bottom:
            child = Node(self.top.copy(), self.bottom.copy(),
                         self.farmer, self)
            child.move(item)
            children.append(child)
        child = Node(self.top.copy(), self.bottom.copy(),
                     not self.farmer, self)
        children.append(child)
        return children


def dfs(node: Node, goal: Node, path: list = []) -> Node:
    paths = []
    if node == goal:
        path.append(node)
        paths.append(path.copy())
        path.pop()
    elif node not in path and node.is_valid():
        path.append(node)
        for child in node.get_children():
            paths += dfs(child, goal, path)
        path.pop()
    return paths


def print_paths(list_of_paths: list[list[Node]]):
    for idx, path in enumerate(list_of_paths):
        print(color.Fore.GREEN + "Path: " + str(idx + 1))
        print_path(path)


def print_path(path: list[Node]):
    for node in path:
        print(node)


def river_crossing(start_state: str) -> str:
    d = {"G": "🐐", "C": "🥬", "W": "🐺"}
    top, bottom = start_state.split("|")
    farmer = "F" in top.upper()
    top, bottom = top.upper().replace("F", ""), bottom.upper().replace("F", "")
    top, bottom = [d[c] for c in top], [d[c] for c in bottom]
    start_node = Node(set(top), set(bottom), farmer)
    goal_node = Node(set(), set(top + bottom), farmer)
    result = dfs(start_node, goal_node)
    if result is None:
        print(color.Fore.RED + "No solution found")
    print_paths(result)


# import the words from the file
words = []
with open("boggle/words_EN.txt") as f:
    for line in f.readlines():
        words.append(line.strip())


class BoggleGame(object):
    words: set[str]
    board: list[list[chr]]
    prefixes: set[str]

    def __init__(self, words: list[str], board: list[list[chr]]):
        self.words = set(words)
        self.board = board
        self.prefixes = set()
        for word in self.words:
            for i in range(len(word)):
                self.prefixes.add(word[:i+1])

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.board])

    def find_neighbors(self, i: int, j: int) -> list[tuple[int, int]]:
        return [(x, y) for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                if 0 <= x < len(self.board) and 0 <= y < len(self.board[0])]

    @classmethod
    def from_str(cls, s: str):
        return cls(words, [[c for c in row] for row in s.split("\n")])

    def dfs(self, i: int, j: int, visited: list[tuple[int, int]], word: str) -> str:
        if (word not in self.prefixes) and (word not in self.words):
            return None
        for x, y in self.find_neighbors(i, j):
            if (x, y) not in visited:
                visited.append((x, y))
                new_word = word + self.board[x][y]
                deeper = self.dfs(x, y, visited, new_word)
                if deeper is not None:
                    return deeper
                if deeper is None and new_word in self.words:
                    return new_word
                visited.pop()
        return None

    def find_words(self) -> list[str]:
        found_words = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if (res := self.dfs(i, j, [(i, j)], self.board[i][j])) is not None:
                    found_words.append(res)
        return found_words


class NumbrixBoard(object):
    def __init__(self, hints: list[list[str]]):
        self.board = hints
        self.size = len(hints)
        self.start = self.find_in_board("1")
        self.end = self.find_in_board(str(self.size**2))

    def __str__(self):
        result = ""
        for row in self.board:
            result += "|".join(str(cell).center(3) for cell in row) + "\n"
            result += "-" * (self.size * 4 - 1) + "\n"
        return result

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

    @classmethod
    def from_str(cls, board: str):
        lines = board.strip().split('\n')
        b = [[cell if cell != '0' else ' ' for cell in line.split()]
             for line in lines]
        return cls(b)

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
        ]
        for x, y in self.get_neighbors(i, j):
            if (x, y) in visited:
                continue
            if (x, y) == self.end and num == self.size**2 - 1:
                return current_board
            neigh_num = int(
                self.board[x][y]) if self.board[x][y] != " " else num + 1
            if (x, y) not in visited and neigh_num == num + 1:
                current_board[x][y] = str(num + 1)
                visited.append((x, y))
                if b := self.dfs(visited, num + 1, (x, y), current_board):
                    return b
                visited.pop()
        return False


if __name__ == "__main__":
    try:
        game = sys.argv[1]
    except IndexError:
        print("No game specified")
        exit(1)
    if game == "river":
        river_crossing(sys.argv[2])
    elif game == "boggle":
        boggle = BoggleGame.from_str(sys.argv[2])
        print(boggle)
        print("Found words:")
        print(boggle.find_words())
    elif game == "numbrix":
        board = NumbrixBoard.from_str(sys.argv[2])
        print(board)
        print(board.dfs())
    else:
        print("Invalid game")
