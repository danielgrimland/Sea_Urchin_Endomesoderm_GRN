# Inputs: an error message.
# Outputs: displays the error message and closes the program.
def error(error_name):
    print(error_name)
    input()
    exit()


# Inputs: a list.
# Outputs: a new list without any duplicates.
def remove_duplicates(list):
    new_list = []

    for e in list:
        if (e not in new_list):
            new_list.append(e)
        
    return new_list


# Inputs: a list without duplicates.
# Outputs: the cartesian product of the list.
def prod(list):
    prod_list = []

    for e1 in list:
        for e2 in list:
            prod_list.append((e1, e2))

    return prod_list


# Inputs: a list.
# Outputs: whether all elements of it are numeric.
def list_numeric(list):
    for e in list:
        if (not(type(e) is float) and not(type(e) is int)):
            return False
        
    return True