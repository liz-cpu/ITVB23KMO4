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
    count = 1 if state != 'Stay' else 0
    for next_state in possibilities[state]:
        count += find_path_count(next_state, depth - 1)
    return count


if __name__ == '__main__':
    print(find_path_count('Stay', 10))

    # Calculate the total number of nodes and the total number of children
    total_nodes = len(possibilities)
    total_children = sum(len(children) for children in possibilities.values())

    # Calculate the branching factor
    branching_factor = total_children / total_nodes

    print("Branching Factor:", branching_factor)

