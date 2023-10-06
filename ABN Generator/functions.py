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


# Inputs: a string and a charcter seperating parts of it.
# Outputs: a list of segments of the original string.
def segmentize_string(string, seperator):
    segments = []

    sep_index = string.find(seperator)

    while (sep_index != -1):

        segments.append(string[:sep_index])
        string = string[sep_index + 1:]
        sep_index = string.find(seperator)

    segments.append(string)

    return segments