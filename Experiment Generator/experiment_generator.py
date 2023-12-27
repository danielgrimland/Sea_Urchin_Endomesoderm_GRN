import pathlib as p
import re
import functions as f
from auxilary_objects import Constraint, Perturbation, Range, SPT, Constraint_Appearences, Experiment_Expression
import os
import shutil
import itertools as itt
import copy as c


ABN_FILE = f"---"
ABN_FOLDER = p.Path(rf"---")

DATA_FILE = f"---"
DATA_PATH = p.Path(rf"---")

OUTPUT_NAME = f"---"
OUTPUT_FOLDER_NAME = f"---"
OUTPUT_PATH = p.Path(rf"---")


CONSTRAINT_EXPRESSIONS = {}


ORDER = {}


PERTURBATIONS = []
                 

# Inputs: an ABN.
# Outputs: the components of the abn.
def get_components():
    abn_path = (ABN_FOLDER.joinpath(f"{ABN_FILE}.rein"))
    components = []

    with open(abn_path) as abn:
        lines = abn.readlines()

    new_lines = []

    for i in range(len(lines)):
        new_line = (lines[i].replace(" ", "")).replace("\n", "")

        if (len(new_line) != 0):
            new_lines.append([new_line, i + 1])

    for line in new_lines:
        is_component = re.search("^[^\/](.*)\(([0-9]|1[0-7])..([0-9]|1[0-7])\);$", line[0])
        
        if (is_component):
            line[0] = line[0].replace(" ", "")
            with_specification = re.search("(\[\+-\])|(\[-\+\])|(\[-\])|(\[\+\])|(\[!\])", line[0])
            
            if (with_specification):
                last = line[0].rfind("[")
            
            else:
                last = line[0].rfind("(")
            
            components.append(line[0][:last])

    return components


# Inputs: the name of the data file, and the path to its folder.
# Outputs: a list of the lines of the files without the deafult \n at the start.
def get_lines():
    path = DATA_PATH.joinpath(f"{DATA_FILE}.txt")
    with open(path) as data:
        lines = data.readlines()

    new_lines = []

    for i in range(len(lines)):
        new_line = (lines[i].replace(" ", "")).replace("\n", "")

        if (len(new_line) != 0):
            new_lines.append([new_line, i + 1])

    return new_lines


# Inputs: a list of lines.
# Outputs: a dictionary mapping an experiment number with the lines corresponding to the experiment
def filter_lines(lines):
    experiments = {}
    experiment_numbers = []

    for line in lines:
        is_comment = re.search("^#.+$", line[0])

        if (not(is_comment)):
            is_experiment = re.search("^([1-9][0-9]*)\|([^|]+)\|([1-9][0-9]*-[1-9][0-9]*-[0-1]\/)*([1-9][0-9]*-[1-9][0-9]*-[0-1])$", line[0])

            if (is_experiment):
                end_of_number = line[0].find("|")
                experiment_number = int(line[0][:end_of_number])

                if (experiment_number not in experiment_numbers):
                    experiments.update({experiment_number : []})
                    experiment_numbers.append(experiment_number)

                experiments[experiment_number].append((line[0][end_of_number + 1:], line[1]))
            
            else:
                f.error(f"Line << {line[1]} >> is neither an experiment line or comment.")

    return experiments


# Inputs: a list of experiment lines.
# Outputs: a translation of the lines to a more suitable format.
def translate_experiments(experiments, components):
    new_experiments = {}
    constraints = {}
    
    for experiment_n in experiments:
        data_list = []
        constraints.update({experiment_n : []})

        for line in experiments[experiment_n]:
            segments = re.split("\|", line[0])
            
            if (segments[0] not in components):
                f.error(f"Component in line << {line[1]} >> is nonexistant in the ABN used.")

            ranges = re.split("\/", segments[1])
            new_ranges = []

            for i in range(len(ranges)):
                new_r = re.split("\-", ranges[i])

                if (int(new_r[0]) <= int(new_r[1])):
                    new_r = Range(int(new_r[0]), int(new_r[1]), int(new_r[2]), line[1])
                    constraints[experiment_n].extend(new_r.range)
                    constraints[experiment_n] = f.remove_copies(constraints[experiment_n])

                    for r in new_ranges:
                        if (not(Range.disjoint(r, new_r))):
                            if (r.val != new_r.val):
                                f.error(f"The ranges {r.start}-{r.end}-{r.val} and {new_r.start}-{new_r.end}-{new_r.val} specified in line {r.line_index} disagree on the value of {segments[0]} in some constraints.")

                    new_ranges.append(c.deepcopy(new_r))

                else:
                    f.error(f"A range in line << {line[1]} >> starts with {new_r[0]}, which is larger than the number it ends with ({new_r[1]}).")

            data_list.append((segments[0], new_ranges))

        new_experiments.update({experiment_n : list(data_list)})

    return new_experiments, constraints


# Inputs: experiment lines.
# Outputs: constraint objects for each experiment.
def generate_constraints(experiments):
    new_experiments = {}

    for experiment_n in experiments:
        constraints = {}
        constraint_numbers = []
        
        for data in experiments[experiment_n]:
            for range in data[1]:
                for i in range.range:
                    if (i not in constraint_numbers):
                        constraints.update({i : Constraint(f"Restriction_{experiment_n}_{i}")})
                        constraint_numbers.append(i)

                    constraints[i].dict.update({data[0] : range.val})

        new_experiments.update({experiment_n : dict(constraints)})
    
    return new_experiments


# Inputs: the perturbations list.
# Outputs: translates the perturbations to a more suitable format.
def translate_perturbations():
    perturbations = []

    for i in range(len(PERTURBATIONS)):
        if (PERTURBATIONS[i][0] == "COMB"):
            new_combinations = []

            combinations = list(itt.combinations(f.remove_copies(PERTURBATIONS[i][1][0]), PERTURBATIONS[i][1][1]))
            
            for combination in combinations:
                p = []

                for tuple in combination:
                    for e in tuple:
                        p.append(SPT(e, f.remove_copies(PERTURBATIONS[i][1][2]), PERTURBATIONS[i][1][3]))

                new_combinations.append(p)
            
            perturbations.append(list(new_combinations))
            
        else:

            for p in PERTURBATIONS[i][1]:
                for component in p[0]:
                    perturbations.append([[SPT(component, p[1], p[2])]])

    perturbations = f.general_prod(perturbations)

    new_perturbations = []

    for combination in perturbations:
        new_combination = []

        for e in combination:
            new_combination.extend(e)

        new_perturbations.append(new_combination)

    perturbations = list(new_perturbations)

    new_perturbations = []

    for list1 in perturbations:
        append = True
        
        for list2 in new_perturbations:
            if ((f.subset_lists(list1, list2)) and (f.subset_lists(list2, list1))):
                append = False

        if (append):
            new_perturbations.append(list1)

    return new_perturbations


# Inputs: a perturbation list.
# Outputs: generates perturbations for all experiments a file.
def generate_perturbations(perturbations):
    new_perturbations = []
    not_added = 0

    for i in range(len(perturbations)):
        index = i - not_added
        batch_perturbations = generate_batch(perturbations[i], index)

        if (len(batch_perturbations) != 0):
            new_perturbations.append(dict(batch_perturbations))
        else:
            not_added += 1

    return new_perturbations


# Inputs: a batch of perturbations for a single file.
# Outputs: translates the perturbations to a final format.
def generate_batch(batch, index):
    batch_perturbations = {}
    add = True

    for i in range(len(batch)):
        for experiment_n in batch[i].experiments:
            if (not(experiment_n in batch_perturbations)):
                batch_perturbations.update({experiment_n : Perturbation(f"Perturbation_{experiment_n}_{index + 1}")})

            if batch[i].component in batch_perturbations[experiment_n].dict:
                if (batch_perturbations[experiment_n].dict[batch[i].component] != batch[i].val):
                    add = False
                    print(f"Please notice that the PERTURBATIONS provided generated some perturbations where {batch[i].component} is both KOed and FEed. These scenrios were ignored.")
                
            batch_perturbations[experiment_n].dict.update({batch[i].component : batch[i].val})

    if (add):
        return batch_perturbations
    
    return {}


# Inputs: the Constraint Expressions.
# Outputs: a dictionary which maps experiments to lists of constraints with their corresponding timestamps where they can be satisfied.
def generate_constraint_appearences():
    new_expressions = {}

    for experiment_n in CONSTRAINT_EXPRESSIONS:
        if (not(experiment_n in new_expressions)):
            new_expressions.update({experiment_n : []})

        for constraint_n in CONSTRAINT_EXPRESSIONS[experiment_n]:
            appearences = []

            for ranges in CONSTRAINT_EXPRESSIONS[experiment_n][constraint_n]:
                appearences.append(f.generate_appearences(ranges))

            new_expressions[experiment_n].append(Constraint_Appearences(appearences, constraint_n))

    return new_expressions


# Inputs: a list of constraint appereances.
# Outputs: a list of constraint expressions for every experiment.
def generate_permutations(expressions):
    new_expressions = {}
    corresponding_constraints = {}

    for experiment_n in expressions:
        corresponding_constraints.update({experiment_n : []})
        corresponding_constraint_names = []
        list_family = []

        if (not(ORDER)):
            for appearences in expressions[experiment_n]:
                for _ in range(len(appearences.appearences)):
                    corresponding_constraint_names.append(str(appearences.constraint_n))
                list_family.extend(appearences.appearences)
        else:
            for satisfication in ORDER[experiment_n]:
                for appearences in expressions[experiment_n]:
                    if (appearences.constraint_n == satisfication[0]):
                        list_family.append(appearences.appearences[satisfication[1]])
                        corresponding_constraint_names.append(str(appearences.constraint_n))

        corresponding_constraints[experiment_n] = list(corresponding_constraint_names)

        permutations = f.general_prod(list_family)

        new_permutations = []

        for p in permutations:
            valid = True

            for i in range(0, len(p) - 1):
                if not(p[i] < p[i + 1]):
                    valid = False

            if (valid):
                new_permutations.append(p)

        new_expressions.update({experiment_n : list(new_permutations)})
    
    expressions = dict(new_expressions)

    new_expressions = []

    for experiment_n in expressions:
        new_expressions.append(Experiment_Expression(experiment_n, list(corresponding_constraints[experiment_n]), expressions[experiment_n]))

    return new_expressions


# Inputs: the name of the folder to generate, and the directory to put it in.
# Outputs: generates the file.
def make_folder():
    new_path = OUTPUT_PATH.joinpath(OUTPUT_FOLDER_NAME)

    try:
        os.mkdir(new_path)

    except:
        for filename in os.listdir(new_path):
            file_path = os.path.join(new_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path} due to: {e})")


# Inputs: experimental constraints, experiment expressions, and perturbation constraints.
# Outputs: a cabn composed of them.
def create_cabns_perturbations(experiments, expressions, perturbations):
    make_folder()

    abn_path = (ABN_FOLDER.joinpath(f"{ABN_FILE.rein"))

    count = 1

    for i in range(len(perturbations)):
        file_path = (OUTPUT_PATH.joinpath(OUTPUT_FOLDER_NAME)).joinpath(f"{OUTPUT_NAME}_{i}.rein")

        with open(file_path, "w") as cabn:
            with open(abn_path) as abn:
                lines = abn.readlines() 

            for abn_line in lines:
                cabn.write(abn_line)
            
            cabn.write("\n\n")
            
            for experiment_n in experiments:
                for constraint in experiments[experiment_n]:
                    cabn.write(f"{experiments[experiment_n][constraint]}")
                    cabn.write("\n\n")

            cabn.write("\n\n")

            for experiment_n in perturbations[i]:
                cabn.write(f"{perturbations[i][experiment_n]}")
                cabn.write("\n\n")
            
            cabn.write("\n\n")

            for experiment_n in perturbations[i]:
                cabn.write(f"#Experiment_{experiment_n}[0] |= Perturbation_{experiment_n}_{count};")
                cabn.write("\n\n")
                count += 1

            cabn.write("\n\n")

            if (bool(CONSTRAINT_EXPRESSIONS)):
                for expression in expressions:
                    cabn.write(f"{expression}")


# Inputs: experimental constraints, and experiment expressions.
# Outputs: a cabn composed of them.
def create_cabns(experiments, expressions):
    make_folder()

    abn_path = (ABN_FOLDER.joinpath(f"{ABN_FILE}.rein"))

    file_path = (OUTPUT_PATH.joinpath(OUTPUT_FOLDER_NAME)).joinpath(f"{OUTPUT_NAME}.rein")

    with open(file_path, "w") as cabn:
        with open(abn_path) as abn:
            lines = abn.readlines() 

        for abn_line in lines:
            cabn.write(abn_line)
        
        cabn.write("\n\n")
        
        for experiment_n in experiments:
            for constraint in experiments[experiment_n]:
                cabn.write(f"{experiments[experiment_n][constraint]}")
                cabn.write("\n\n")

        cabn.write("\n\n")

        if (bool(CONSTRAINT_EXPRESSIONS)):
            for expression in expressions:
                cabn.write(f"{expression}")


# Inputs: the index of a COMB block, a list of components, and a list of experiments.
# Outputs: whether the block is in correct format.
def check_comb_block(i, components, experiments):
    if (len(PERTURBATIONS[i][1]) != 4):
        f.error(f"The specifications of the COMB block which is element {i + 1} of PERTURBATIONS are too short or too long.")

    elif ((str(type(PERTURBATIONS[i][1][0])) != "<class 'list'>") or (str(type(PERTURBATIONS[i][1][1])) != "<class 'int'>") or (str(type(PERTURBATIONS[i][1][2])) != "<class 'list'>") or (str(type(PERTURBATIONS[i][1][3])) != "<class 'int'>")):
        f.error(f"An element of the specifications of element {i + 1} of PERTURBATIONS is not of the correct type (look up manual).")

    else:
        for j in range(len(PERTURBATIONS[i][1][0])):
            if (str(type(PERTURBATIONS[i][1][0][j])) != "<class 'tuple'>"):
                f.error(f"Element {j + 1} of the tuple list in the specifications of element {i + 1} of PERTURBATIONS is not a tuple.")
            
            else:
                for component in PERTURBATIONS[i][1][0][j]:
                    if (component not in components):
                        f.error(f"The component {component} in the tuple list of element {i + 1} of PERTURBATIONS doesn't exist in the ABN provided.")

        if (PERTURBATIONS[i][1][1] <= 0):
            f.error(f"There can't be {PERTURBATIONS[i][1][1]} components in a combinations as specified in element {i + 1} of PERTURBATIONS.")

        if (len(PERTURBATIONS[i][1][2]) == 0):
            f.error(f"The experiment list in the specification of COMB block {i + 1} is empty.")

        for e_number in PERTURBATIONS[i][1][2]:
            if (str(type(e_number)) == "<class 'int'>"):
                if (e_number <= 0):
                    f.error(f"An experiment number in the list in element {j + 1} of element {i + 1} of PERTURBATIONS is a non-positive integer.")
                
                elif (e_number not in experiments):
                    print(f"Please notice the experiment number {e_number} you provided in PERTURBATIONS was not defined in CONSTRAINT EXPRESSIONS, meaning you will get perturbations for an empty experiment.")
            
            else:
                f.error(f"An experiment number in the list in element {j + 1} of element {i + 1} of PERTURBATIONS is a non-positive integer.")

        if ((PERTURBATIONS[i][1][3] != 0) and (PERTURBATIONS[i][1][3] != 1)):
            f.error(f"The state for the components of element {j + 1} of element {i + 1} of PERTURBATIONS is not 0 or 1.")


# Inputs: the indecies of a REG subblock, a list of components, and a list of experiments.
# Outputs: whether the subblock is in correct format.
def check_reg_subblocks(i, j, components, experiments):
    if (len(PERTURBATIONS[i][1][j]) != 3):
        f.error(f"Element {j + 1} of element {i + 1} of PERTURBATIONS has not enough or too many elements.")

    elif ((str(type(PERTURBATIONS[i][1][j][0])) != "<class 'tuple'>") or (str(type(PERTURBATIONS[i][1][j][1])) != "<class 'list'>") or (str(type(PERTURBATIONS[i][1][j][2])) != "<class 'int'>")):
        f.error(f"An element of element {j + 1} of element {i + 1} of PERTURBATIONS is not of the correct type (look up manual).")

    else:
        if (len(PERTURBATIONS[i][1][j][0]) == 0):
            f.error(f"The component list in element {j + 1} of element {i + 1} of PERTURBATIONS is empty.")

        for component in PERTURBATIONS[i][1][j][0]:
            if (str(type(component)) != "<class 'str'>"):
                f.error(f"Component {component} of the component list in element {j + 1} of element {i + 1} of PERTURBATIONS is not a string.")
            
            elif (component not in components):
                f.error(f"The component {component} in the components of element number {j + 1} in element number {i + 1} of PERTURBATIONS doesn't exist in the ABN provided.")

        if (len(PERTURBATIONS[i][1][j][1]) == 0):
            f.error(f"The experiment list in element {j + 1} of element {i + 1} of PERTURBATIONS is empty.")

        for e_number in PERTURBATIONS[i][1][j][1]:
            if (str(type(e_number)) == "<class 'int'>"):
                if (e_number <= 0):
                    f.error(f"An experiment number in the list in element {j + 1} of element {i + 1} of PERTURBATIONS is a non-positive integer.")
                
                elif (e_number not in experiments):
                    print(f"Please notice the experiment number {e_number} you provided in PERTURBATIONS was not defined in CONSTRAINT EXPRESSIONS, meaning you will get perturbations for an empty experiment.")
            
            else:
                f.error(f"An experiment number in the list in element {j + 1} of element {i + 1} of PERTURBATIONS is a non-positive integer.")

        if ((PERTURBATIONS[i][1][j][2] != 0) and (PERTURBATIONS[i][1][j][2] != 1)):
            f.error(f"The state for the components of element {j + 1} of element {i + 1} of PERTURBATIONS is not 0 or 1.")


# Inputs: a list of components, and a list of experiments
# Outputs: whether the PERTURBATIONS list provided is in the correct format as specified in the manual.
def format_perturbations(components, experiments):
    for i in range(len(PERTURBATIONS)):
        if (str(type(PERTURBATIONS[i])) != "<class 'list'>"):
            f.error(f"Element {i + 1} of PERTURBATIONS is not a list.")

        elif (len(PERTURBATIONS[i]) <= 1):
            f.error(f"Element {i + 1} of PERTURBATIONS is too short to be a COMB block or REG block.")

        else:
            if (PERTURBATIONS[i][0] == "REG"):
                if (len(PERTURBATIONS[i]) != 2):
                    f.error(f"Element number {i + 1} in PERTURBATIONS is a REG block with more or less than 2 elements.")
                
                elif (str(type(PERTURBATIONS[i][1])) != "<class 'list'>"):
                    f.error(f"Second element in element number {i + 1} in PERTURBATIONS is not a list.")

                for j in range(1, len(PERTURBATIONS[i][1])):
                    check_reg_subblocks(i, j, components, experiments)

            elif (PERTURBATIONS[i][0] == "COMB"):
                if (len(PERTURBATIONS[i]) != 2):
                    f.error(f"Element number {i + 1} in PERTURBATIONS is a COMB block with more or less than 2 elements.")
                                
                elif (str(type(PERTURBATIONS[i][1])) != "<class 'list'>"):
                    f.error(f"Second element in element number {i + 1} in PERTURBATIONS is not a list.")

                else:
                    check_comb_block(i, components, experiments)

            else:
                f.error(f"Element number {i + 1} in PERTURBATIONS is neither a REG block nor a COMB block.")


# Inputs: a list of constraints in the untranslated data.
# Outputs: whether the CONSTRAINT EXPRESSIONS are in correct format, and a list of experiments and order elements defined.
def format_constraint_expressions(constraints):
    experiments = []

    order_elements = {}

    for e_number in CONSTRAINT_EXPRESSIONS:
        experiments.append(e_number)
        order_elements.update({e_number : []})

        if (str(type(e_number)) == "<class 'int'>"):
            if (e_number <= 0):
                f.error(f"The CONSTRAINT EXPRESSIONS provided assign a non-positive integer an expression, when all experiment numbers should be natural numbers.")
            
            else:
                if (str(type(CONSTRAINT_EXPRESSIONS[e_number])) != "<class 'dict'>"):
                    f.error(f"Experiment {e_number} doesn't map to a dictionary.")
                
                elif (len(CONSTRAINT_EXPRESSIONS[e_number]) == 0):
                    f.error(f"Experiment {e_number} maps to an empty dictionary.")
                
                else:
                    for c_number in CONSTRAINT_EXPRESSIONS[e_number]:
                        if (c_number not in constraints[e_number]):
                            f.error(f"The constraint number {c_number} (which may not be an integer) doesn't exist in the untranslated data provided.")

                        else:
                            if (str(type(CONSTRAINT_EXPRESSIONS[e_number][c_number])) != "<class 'list'>"):
                                f.error(f"The constraint number {c_number} in experiment {e_number} doesn't map to a list.")
                            
                            elif (len(CONSTRAINT_EXPRESSIONS[e_number][c_number]) == 0):
                                f.error(f"The constraint number {c_number} in experiment {e_number} maps to an empty list.")
                            
                            else:
                                for i in range(len(CONSTRAINT_EXPRESSIONS[e_number][c_number])):
                                    order_elements[e_number].append((c_number, i))

                                    if (str(type(CONSTRAINT_EXPRESSIONS[e_number][c_number][i])) != "<class 'tuple'>"):
                                        f.error(f"Tuple {i + 1} in the list of constraint number {c_number} in experiment {e_number} is not a tuple.")
                                    
                                    elif (len(CONSTRAINT_EXPRESSIONS[e_number][c_number][i]) == 0):
                                        f.error(f"Tuple {i + 1} in the list of constraint number {c_number} in experiment {e_number} is empty.") 
                                    
                                    else:
                                        for j in range(len(CONSTRAINT_EXPRESSIONS[e_number][c_number][i])):
                                            if (str(type(CONSTRAINT_EXPRESSIONS[e_number][c_number][i][j])) != "<class 'str'>"):
                                                f.error(f"Range {j + 1} of Tuple {i + 1} in the list of constraint number {c_number} in experiment {e_number} is not a string")

                                            elif (not(re.search("^([0-9]*)\-([0-9]*)$", CONSTRAINT_EXPRESSIONS[e_number][c_number][i][j]))):
                                                f.error(f"Range {j + 1} of Tuple {i + 1} in the list of constraint number {c_number} in experiment {e_number} is not a proper range (see manual).")
                                                                                        
                                            else:
                                                start_and_end = re.split("\-", CONSTRAINT_EXPRESSIONS[e_number][c_number][i][j])
                                                
                                                if (int(start_and_end[0]) > int(start_and_end[1])):
                                                    f.error(f"Range {j + 1} of Tuple {i + 1} in the list of constraint number {c_number} in experiment {e_number} has a first element ({start_and_end[0]}) larger than the second ({start_and_end[1]})")

        else:
            f.error(f"The CONSTRAINT EXPRESSIONS provided assign a non-positive integer an expression, when all experiment numbers should be natural numbers.")

    return experiments, order_elements


# Inputs: a list of experiment numbers and order elements.
# Outputs: whether the ORDER was given in correct format.
def format_order(experiments, order_elements):
    for e_number in ORDER:
        if (e_number not in experiments):
            f.error(f"The ORDER provided assigns a variable (possibly not integer) an order, despite not being defined in the CONSTRAINT EXPRESSIONS as experiment.")
            
        else:
            if (str(type(ORDER[e_number])) != "<class 'list'>"):
                f.error(f"Experiment number {e_number} doesn't map to a list.")

            elif (len(ORDER[e_number]) == 0):
                f.error(f"Experiment number {e_number} maps to an empty list.")

            else:
                if (not(f.subset_lists(ORDER[e_number], order_elements[e_number])) and (f.subset_lists(order_elements[e_number], ORDER[e_number]))):
                    f.error(f"The order given for experiment {e_number} is not a permutation of the constraints and their appearences.")


components = get_components()

experiments, constraints = translate_experiments(filter_lines(get_lines()), components)

experiments = generate_constraints(experiments)

experiment_numbers = []

if (len(CONSTRAINT_EXPRESSIONS) != 0):
    experiment_numbers, order_elements = format_constraint_expressions(constraints)

    format_order(experiment_numbers, order_elements)

if (len(PERTURBATIONS) != 0):
    format_perturbations(components, experiment_numbers)

    perturbations = generate_perturbations(translate_perturbations())

expressions = generate_permutations(generate_constraint_appearences())

if (len(PERTURBATIONS) != 0):
    create_cabns_perturbations(experiments, expressions, perturbations)
else:
    create_cabns(experiments, expressions)

print("cABN(s) Generated")
