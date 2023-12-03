import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')


def distance(A: City, B: City) -> float:
    return math.hypot(A.x - B.x, A.y - B.y)


def try_all_tours(cities: frozenset) -> list:
    """
    Generate and test all tours of the cities and pick the shortest one.
    """
    tours = alltours(cities)
    return min(tours, key=tour_length)


def alltours(cities: frozenset) -> list[list]:
    """
    Return a list of tours (a list of lists), each tour a permutation of cities,
    and each one starting with the same city
    note: cities is a set, sets don't support indexing
    """
    start = next(iter(cities))
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]


def tour_length(tour: list) -> float:
    """
    Calculate the total length of the tour
    """
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))


def make_cities(n: int, width: int = 1000, height: int = 1000):
    """
    Makes a set of n cities, each with random coordinates within a rectangle (width x height).
    The current system time is used as a seed
    note: if we used the same seed, we'd get the same set of cities
    """
    random.seed("hanze")
    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))


def nearest_neighbour(cities):
    """
    Using the nearest neighbour algorithm, find a tour starting from the first
    city and going to the nearest neighbour, etc.
    """
    cities = set(cities)  # defrost the cities
    start = next(iter(cities))  # the first city
    tour = [start]
    unvisited = cities - set([start])
    while unvisited:
        nearest = min(unvisited, key=lambda city: distance(city, tour[-1]))
        tour.append(nearest)
        unvisited.remove(nearest)
    return tour


def plot_tour(tour: list) -> None:
    """
    Plot a tour, i.e. the order in which we visit the cities in the tour.
    Cities are represented as circles centred on their coordinates, and the tour
    is shown as lines joining the cities.
    """
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled')  # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()


def plot_tsp(algorithm: callable, cities: frozenset) -> None:
    """
    Applies the given algorithm to cities, and visualises the results.
    """
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

plot_tsp(nearest_neighbour, make_cities(50))


"""
1a.
random.seed("hanze")
plot_tsp(try_all_tours, make_cities(10))
plot_tsp(nearest_neighbour, make_cities(10))


Output:
10 city tour with length 3648.9 in 0.922 secs for try_all_tours
Start plotting ...
10 city tour with length 4164.1 in 0.000 secs for nearest_neighbour
Start plotting ...

This is a 14.11% increase in length, but the algorithm is a lot faster.

======
1b.
500 city tour with length 19445.9 in 0.031 secs for nearest_neighbour

======


"""