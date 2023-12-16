"""
# TASK 2: CROSSWORD PUZZLE

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
        > The binary constraints are the size of the words, which are given
        > in the grid.
    b. How can you represent the binary constraint in code?
        > The binary constraints can be represented as a dictionary with the
        > size of the words as keys and the words as values. These words in
        > turn can be represented as a set, because the order of the words
        > does not matter.
        > I think that the domain here qualifies as how you would represent
        > these, but I am not sure.
    c. What does it mean for a value for a variable to be 'arc-consistent'?
        > A value for a variable is arc-consistent if it is consistent with
        > the constraints of the other variables. Consider yourself to be
        > solving a jig-saw puzzle. If you have a piece that has a straight
        > edge, you can already rule out all pieces that do not have a
        > straight edge. This is because the straight edge is consistent with
        > the constraints of the other pieces.
        > This is an example of arc-consistency because you are ruling out
        > values for a variable based on the constraints of the other
        > variables.
    d. How meaningful is it to apply arc-consistency?
        > It is very meaningful to apply arc-consistency when solving crossword
        > puzzles like this one. This is because you can rule out a lot of
        > words that do not fit the constraints of the other words. You can
        > for example rule out all words that do not have a certain letter
        > at a certain position if you already know the letter at that
        > position for another word. Similarly, you can rule out all words
        > that do not fit the length of the word that you are trying to
        > solve.


    3. Is it possible to find all solutions?
        > Yes, it is possible to find all solutions. This is because the
        > constraints are very strict, and there are only 6 variables. This
        > means that the search tree is not very large, and it is possible
        > to search through the entire tree withing a reasonable amount of
        > time.

Write a program that, given a list of words, fills the grid with appropriate
words so that all constraints are met. It is convenient to first process the
list of words into data structures that represent the different domains.
The program only needs to generate words for this specific grid, so a generic
setup is not required. There are many solutions, but showing one is sufficient.

On Blackboard, you can find the file start_x_word_puzzle.py, which provides
some suggestions on how to approach it. Note that you can view it as one
grid, but also as two independent grids.
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


def valid(key: int, a: dict):
    """
    Check if a[key] is valid, given the constraints of the other variables.
    `a` is a dictionary variable:value, where value is a word but could be None.

    :param key: The variable to check 
    :type key: int
    :param a: _description_
    :type a: _type_
    :return: _description_
    :rtype: _type_
    """
    return a[key]


def make_arc_consistent(domain, a, key):
    """
    Make variable x arc consistent with variable y. Meaning: if words x and y
    overlap, and if word x = a[key] has no match in y.domain, then remove
    word x from x.domain.

    :param domain: _description_
    :type domain: _type_
    :param a: _description_
    :type a: _type_
    :param key: _description_
    :type key: _type_
    """
    # make variable x arc consistent with variable y
    # meaning: if words x and y overlap, and if word x = a[key] has no match in
    # y.domain,
    pass


# dict represents a tree: a dictionary variable:value
def solve(domain, assign, unassigned_vars):
    pass
