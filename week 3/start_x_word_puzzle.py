# vragen:
# 1. Vragen m.b.t. variabelen:
#   a. Wat zijn hier de variabelen en hoeveel zijn er?
#       de lege plekken in de puzzel, dus 11
#   b. Wat zijn de domeinen van de variabelen?
#       woorden met de juiste lengte
#   c. Hoe kun je de variabelen representeren in code?
#       getallen van 1 t/m 11
#   d. Wat is de beste volgorde (prioriteit) voor het testen van variabelen?
#       woorden met veel kruisende woorden
# 2. Vragen m.b.t. constraints:
#   a. Wat zijn de binaire constraints en hoeveel zijn er?
#       verticaal en horizontaal
#   b. Hoe kun je de binaire constraint representeren in code?
#       zou met een 'H' en 'V' kunnen
#   c. Wat betekent het dat een waarde voor een variabele 'arc-consistent' is?
#       dat ze voldoen aan de constraints, dus de waarden welke niet kunnen voldoen aan de constraints worden verwijderd
#   d. Hoe zinvol is het om arc-consistency toe te passen?
#       redelijk zinvol, want dan worden de domeinen kleiner en hoeft er dus minder permutaties getest te worden
# 3. Is het mogelijk om alle oplossingen te vinden?
#   zeker is dat mogelijk, alleen zou het langer duren omdat er meer getest moet worden.

# set word_info, dict with key = variable, value = list of charcount followed by lists with [other variable, overlap index]
word_info = {
    1: [4, [2, 1]],
    2: [11, [1, 6]],
    3: [5, [9, 2], [10, 4]],
    4: [5, [5, 3], [1, 4]],
    5: [6, [11, 4]],
    6: [5, [9, 1], [10, 3]],
    7: [5, [11, 3]],
    8: [4, [11, 3]],
    9: [5, [3, 0], [6, 3]],
    10: [6, [3, 0], [6, 3]],
    11: [7, [5, 0], [7, 3], [8, 6]]
}

# assignment is a dict var:value, where value is a word but can be None
assignment = dict()
for i in range(1,12):
    assignment[i] = None

found_assignments = []

def make_domain(word_info):
    # domain is a dict var:value and value is a set of words with correct length
    words = []
    with open('words_NL.txt') as f:
        for line in f:
            words.append(line.strip())

    domain = dict()
    for i in [4,5,6,7,11]:
        domain[i] = set()
    for word in words:
        if len(word) in domain:
            domain[len(word)].add(word)
    domain_words = dict()
    for word in word_info.keys():
        domain_words[word] = domain[word_info[word][0]]
    return domain_words

def make_arc_consistent(domain):
    # make domain arc-consistent
    for key in domain.keys():
        for other_key in domain.keys():
            if other_key != key:
                for overlap in word_info[key][1:]:
                    for other_overlap in word_info[other_key][1:]:
                        if overlap[0] == other_key and other_overlap[0] == key:
                            for word in domain[key].copy():
                                if word[overlap[1]] not in [other_word[other_overlap[1]] for other_word in domain[other_key]]:
                                    domain[key].remove(word)
    return domain

def valid(assignments):
    # check if all assignments are valid
    for key in assignments.keys():
        if assignments[key] != None:
            for other_key in assignments.keys():
                if other_key != key and assignments[other_key] != None:
                    for overlap in word_info[key][1:]:
                        if assignments[key][overlap[1]] != assignments[other_key][word_info[other_key][1][1]]:
                            return False
    return True    

# dict represents a tree: a dictionary variable:value
def solve(domain, assignments):
    # give first variable with no assignment the first word in its domain that satisfies the constraints
    # if no such word exists, return False
    for key in assignments.keys():
        if assignments[key] == None:
            for word in domain[key]:
                assignments[key] = word
                if valid(assignments):
                    result = solve(domain, assignments)
                    if result != False:
                        return result
                assignments[key] = None
            return False
    # # below code is for finding all solutions, this is not needed and would take too long 
    # if None not in assignments.values():
    #     found_assignments.append(assignments.copy())
    #     return False
    return assignments


print("total words in all domains: " + str(sum([len(domain) for domain in make_domain(word_info).values()])))
new_domain = make_arc_consistent(make_domain(word_info))
print("total words in all arc-consistent domains: " + str(sum([len(domain) for domain in new_domain.values()])))
print("Found assignments: ")
print(solve(new_domain, assignment))
print("Number of solutions found: " + str(len(found_assignments)))