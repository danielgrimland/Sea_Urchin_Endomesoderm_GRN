import re


# Inputs: an error message.
# Outputs: displays the error message and closes the program.
def error(error_name):
    print(error_name)
    input()
    exit()


# Inputs: a list of lists.
# Outputs: a list containing lists that are the cartesian product of all lists.
def general_prod(list_family):
    if (len(list_family) == 1):
        prod = []

        for e in list_family[0]:
            prod.append([e])

        return prod

    else:
        previous_prod = general_prod(list_family[:-1])
        new_prod = []

        for combination in previous_prod:

            for e in list_family[-1]:
                new_combination = list(combination)
                new_combination.extend([e])
                new_prod.append(list(new_combination))

        return new_prod


# Inputs: two lists of SPT objects.
# Outputs: whether all objects of list1 are in list2.
def subset_spt_lists(list1, list2):
    for spt1 in list1:
        spt1_in_list2 = False

        for spt2 in list2:
            if (spt1 == spt2):
                spt1_in_list2 == True

        if (not(spt1_in_list2)):
            return False
        
    return True


# Inputs: a list of components.
# Outputs: the same list where all elements are in tuples.
def tuplize(list):
    new_list = []
    
    for e in list:
        new_list.append((e,))
        
    return new_list


# Inputs: a tuple of ranges.
# Outputs: a list composed of all numbers within the ranges.
def generate_appearences(ranges):
    appearences = []

    for r in ranges:
        bounds = re.split("-", r)
        appearences.append(range(int(bounds[0]), int(bounds[1]) + 1))

    new_appearences = []
    
    for list in appearences:
        for e in list:
            if not(e in new_appearences):
                new_appearences.append(e)

    return new_appearences