import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP
# Ramon's version

City = namedtuple('City', 'x y')


def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)


def try_all_tours(cities: frozenset) -> list:
    """
    Generate and test all tours of the cities and pick the shortest one.
    """
    tours = alltours(cities)
    print(min(tours, key=tour_length))
    return min(tours, key=tour_length)


def nearest_neighbor(cities):
    city_set = set(cities)
    nodes = [city_set.pop()]
    while len(city_set) > 0:
        shortest = (City, None)
        for c in city_set:
            dist = distance(nodes[-1], c)
            if shortest[1] is None or dist < shortest[1]:
                shortest = (c, dist)
        nodes += [shortest[0]]
        city_set.remove(shortest[0])
    return nodes


def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities))
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]


def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i - 1]) for i in range(len(tour)))


def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(314)  # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

def make_cities(n: int, width: int = 1000, height: int = 1000):
    """
    Makes a set of n cities, each with random coordinates within a rectangle (width x height).
    The current system time is used as a seed
    note: if we used the same seed, we'd get the same set of cities
    """
    random.seed("hanze")
    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))


def plot_tour(tour):
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')  # blue circle markers, solid line style
    plt.axis('scaled')  # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()


def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting...")
    plot_tour(optimize_tour(tour))


def optimize_tour(tour):
    segments = [[tour[s % len(tour)], tour[(s + 1) % len(tour)]] for s in range(len(tour))] # list of segments
    optimal = False
    while not optimal:
        optimal = True
        for s in segments:
            index = segments.index(s)
            # check for intersections and optimize them
            for i in range(index + 1, len(segments)):
                # if intersected, swap the 2nd city of the 1st segment with the 1st city of the 2nd segment
                old = distance(s[0], s[1]) + distance(segments[i][0], segments[i][1])
                new = distance(s[0], segments[i][0]) + distance(segments[i][1], s[1])
                if old > new:
                    optimal = False # if there is an intersection, the tour is not optimal
                    s[1], segments[i][0] = segments[i][0], s[1]
                    for sw in segments[index + 1:i]:
                        sw[0], sw[1] = sw[1], sw[0]
                    segments[index + 1:i] = segments[index + 1:i][::-1] # reverse the order of the segments
    # sort by connecting 2nd city to 1st city of every segment
    return [s[0] for s in segments]


# give a demo with 10 cities using brute force
plot_tsp(nearest_neighbor, make_cities(500))
