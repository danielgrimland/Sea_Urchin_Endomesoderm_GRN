import functions as f
import re
from auxilary_objects import Interaction, Component
from pathlib import Path


UNTRANSLATED_INPUT = f"---"
DATA_FOLDER = Path(rf"---")


OUTPUT_NAME =  f"---"
OUTPUT_FOLDER = Path(rf"---")


# Inputs: a .txt file name.
# Outputs: a list containing each line of the file. the lines have the default /n deleted.
def get_lines():
    data_path = DATA_FOLDER.joinpath(UNTRANSLATED_INPUT + ".txt")

    try:
        with open(data_path) as data:
            lines = data.readlines()
    except IOError:
        f.error("Data path or untranslated input name given don't exist")

    new_lines = []

    for i in range(len(lines)):
        new_line = (lines[i].replace(" ", "")).replace("\n", "")

        if (len(new_line) != 0):
            new_lines.append([new_line, i + 1])

    return f.remove_duplicates(new_lines)


# Inputs: a list of lines.
# Outputs: filters the lines to a component line list and an interaction line list.
def filter_lines(lines):
    components = []
    interactions = []

    for line in lines:
        is_comment = re.search("^#.+$", line[0])

        if (not(is_comment)):
            is_component = re.search("^([^#])([^|]*)\|([0-9]|1[0-7])\|([0-9]|1[0-7])$", line[0])
            is_interaction = re.search("^([^#])([^|]*)\|([^|]+)\|(pos|neg)\|(def|op)\|([1-9][0-9]*-[1-9][0-9]*\/)*([1-9][0-9]*-[1-9][0-9]*)$", line[0])

            if (is_component):
                components.append([line[0], line[1]])
            elif (is_interaction):
                interactions.append([line[0], line[1]])
            else:
                f.error(f"Line << {line[1]} >> is not an interaction, component, or comment.")

    if ((len(interactions) == 0) or (len(components) == 0)):
        f.error("No Interactions or Components exist.")
    
    return components, interactions


# Inputs: a list of interaction strings, and a list of component names used.
# Outputs: a list of interaction objects made according to strings.
def translate_interactions(interactions, component_names):
    new_interactions = []

    for i in range(len(interactions)):
        segments = re.split("\|", interactions[i][0])
        delays = re.split("\/", segments[4])
        new_delays = []

        for i in range(len(delays)):
            edges = re.split("\-", delays[i])
            if (int(edges[0]) <= int(edges[1])):
                new_delays.extend(range(int(edges[0]), int(edges[1]) + 1))
            else:
                f.error(f"Delay range number {i + 1} in the interaction in line << {interactions[i][1]} >> starts with {edges[0]}, which is larger than the number it ends with ({edges[1]}).")

        if (segments[0] not in component_names):
            if (segments[1] not in component_names):
                f.error(f"Interaction in line << {interactions[i][1]} >> uses both an intiator (first component) and target (second component) which are not defined.")
            else:
                f.error(f"Interaction in line << {interactions[i][1]} >> uses an intiator (first component) which is not defined.")
        else:
            if (segments[1] not in component_names):
                f.error(f"Interaction in line << {interactions[i][1]} >> uses a target (second component) which is not defined.")
            else:
                new_interactions.append(Interaction(segments[0], segments[1], segments[2], segments[3], f.remove_duplicates(new_delays)))

    return new_interactions


# Inputs: a list of component strings.
# Outputs: a list of component objects made according to strings, and a list of component names.
def translate_components(components):
    new_components = []
    component_names = []

    for i in range(len(components)):
        segments = re.split("\|", components[i][0])

        if (int(segments[1]) <= int(segments[2])):
            new_components.append(Component(segments[0], int(segments[1]), int(segments[2])))
            component_names.append(segments[0])
        else:
            f.error(f"Regulation condition range in the component in line << {components[i][1]} >> starts with {segments[0]}, which is larger than the number it ends with ({segments[1]}).")

    return new_components, component_names


# Inputs: a list of component and interaction objects.
# Outputs: updated lists according to time delays specified.
def add_time_delays(components, interactions):
    new_interactions = list(interactions)
    new_components = list(components)

    for interaction in interactions:
        if ((interaction.delays[0] != 1) or (len(interaction.delays) != 1)):
            max_delay = max(interaction.delays)
            min_delay = min(interaction.delays)

            for i in range(2, max_delay + 1):
                new_components.append(Component(f"{interaction.initiator}_{interaction.target}_{i}", 1, 17))
            
            new_interactions.append(Interaction(interaction.initiator, f"{interaction.initiator}_{interaction.target}_2", "pos", "def", 1))
            
            for i in range(2, max_delay):
                new_interactions.append(Interaction(f"{interaction.initiator}_{interaction.target}_{i}", f"{interaction.initiator}_{interaction.target}_{i + 1}", "pos", "def", 1))
                
                if (i in interaction.delays):
                    new_interactions.append(Interaction(f"{interaction.initiator}_{interaction.target}_{i}", interaction.target, interaction.is_pos, interaction.is_def, 1))

            new_interactions.append(Interaction(f"{interaction.initiator}_{interaction.target}_{max_delay}", interaction.target, interaction.is_pos, interaction.is_def, 1))

            if (1 not in interaction.delays):
                new_interactions.remove(interaction)

    return new_components, new_interactions


# Inputs: a list of component and interaction objects
# Outputs: a RE:IN ABN.
def generate_abn(components, interactions):
    try:
        with open(OUTPUT_FOLDER.joinpath(OUTPUT_NAME + ".txt"), 'w') as abn:
            for i in range(len(components)):
                abn.write(f"{components[i]}\n")
                abn.write("\n")

            abn.write("\n\n\n")

            for i in range(len(interactions) - 1):
                abn.write(f"{interactions[i]}\n")
                abn.write("\n")

            abn.write(f"{interactions[-1]}")
    except IOError:
        f.error("Output path given doesn't exist")


lines = get_lines()

components, interactions = filter_lines(lines)

components, component_names = translate_components(components)

interactions = translate_interactions(interactions, component_names)

components, interactions = add_time_delays(components, interactions)

generate_abn(components, interactions)

print("Generated ABN")