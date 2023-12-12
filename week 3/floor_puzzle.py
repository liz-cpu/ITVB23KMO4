"""
TASK 1: FLOOR PUZZLE

Lynette, Mehmet, Nina, Eduardo, and Jovi live in a building with 5 floors, each on their own floor.
Lynette does not live on the top floor.
Mehmet does not live on the ground floor.
Nina does not live on the ground floor or the top floor.

Eduardo lives at least one floor higher than Mehmet.
Jovi does not live on a floor one higher or lower than Nina.
Nina does not live on a floor one higher or lower than Mehmet.

Where does everyone live?

You can generate all permutations and test them one by one. This can be done with:

`for (L, M, N, E, J) in list(itertools.permutations(floors))`

Of course, the order in which you conduct the tests affects performance.
"""

import itertools

def test_permutations(lynette, mehmet, nina, eduardo, jovi, floors):
    top = max(floors)
    ground = min(floors)
    if lynette == top:
        return False
    if mehmet == ground:
        return False
    if nina == ground or nina == top:
        return False
    if eduardo <= mehmet:
        return False
    if jovi == nina + 1 or jovi == nina - 1:
        return False
    if nina == mehmet + 1 or nina == mehmet - 1:
        return False
    return True


floors = (1, 2, 3, 4, 5)
for (L, M, N, E, J) in list(itertools.permutations(floors)):
    if test_permutations(L, M, N, E, J, floors):
        print("Found a solution! ")
        print("Lynette: " + str(L))
        print("Mehmet: " + str(M))
        print("Nina: " + str(N))
        print("Eduardo: " + str(E))
        print("Jovi: " + str(J))
        print()
        print(f"Solution! [L: {L}, M: {M}, N: {N}, E: {E}, J: {J}]")
