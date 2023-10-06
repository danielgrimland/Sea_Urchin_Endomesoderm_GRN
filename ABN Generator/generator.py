import functions as f
from interactions_and_components import Interaction, Component
from pathlib import Path
import copy as c


UNTRANSLATED_INPUT = f"Domain-Divided_Input_ABN_all_optional"
OUTPUT_NAME =  f"Domain-Divided_ABN_test_new_gen"

OUTPUT_FOLDER = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\ABN Storage\Domain-Divided")
DATA_FOLDER = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Untranslated Input Data\Domain-Divided")


# Inputs: a .txt file name.
# Outputs: a list containing each line of the file. the lines have the default /n deleted.
def get_lines():
    data_path = DATA_FOLDER.joinpath(UNTRANSLATED_INPUT + ".txt")

    with open(data_path) as data:
        lines = data.readlines()

    for i in range(len(lines) - 1):
        lines[i] = [lines[i][:-1], i + 1]
    lines[-1] = [lines[-1], len(lines)] 

    return f.remove_duplicates(lines)


# Inputs: a list of lines.
# Outputs: filters the lines to a component line list and an interaction line list.
def filter_lines(lines):
    components = []
    interactions = []

    for line in lines:
        if (line[0][0] == "*"):
            components.append([line[0][1:], line[1]])
        if (line[0][0] == "@"):
            interactions.append([line[0][1:], line[1]])

    if ((len(interactions) == 0) or (len(components) == 0)):
        f.error("No Interactions or Components exist.")
    
    return components, interactions


# Inputs: a list of interaction strings, and a list of component names used.
# Outputs: a list of interaction objects made according to strings.
def translate_interactions(interactions, component_names):
    new_interactions = []

    for i in range(len(interactions)):
        segments = f.segmentize_string(interactions[i][0], "|")

        if (len(segments) != 5):
            f.error(f"Not enough information about the interaction in line {interactions[i][1]}.")

        if (segments[0] not in component_names) or (segments[1] not in component_names):
            f.error(f"Components in line {interactions[i][1]} were not defined in the given data.")
    
        new_interactions.append(Interaction(segments[0], segments[1], segments[2], segments[3], int(segments[4]), interactions[i][1]))

    return new_interactions


# Inputs: a list of component strings.
# Outputs: a list of component objects made according to strings, and a list of component names.
def translate_components(components):
    new_components = []
    component_names = []

    for i in range(len(components)):
        segments = f.segmentize_string(components[i][0], "|")

        if (len(segments) != 3):
            f.error(f"Not enough information about the interaction in line {components[i][1]}.")
    
        new_components.append(Component(segments[0], int(segments[1]), int(segments[2]), components[i][1]))
        component_names.append(segments[0])

    return new_components, component_names


# Inputs: a list of component and interaction objects.
# Outputs: updated lists according to time delays specified.
def add_time_delays(components, interactions):
    count = 0
    new_interactions = list(interactions)
    new_components = list(components)

    for interaction in interactions:
        if (interaction.delay != 1):
            for _ in range(interaction.delay - 1):
                new_components.append(Component(count, 1, 17, -1))
                count += 1

            new_interactions.append(Interaction(interaction.initiator, str(count - interaction.delay + 1), "pos", "def", 1, -1))
            for i in range(interaction.delay - 2):
                new_interactions.append(Interaction(str(count - interaction.delay + 1 + i), str(count - interaction.delay + 2 + i), "pos", "def", 1, -1))  
            new_interactions.append(Interaction(str(count - 1), interaction.target, interaction.is_pos, interaction.is_def, 1, -1))
            
            new_interactions.remove(interaction)

    return new_components, new_interactions


# Inputs: a list of component and interaction objects
# Outputs: a RE:IN ABN.
def generate_abn(components, interactions):
    with open(OUTPUT_FOLDER.joinpath(OUTPUT_NAME), 'w') as abn:
        for i in range(len(components)):
            abn.write(f"{components[i]}\n")
            abn.write("\n")

        abn.write("\n\n")

        for i in range(len(interactions) - 1):
            abn.write(f"{interactions[i]}\n")
            abn.write("\n")

        abn.write(f"{interactions[-1]}")


lines = get_lines()

components, interactions = filter_lines(lines)

components, component_names = translate_components(components)
interactions = translate_interactions(interactions, component_names)

components, interactions = add_time_delays(components, interactions)

generate_abn(components, interactions)

print("Generated ABN")