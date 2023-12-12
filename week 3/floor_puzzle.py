import itertools

num_floors = 5
persons = ['L', 'M', 'N', 'E', 'J']

def get_valid_permutations(num_floors, persons):
    # get a list of dictionaries with all possible configurations
    configurations = [dict(zip(persons, configuration)) for configuration in itertools.permutations(range(num_floors), len(persons))]
    # filter out the invalid configurations
    for configuration in configurations:
        if is_valid_configuration(configuration, num_floors):
            yield configuration
    
def is_valid_configuration(configuration, num_floors):
    """
    Checks if the configuration is valid.
    :param configuration: a dictionary with the persons as keys and the floor numbers as values
    :param num_floors: the number of floors in the building
    """
    # Loes is not on the top floor
    if configuration['L'] == num_floors - 1:
        return False
    # Marja is not on the bottom floor
    if configuration['M'] == 0:
        return False
    # Niels is not on the top nor bottom floor
    if configuration['N'] in (0, num_floors - 1):
        return False
    # Erik is at least one floor above Marja
    if configuration['E'] <= configuration['M']:
        return False
    # Joep is at least two floors from Niels
    if abs(configuration['J'] - configuration['N']) <= 1:
        return False
    # Niels is at least two floors from Marja
    if abs(configuration['N'] - configuration['M']) <= 1:
        return False    
    return True


valid_configs = list(get_valid_permutations(num_floors, persons))
print("Valid configurations:")
print(valid_configs)
print("Written in a more readable format (only works for num_floors == len(persons)):")
print([sorted(valid_config, key=valid_config.get) for valid_config in valid_configs])

