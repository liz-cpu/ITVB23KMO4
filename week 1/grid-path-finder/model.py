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
        if (
            0 <= x + i < cf.SIZE
            and 0 <= y + j < cf.SIZE
            and get_grid_value((x + i, y + j)) != "b"
        ):
            neighbors.append((x + i, y + j))
    return neighbors


def search(app, start, goal):
    if app.alg.get() == "UC":
        return ucs(app, start, goal)
    return a_star(app, start, goal)

def h(start, goal):
    return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)


def ucs(app, start, goal):
    frontier = PriorityQueue()
    visited = set()
    frontier.put(start, 0)
    came_from = {}  # To store the parent node for each explored node
    cost_so_far = {start: 0}  # To store the cost to reach each explored node

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            # Reconstruct the path and plot it
            path = reconstruct_path(came_from, start, goal)
            for node in path:
                app.plot_node(node, color=cf.FINAL_C)
                app.pause()
            return

        visited.add(current)

        for next_node in get_neighbors(current):
            new_cost = cost_so_far[current] + 1

            if next_node not in visited and (next_node not in cost_so_far or new_cost < cost_so_far[next_node]):
                cost_so_far[next_node] = new_cost
                frontier.put(next_node, new_cost)
                came_from[next_node] = current
                app.plot_node(next_node, color=cf.PATH_C)
                app.pause()
    return


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]

    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def a_star(app, start, goal):
    """
    A* Search
    Heuristic search algorithm
    """
    frontier = PriorityQueue()
    visited = set()
    frontier.put(start, 0)
    came_from = {}  # To store the parent node for each explored node
    cost_so_far = {start: 0}  # To store the cost to reach each explored node

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            # Reconstruct the path and plot it
            path = reconstruct_path(came_from, start, goal)
            for node in path:
                app.plot_node(node, color=cf.FINAL_C)
                app.pause()
            return

        visited.add(current)

        for next_node in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_node not in visited and (next_node not in cost_so_far or new_cost < cost_so_far[next_node]):
                cost_so_far[next_node] = new_cost
                priority = new_cost + h(next_node, goal)  # A* uses the sum of cost and heuristic as priority
                frontier.put(next_node, priority)
                came_from[next_node] = current
                app.plot_node(next_node, color=cf.PATH_C)
                app.pause()

    return
