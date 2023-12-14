"""
TASK 2: CROSSWORD PUZZLE

Below is a grid for a crossword puzzle. The goal is to fill the grid with words
to generate a crossword puzzle. Also given is a list of words that can be used.
This list, words_NL.txt, can be found on Blackboard. We can view this problem
as a Constraint Satisfaction Problem (CSP).

Questions regarding variables:
    a. What are the variables here, and how many are there?
        > The variables are the length of the words, which in this case are
        > 4, 5, 6, 7, 8, 11 for a total of 6 variables.
    b. What are the domains of the variables?
        > The domains are the words that can be used, which are given in the
        > file words_NL.txt.
    c. How can you represent the variables in code?
        > The variables can be represented as a dictionary with the length of
        > the words as keys and the words as values. These words in turn can
        > be represented as a set, because the order of the words does not
        > matter.
    d. What is the best order (priority) for testing variables?
        > It isge nerally best to test the variables with the smallest domain
        > first, and then try to fail fast to prune the search tree. In this
        > case, the variable with the smallest domain is 11, so we should
        > start with that one.

Questions regarding constraints:
    a. What are the binary constraints, and how many are there?

    b. How can you represent the binary constraint in code?

    c. What does it mean for a value for a variable to be 'arc-consistent'?

    d. How meaningful is it to apply arc-consistency?


    Is it possible to find all solutions?
"""

import os
import itertools

def load_words() -> set:
    """
    Load a set of words from the file words_NL.txt. The file contains one word
    per line.

    :return: a set of words
    :rtype: set
    """
    words = set()
    with open(os.path.join(os.getcwd(), "words_NL.txt"), "r") as f:
        for line in f:
            words.add(line.strip())
    return words

def make_domain() -> dict:
    """
    Create a domain for the crossword puzzle. The domain is a dictionary
    variable:value, where variable is a number between 1 and 11, and value is
    a set of words with the correct length.

    :return: a domain for the crossword puzzle
    :rtype: dict
    """
    domain = dict()
    words = load_words()
    domain_size = dict()
    for i in [4, 5, 6, 7, 8, 11]:
        domain_size[i] = {word for word in words if len(word) == i}
    return domain


def valid(key, a):
    # key = variable, a is a dict var:value, where value is a word but can be None
    match key:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            pass
        case 10:
            pass
        case 11:
            pass
    return False


def make_arc_consistent(domain, a, key):
    # make variable x arc consistent with variable y
    # meaning: if words x and y overlap, and if word x = a[key] has no match in y.domain,
    pass


# dict represents a tree: a dictionary variable:value
def solve(domain, assign, unassigned_vars):
    pass
