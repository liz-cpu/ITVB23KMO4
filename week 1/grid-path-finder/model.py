import random
import heapq
import math
import config as cf

# global var
grid = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]


class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get()) / 10 else 0


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value


def get_neighbors(node):
    neighbors = []
    x, y = node
    for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if 0 <= x+i < cf.SIZE and 0 <= y+j < cf.SIZE and get_grid_value((x+i, y+j)) != 'b':
            neighbors.append((x+i, y+j))
    return neighbors


def search(app, start, goal):
    if app.alg.get() == 'UC':
        return ucs(app, start, goal)
    return a_star(app, start, goal)

def cost(node, goal):
    return math.sqrt((goal[0]-node[0])**2 + (goal[1]-node[1])**2)

def ucs(app, start, goal) -> list[tuple[int, int]]:
    """
    Uniform Cost Search
    Non-heuristic search algorithm
    """
    frontier = PriorityQueue()
    visited = set()
    frontier.put(start, 0)
    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            return
        visited.add(current)
        for next in get_neighbors(current):
            if next not in visited:
                frontier.put(next, get_grid_value(current)+1)
                set_grid_value(next, get_grid_value(current)+1)
                app.plot_node(next, color=cf.FINAL_C)
                app.pause()
    return

def a_star(app, start, goal):
    """
    A* Search
    Heuristic search algorithm
    """
    frontier = PriorityQueue()
    visited = set()
    frontier.put(start, 0)
    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            return
        visited.add(current)
        for next in get_neighbors(current):
            if next not in visited:
                frontier.put(next, cost(next, goal))
                set_grid_value(next, get_grid_value(current)+1)
                app.plot_node(next, color=cf.FINAL_C)
                app.pause()
    return