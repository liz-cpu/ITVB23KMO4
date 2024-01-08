possibilities: dict[str, list[str]] = {
    'Stay': ['Left', 'Up', 'Down', 'Right'],
    'Left': ['Left', 'Stay'],
    'Right': ['Right', 'Stay'],
    'Up': ['Up', 'Stay'],
    'Down': ['Down', 'Stay']
}


def find_path_count(state: str, depth: int) -> int:
    if depth == 0:
        return 1
    count = int(state != 'Stay')
    for next_state in possibilities[state]:
        count += find_path_count(next_state, depth - 1)
    return count


if __name__ == '__main__':
    print(find_path_count('Stay', 10))

    total_branches = 0
    for state, moves in possibilities.items():
        total_branches += len(moves)

    average_branching_factor = total_branches / len(possibilities)

    print(f"Average Branching Factor: {average_branching_factor}")