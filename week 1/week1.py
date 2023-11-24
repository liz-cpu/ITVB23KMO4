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
        return  not any(p.issubset(items_on_shore) for p in self.prohibited)

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


def dfs(node: Node, goal: Node, visited: list = []) -> Node:
    if node == goal:
        return node
    if node in visited or not node.is_valid():
        return None
    visited.append(node)
    for child in node.get_children():
        result = dfs(child, goal, visited)
        if result is not None:
            return result
    return None

def bfs(node: Node, goal: Node) -> Node:
    visited = []
    queue = [node]
    while len(queue) > 0:
        current = queue.pop(0)
        if current == goal:
            return current
        if current in visited or not current.is_valid():
            continue
        visited.append(current)
        for child in current.get_children():
            queue.append(child)
    return None

def print_solution(node: Node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()
    for node in path:
        print(node)

print("DFS:")
print_solution(dfs(Node(set("🐐🥬🐺"), set(), True), Node(set(), set("🐐🥬🐺"), False)))
print("BFS:")
print_solution(bfs(Node(set("🐐🥬🐺"), set(), True), Node(set(), set("🐐🥬🐺"), False)))