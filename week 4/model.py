import random

import config as cf

# Global variable
grid: list[list[int]] = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

"""
(x, y) = (0, 0) is the top left of the grid

a state (x, y, action) is a combination of current position (x,y) and last/previous action
where: 0 <= x,y <= cf.SIZE - 1 and action is one of {'L', 'R', 'U', 'D', 'S'}
"""


class Distribution(dict):
    """
    The Distribution class extends a Python dictionary.

    Methods:
    - __missing__: Returns probability 0 if the key is missing.
    - renormalize: Scales all the probabilities so that they sum up to 1.
    """

    def __missing__(self, key: tuple[int, int, str]) -> float:
        """
        Returns probability 0 if the key is missing.

        :param tuple[int, int, str] key: The key to check.
        :return: The probability (always 0).
        :rtype: float
        """
        return 0

    def renormalize(self) -> None:
        """
        Scales all the probabilities so that they sum up to 1.
        """
        normalization_constant = sum(self.values())
        for key in self.keys():
            self[key] /= normalization_constant


def get_all_states() -> list[tuple[int, int, str]]:
    """
    Returns a list of all possible states (position and previous action).

    :return: list of all possible states.
    :rtype: list[tuple[int, int, str]]
    """
    all_states = []
    for x in range(cf.SIZE):
        for y in range(cf.SIZE):
            possible_prev_actions = ['L', 'R', 'U', 'D', 'S']

            if x == 0:
                possible_prev_actions.remove('R')
            if x == cf.SIZE - 1:
                possible_prev_actions.remove('L')
            if y == 0:
                possible_prev_actions.remove('D')
            if y == cf.SIZE - 1:
                possible_prev_actions.remove('U')

            for action in possible_prev_actions:
                all_states.append((x, y, action))
    return all_states


def transition_model(state: tuple[int, int, str]) -> Distribution:
    """
    Given a state (position and previous action), return a distribution for possible next states.

    Example output: {
        (7, 7, 'S'): 0.2,
        (7, 6, 'U'): 0.2,
        (7, 8, 'D'): 0.2,
        (6, 7, 'L'): 0.2,
        (8, 7, 'R'): 0.2
    }

    :param tuple[int, int, str] state: Current state (position and previous action).
    :return: Distribution of possible next states and their probabilities.
    :rtype: Distribution
    """
    x, y, action = state
    distr_next_states = Distribution()
    possible_moves = [('S', 0, 0), ('L', -1, 0),
                      ('R', 1, 0), ('U', 0, -1), ('D', 0, 1)]

    for move, hor_mov, vert_move in possible_moves:
        next_x = x + hor_mov
        next_y = y + vert_move

        if (0 <= next_x < cf.SIZE) and (0 <= next_y < cf.SIZE):
            if action == 'S':
                distr_next_states[(next_x, next_y, move)] = 0.2
            elif move == 'S':
                distr_next_states[(next_x, next_y, move)] = 0.1
            elif action == move:
                distr_next_states[(next_x, next_y, move)] = 0.9

    distr_next_states.renormalize()
    return distr_next_states


def get_next_state(distr_next_states) -> None:
    pass


def observation_model(state: tuple[int, int, str]) -> Distribution:
    """
    Given a state, return the distribution for its observations (positions).

    :param tuple[int, int, str] state: Current state.
    :return: Distribution of possible observed positions and their probabilities.
    :rtype: Distribution
    """
    x, y, action = state
    observed_states = Distribution()
    observation_probs = [(0, 0, 0.2), (-1, 0, 0.2),
                         (1, 0, 0.2), (0, -1, 0.2), (0, 1, 0.2)]

    for dx, dy, prob in observation_probs:
        if (0 <= x + dx < cf.SIZE) and (0 <= y + dy < cf.SIZE):
            observed_states[(x + dx, y + dy)] = prob

    observed_states.renormalize()
    return observed_states


def viterbi(all_possible_states, observations):
    pass


def load_data(filename: str) -> tuple[list, list]:
    """
    Loads data from a file and returns states and observed path.

    :param str filename: Name of the file.
    :return: tuple containing lists of states and observed path.
    :rtype: tuple[list[tuple[int, int, str]], list[Optional[tuple[int, int]]]]
    """
    states = []
    observed_path = []

    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip()
            parts = line.split()

            prev_action = parts[0]

            string_xy = parts[1].split(',')
            real_x = int(string_xy[0])
            real_y = int(string_xy[1])
            states.append((real_x, real_y, prev_action))

            if parts[2] == 'missing':
                observed_path.append(None)
            else:
                string_xy = parts[2].split(',')
                observed_x = int(string_xy[0])
                observed_y = int(string_xy[1])
                observed_path.append((observed_x, observed_y))

    return states, observed_path


def move_robot(app: any, start: tuple[int, int]) -> None:
    """
    Plots a fully random path for demonstration.

    :param any app: Application object.
    :param tuple[int, int] start: Initial position.
    """
    prev = start
    for i in range(100):
        direction = random.choice(['L', 'R', 'U', 'D'])
        match direction:
            case 'L': current = prev[0] - 1, prev[1]
            case 'R': current = prev[0] + 1, prev[1]
            case 'D': current = prev[0], prev[1] - 1
            case 'U': current = prev[0], prev[1] + 1

        if (0 <= current[0] <= cf.SIZE - 1) and (0 <= current[1] <= cf.SIZE - 1):
            app.plot_line_segment(
                prev[0], prev[1], current[0], current[1], color=cf.ROBOT_C)
            app.pause()
            app.plot_line_segment(
                prev[0], prev[1], current[0], current[1], color=cf.PATH_C)
            prev = current
            app.pause()

    app.plot_node(current, color=cf.ROBOT_C)
