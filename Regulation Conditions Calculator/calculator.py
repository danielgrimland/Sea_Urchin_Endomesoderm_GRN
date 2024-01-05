import copy as c
import functions as f
from state_mapping import State_Mapping


DOMAIN_VALUES = [-1, 0, 1]
DOMAIN_VALUES.append(min(DOMAIN_VALUES) - 1)
DOMAIN = f.prod(DOMAIN_VALUES)
CODOMAIN = [0, 1]


# Inputs: constants of the program.
# Outputs: a list containing all possible mappings from the Domain to the Codomain.
def generate_all_maps():
    current_maps = [State_Mapping(DOMAIN_VALUES, CODOMAIN)]
    new_maps = []    

    for i in range(len(DOMAIN)):
        for rc in current_maps:
            for val in CODOMAIN:
                new_rc = c.deepcopy(rc)
                new_rc.add_or_modify_pair(DOMAIN[i], val)
                new_maps.append(c.deepcopy(new_rc))

        current_maps = list(new_maps)
        new_maps = []
    
    print(len(current_maps))
    
    return current_maps


# Inputs: a list of all mappings from the Domain to the Codomain.
# Outputs: prints all regulations conditions of the list, and the number of them.
def print_regulation_conditions(all_maps):
    count = 0

    for grc in all_maps:
        if (grc.monotonic()):
            count += 1
            print(grc)
            print()

    print(f"In total there are {count} regulation conditions")


print_regulation_conditions(generate_all_maps())