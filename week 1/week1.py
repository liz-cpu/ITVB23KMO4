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


def dfs(node: Node, goal: Node, path: list = [], visited: list = []) -> list:
    if node == goal:
        path.append(node)
        return [path]
    if node in visited or not node.is_valid():
        return []
    visited.append(node)
    paths = []
    for child in node.get_children():
        result_paths = dfs(child, goal, path + [node], visited)
        paths.extend(result_paths)
    return paths


print("DFS:")
start_node = Node(set("🐐🐺🥬"), set(), True)
goal_node = Node(set("🐐"), set("🐺🥬"), False)

result_paths = dfs(start_node, goal_node)

if result_paths:
    for path in result_paths:
        for node in path:
            print(node)
        print("----")


def get_solution(string: str) -> str:
    top, bottom = string.split("|")
    farmer = True if "F" in top else False
    node = Node(set(top), set(bottom), farmer)
    














































































































