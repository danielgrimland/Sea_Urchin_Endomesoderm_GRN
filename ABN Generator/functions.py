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


# Inputs: a list.
# Outputs: the elements of the list.
def print_list(list):
    for e in list:
        print(e)