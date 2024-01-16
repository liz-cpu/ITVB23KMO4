from itertools import product

def generate_configurations(choices, num_choices):
    all_configurations = list(product(choices, repeat=num_choices))
    return all_configurations

# Set of choices
choices = {'S', 'L', 'R', 'U', 'D'}

# Number of times to choose
num_choices = 10

# Generate all configurations
configurations = generate_configurations(choices, num_choices)

# make sure no L is followed by R, U or D, and no R is followed by L, U or D etc.
new_configurations = []
for configuration in configurations:
    for i in range(len(configuration)-1):
        if configuration[i] == 'L':
            if configuration[i+1] in ['R', 'U', 'D']:
                break
        elif configuration[i] == 'R':
            if configuration[i+1] in ['L', 'U', 'D']:
                break
        elif configuration[i] == 'U':
            if configuration[i+1] in ['L', 'R', 'D']:
                break
        elif configuration[i] == 'D':
            if configuration[i+1] in ['L', 'R', 'U']:
                break
    else:
        new_configurations.append(configuration)

# remove all S's from each configuration
new_configurations = [[move for move in configuration if move != 'S'] for configuration in new_configurations]

# remove all empty configurations
new_configurations = [configuration for configuration in new_configurations if configuration]

# remove duplicates
new_configurations = list(set([tuple(configuration) for configuration in new_configurations]))

# print the number of possible paths
print(len(new_configurations))