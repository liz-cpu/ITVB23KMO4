import random

import config as cf

grid = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

"""
top left of the grid is (0, 0)

a state (x, y, action) is a combination of current position (x,y) and
last/previous action
where: 0 <= x,y <= cf.SIZE - 1 and action is one of {'L', 'R', 'U', 'D', 'S'}
("L"eft, "R"ight, "U"p, "D"own, "S"tay)

standard 2d list indexing
"""


class Distribution(dict):
    """
    The Distribution class extends a Python dictionary.

    :extends: dict
    """

    def __missing__(self, key: str) -> int:
        """
        If the key is missing, return probability 0.

        :param key: The key to check.
        :type key: str
        :return: The probability of the key.
        :rtype: int
        """
        return 0

    def renormalize(self):
        """
        Scale all the probabilities so that they sum up to 1.
        Renormalization is necessary for positions at borders/in corners.
        """
        normalization_constant = sum(self.values())
        for key in self.keys():
            self[key] /= normalization_constant


def get_all_states() -> list[tuple[int, int, str]]:
    """
    Returns a (long) list of all possible states (position and previous action) ex. (7, 7, 'S').
    We need this in Viterbi (1065 states).

    :return: A list of all possible states.
    :rtype: list[tuple[int, int, str]]
    """
    all_states: list[tuple[int, int, str]] = []
    for x in range(cf.SIZE):
        for y in range(cf.SIZE):
            possible_prev_actions = ['L', 'R', 'U', 'D', 'S']

            if x == 0:  # previous action could not have been to go right
                possible_prev_actions.remove('R')
            if x == cf.SIZE - 1:  # could not have gone left
                possible_prev_actions.remove('L')
            if y == 0:  # could not have gone down
                possible_prev_actions.remove('D')
            if y == cf.SIZE - 1:  # could not have gone up
                possible_prev_actions.remove('U')

            for action in possible_prev_actions:
                all_states.append((x, y, action))
    return all_states


def transition_model(state: tuple[int, int, str]) -> Distribution:
    """
    Given a state (position and previous action),
    return a dict with keys = possible next states and values = probabilities.
    Example output: {(7, 7, 'S'): 0.2,
                     (7, 6, 'U'): 0.2,
                     (7, 8, 'D'): 0.2,
                     (6, 7, 'L'): 0.2,
                     (8, 7, 'R'): 0.2}.
    Note: top left position is (0,0).

    :param state: The state to check.
    :type state: tuple[int, int, str]
    :return: A dictionary of possible next states and their probabilities.
    :rtype: Distribution
    """
    x, y, action = state
    distr_next_states = Distribution()
    possible_moves = [('S', 0, 0), ('L', -1, 0),
                      ('R', 1, 0), ('U', 0, -1), ('D', 0, 1)]

    for move, horizontal_move, vertical_move in possible_moves:
        next_x = x + horizontal_move
        next_y = y + vertical_move

        if (next_x >= 0) and (next_x < cf.SIZE) and (next_y >= 0) and (next_y < cf.SIZE):
            if action == 'S':  # previous move was stay, 0.2 prob for all possible moves/stay
                distr_next_states[(next_x, next_y, move)] = .2
            elif move == 'S':  # previous move was a displacement, so prob for stay = 0.1
                distr_next_states[(next_x, next_y, move)] = .1
            elif action == move:  # previous move is same as next move, prob = 0.9
                distr_next_states[(next_x, next_y, move)] = .9

    # if were at border or in corner then renormalize
    distr_next_states.renormalize()
    return distr_next_states


"""
decoding: given an observation sequence, what is the most likely hidden
state sequence (that best explains the observations)
• or: what is the most likely path in the trellis
• can be used to give meaning to 'noisy' or uncertain observations
• examples: interpreting a language, determining the path of a robot
• given a sequence of ice-cream observations 3 1 3 and an HMM, the task of
the decoder is to find the most likely hidden weather sequence
• the Viterbi algorithm finds the most likely sequence of hidden states, called
the Viterbi path, given a sequence of observations in an HMM
• it is one of the most important and basic algorithms in the field of information
technology
• the original application was in signal decoding but has since been used in numerous
other applications (including speech recognition, language parsing and bio-
informatics)


"""


def get_next_state(distr_next_states) -> tuple[int, int, str]:
    """
    Given a distribution of next states, return the next state based on the
    probabilities.

    :param distr_next_states: The distribution of next states.
    :type distr_next_states: Distribution
    :return: The next state.
    :rtype: tuple[int, int, str]
    """

    return max(distr_next_states, key=distr_next_states.get)


def observation_model(state: tuple[int, int, str]) -> Distribution:
    """
    Given a state, return the distribution for its observations = positions.
    Example: state=(5, 4, 'S') returns {(5, 4): 0.2, (4, 4): 0.2, (6, 4): 0.2, (5, 3): 0.2, (5, 5): 0.2}.

    :param state: The state to check.
    :type state: tuple[int, int, str]
    :return: The distribution for the state's observations.
    :rtype: Distribution
    """
    x, y, action = state
    observed_states = Distribution()
    observation_probs = [(0, 0, 0.2), (-1, 0, 0.2),
                         (1, 0, 0.2), (0, -1, 0.2), (0, 1, 0.2)]

    for dx, dy, prob in observation_probs:
        if (x + dx >= 0) and (x + dx < cf.SIZE) and (y + dy >= 0) and (y + dy < cf.SIZE):
            observed_states[(x + dx, y + dy)] = prob

    observed_states.renormalize()
    return observed_states


def Viterbi(all_possible_states: list[tuple[int, int, str]], observations: list[tuple[int, int]]) -> list[tuple[int, int, str]]:
    """
    Given a list of all possible states and a list of observations,
    return the most likely path (list of states) that explains the observations.

    :param all_possible_states: A list of all possible states.
    :type all_possible_states: list[tuple[int, int, str]]
    :param observations: A list of observations.
    :type observations: list[tuple[int, int]]
    :return: The most likely path that explains the observations.
    :rtype: list[tuple[int, int, str]]
    """
    max_prob_matrix = [[0 for x in range(len(observations))] for y in range(
        len(all_possible_states))]
    backpointer_matrix = [
        [0 for x in range(len(observations))] for y in range(len(all_possible_states))]

    for i, state in enumerate(all_possible_states):
        x, y, action = state
        max_prob_matrix[i][0] = transition_model(
            state)[(x, y, action)] * observation_model(state)[observations[0]]
        backpointer_matrix[i][0] = 0

    for t in range(1, len(observations)):
        for i, state in enumerate(all_possible_states):
            x, y, action = state
            # Calculate the max probability for each state
            max_prob_matrix[i][t] = max([max_prob_matrix[j][t - 1] * transition_model(state)[all_possible_states[j]]
                                        * observation_model(state)[observations[t]] for j in range(len(all_possible_states))])
            backpointer_matrix[i][t] = max([max_prob_matrix[j][t - 1] * transition_model(state)[
                                           all_possible_states[j]] * observation_model(state)[observations[t]] for j in range(len(all_possible_states))])

    max_prob = max([max_prob_matrix[i][len(observations) - 1]
                   for i in range(len(all_possible_states))])

    for i in range(len(all_possible_states)):
        if max_prob_matrix[i][len(observations) - 1] == max_prob:
            max_prob_index = i

    path = [all_possible_states[max_prob_index]]

    for t in range(len(observations) - 1, 0, -1):
        path.insert(
            0, all_possible_states[backpointer_matrix[max_prob_index][t]])
        max_prob_index = backpointer_matrix[max_prob_index][t]

    return path


def load_data(filename):
    states = []
    observed_path = []

    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip()
            parts = line.split()

            prev_action = parts[0]

            # get real position
            string_xy = parts[1].split(',')
            real_x = int(string_xy[0])
            real_y = int(string_xy[1])
            states.append((real_x, real_y, prev_action))

            # get observed position
            if parts[2] == 'missing':
                observed_path.append(None)
            else:
                string_xy = parts[2].split(',')
                observed_x = int(string_xy[0])
                observed_y = int(string_xy[1])
                observed_path.append((observed_x, observed_y))

    return states, observed_path


def move_robot(app, start):
    # plot a fully random path for demonstration
    # start[0]=x and start[1]=y
    """
    prev = start
    for i in range(100):
        dir = random.choice(['L', 'R', 'U', 'D'])
        match dir:
            case 'L': current = prev[0]-1, prev[1]
            case 'R': current = prev[0]+1, prev[1]
            case 'D': current = prev[0], prev[1]-1
            case 'U': current = prev[0], prev[1]+1

        # check if new position is valid
        if (current[0] >= 0 and current[0] <= cf.SIZE-1 and current[1] >= 0 and current[1] <= cf.SIZE-1):
            app.plot_line_segment(
                prev[0], prev[1], current[0], current[1], color=cf.ROBOT_C)
            app.pause()
            app.plot_line_segment(
                prev[0], prev[1], current[0], current[1], color=cf.PATH_C)
            prev = current
            app.pause()

    app.plot_node(current, color=cf.ROBOT_C)
    """

    # plot a path based on the Viterbi algorithm
    all_possible_states = get_all_states()
    observations = load_data('observations_v2.txt')[1]
    path = Viterbi(all_possible_states, observations)

    prev = start
    for state in path:
        app.plot_line_segment(prev[0], prev[1], state[0],
                              state[1], color=cf.ROBOT_C)
        app.pause()
        app.plot_line_segment(prev[0], prev[1], state[0],
                              state[1], color=cf.PATH_C)
        prev = state
        app.pause()

    app.plot_node(prev, color=cf.ROBOT_C)
