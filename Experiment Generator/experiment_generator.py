import pathlib as p
import functions as f
from auxilary_objects import Constraint, Perturbation, Range, SPT, Constraint_Appearences, Experiment_Expression
import os
import shutil
import itertools as itt


ABN_FILE = f"---"
ABN_FOLDER = p.Path(rf"---")

DATA_FILE = f"---"
OUTPUT_NAME = f"---"
OUTPUT_FOLDER_NAME = f"---"

OUTPUT_PATH = p.Path(rf"---")
DATA_PATH = p.Path(rf"---")

COMPONENTS = []


CONSTRAINT_EXPRESSIONS = {}
                               

PERTURBATIONS = []


# Inputs: the name of the data file, and the path to its folder.
# Outputs: a list of the lines of the files without the deafult \n at the start.
def get_lines():
    path = DATA_PATH.joinpath(f"{DATA_FILE}.txt")
    with open(path) as data:
        lines = data.readlines()

    for i in range(len(lines) - 1):
        lines[i] = [lines[i][:-1], i + 1]
    lines[-1] = [lines[-1], len(lines)] 

    return lines


# Inputs: a list of lines.
# Outputs: a dictionary mapping an experiment number with the lines corresponding to the experiment
def filter_lines(lines):
    experiments = {}
    experiment_numbers = []

    for line in lines:
        if (line[0][0] == "#"):

            line[0] = line[0][1:]
            end_of_number = line[0].find("|")

            if (end_of_number != -1):

                experiment_number = int(line[0][:end_of_number])

                if (experiment_number not in experiment_numbers):
                    experiments.update({experiment_number : []})
                    experiment_numbers.append(experiment_number)

                experiments[experiment_number].append((line[0][end_of_number + 1:], line[1]))
                
            else:
                f.error(f"No experiment number specified in line {line[1]}.")

    return experiments


# Inputs: a list of experiment lines.
# Outputs: a translation of the lines to a more suitable format.
def translate_experiments(experiments):
    new_experiments = {}
    
    for experiment_n in experiments:
        data_list = []

        for line in experiments[experiment_n]:
            segments = f.segmentize_string(line[0], "|")
            
            if (segments[0] not in COMPONENTS):
                f.error(f"Component mentioned in line {line[1]} is nonexistant in the ABN used.")

            ranges = f.segmentize_string(segments[1], "/")
            new_ranges = []

            for i in range(len(ranges)):
                new_r = f.segmentize_string(ranges[i], "-")
                new_ranges.append(Range(int(new_r[0]), int(new_r[1]), int(new_r[2]), line[1]))

            data_list.append((segments[0], new_ranges))

        new_experiments.update({experiment_n : list(data_list)})

    return new_experiments


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

            combinations = list(itt.combinations(PERTURBATIONS[i][1][0], PERTURBATIONS[i][1][1]))
            
            for combination in combinations:
                p = []

                for tuple in combination:
                    for e in tuple:
                        if (e not in COMPONENTS):
                            f.error(f"The component {e} specified in PERTURBATIONS is not part of the ABN used.")

                        p.append(SPT(e, PERTURBATIONS[i][1][2], PERTURBATIONS[i][1][3]))

                new_combinations.append(p)
            
            perturbations.append(list(new_combinations))
            
        elif (PERTURBATIONS[i][0] == "REG"):

            for p in PERTURBATIONS[i][1]:
                for component in p[0]:
                    perturbations.append([[SPT(component, p[1], p[2])]])

        else:
            f.error(f"No generation specification for block {i}.")

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
            if ((f.subset_spt_lists(list1, list2)) and (f.subset_spt_lists(list2, list1))):
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
            new_expressions[experiment_n].append(Constraint_Appearences(f"Restriction_{experiment_n}_{constraint_n}", f.generate_appearences(CONSTRAINT_EXPRESSIONS[experiment_n][constraint_n])))

    return new_expressions


# Inputs: a list of constraint appereances.
# Outputs: a list of constraint expressions for every experiment.
def generate_permutations(expressions):
    new_expressions = {}

    for experiment_n in expressions:
        list_family = []

        for appereances in expressions[experiment_n]:
            list_family.append(appereances.appearences)

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
        new_expressions.append(Experiment_Expression(experiment_n, list(CONSTRAINT_EXPRESSIONS[experiment_n]), expressions[experiment_n]))

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
                print(f"Failed to delete {file_path}. This is due to: {e})")


# Inputs: experimental constraints, experiment expressions, and perturbation constraints.
# Outputs: a cabn composed of them.
def create_cabns_perturbations(experiments, expressions, perturbations):
    make_folder()

    abn_path = (ABN_FOLDER.joinpath(f"{ABN_FILE}.txt"))

    count = 1

    for i in range(len(perturbations)):
        file_path = (OUTPUT_PATH.joinpath(OUTPUT_FOLDER_NAME)).joinpath(f"{OUTPUT_NAME}_{i}.txt")

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

            for expression in expressions:
                cabn.write(f"{expression}")


# Inputs: experimental constraints, and experiment expressions.
# Outputs: a cabn composed of them.
def create_cabns(experiments, expressions):
    make_folder()

    abn_path = (ABN_FOLDER.joinpath(f"{ABN_FILE}.txt"))

    file_path = (OUTPUT_PATH.joinpath(OUTPUT_FOLDER_NAME)).joinpath(f"{OUTPUT_NAME}.txt")

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

        for expression in expressions:
            cabn.write(f"{expression}")


experiments = generate_constraints(translate_experiments(filter_lines(get_lines())))

if (len(PERTURBATIONS) != 0):
    perturbations = generate_perturbations(translate_perturbations())

expressions = generate_permutations(generate_constraint_appearences())

if (len(PERTURBATIONS) != 0):
    create_cabns_perturbations(experiments, expressions, perturbations)
else:
    create_cabns(experiments, expressions)

print("cABN(s) Generated")