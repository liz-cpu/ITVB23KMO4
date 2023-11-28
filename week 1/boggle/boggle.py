import random

boardSize = 4
found = []


class Node:
    def __init__(self, x, y, val):
        self.x, self.y, self.val = x, y, val

    def __repr__(self):
        return self.val


# begin node, visited set, board, found chars to form a word, words and prefixes
def dfs(n, v, b, ch, ws, pf):
    ch += n.val
    if ch in ws and ch in pf:
        found.append(ch)
    elif ch in ws:
        return found.append(ch)
    if ch not in pf:
        return False
    v.add(n)
    for child in successors(n, b):
        if child not in v and dfs(child, v, b, ch, ws, pf):
            return True


def gen_board(n):
    # return [[Node(0, 0, "p"), Node(0, 1, "i"), Node(0, 2, "e"), Node(0, 3, "t")], [Node(1, 0, "g"), Node(1, 1, "s"), Node(1, 2, "a"), Node(1, 3, "t")], [Node(2, 0, "j"), Node(2, 1, "a"), Node(2, 2, "u"), Node(2, 3, "s")], [Node(3, 0, "e"), Node(3, 1, "u"), Node(3, 2, "i"), Node(3, 3, "s")]]
    return [[Node(x, y, random.choice("abcdefghijklmnopqrstuvwxyz")) for y in range(n)] for x in range(n)]


def gen_prefix_sets(file_name):
    # returns 2 sets, the first with all prefixes and the second with all the possible words
    ws = open(file_name).readlines()
    return set().union(*[set(wd.strip()[0:i] for i in range(0, len(wd) - 1)) for wd in ws]), \
           set(wd.strip() for wd in ws)


def successors(n, b):
    return [b[(n.x + x) % len(b)][(n.y + y) % len(b)] for x, y in zip([0, 1, 0, -1], [1, 0, -1, 0])]


board = gen_board(boardSize)
prefs, words = gen_prefix_sets("words_NL.txt")
for row in board:
    print(row)
    for node in row:
        dfs(node, set(), board, "", words, prefs)

print(found)
