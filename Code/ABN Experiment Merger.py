"""
________________________________________________________________________________________________________________________________________
ABN EXPERIMENT MERGER

This program allows the generation of a cABN from an ABN and constraint data
________________________________________________________________________________________________________________________________________
INPUTS

TYPE: The specific file of the input and output data (if the ABN is of a Domain-Divided system, Full-Genome, etc.).
ABN NAME = The name of the ABN system inputed.
CONSTRAINTS NAME = The name of the constraint data inputed.
OUTPUT NAME = The name of the output file.

STORAGE PATH: Where to store the results.
CONSTRAINTS PATH: Where to get the constraint data from.  
ABN PATH: Where to get the ABN from.

EXPERIMENT_TAKING_LIST = Each place is associated with an experiment (index 0: exp 1, index 1: exp 2, etc.).
A 1 in the experiments place in the list means to use the experiment in the cABN, and not otherwise.

________________________________________________________________________________________________________________________________________
"""


from pathlib import Path


TYPE = "Domain-Divided"
ABN_NAME = "Domain-Divided_ABN_optional"
CONSTRAINTS_NAME = "Domain-Divided_Constraints"
OUTPUT_NAME = "Domain-Divided_cABN_[1-2,1-3,1-4...]"

STORAGE_PATH = Path(rf"C:\Users\Lithi\OneDrive\Documents\submission version 6\submission\artifact\Examples\Daniel Models\Sea Urchin Models\Endomesoderm_GRN\{TYPE}")
ABN_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\ABN Storage\{TYPE}")
CONSTRAINTS_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Experimental Constraints Storage\{TYPE}")

EXPERIMENT_TAKING_LIST = [1, 1, 1, 1, 1, 1, 1, 1, 1]


# inputs: a list
# outputs: the elements of the list
def Print_List(list_printed):
    for e in list_printed:
        print(e)


# inputs: the file name of an ABN
# outputs: the lines of the ABN
def Get_ABN(file_name):
    new_path = ABN_PATH.joinpath(file_name)
    with open(new_path) as model:
        ABN_lines = model.readlines()

    for i in range(len(ABN_lines) - 1):
        ABN_lines[i] = ABN_lines[i][:-1]
    ABN_lines[-1] = ABN_lines[-1] 

    return ABN_lines


# inputs: the list of experiments which are being taken (format: [1,1,0,0,1,...]), and the header (name) of the experiments
# outputs: the lines of the chosen experiments
def Get_Experiments():
    all_experiment_lines = []

    for i in range(len(EXPERIMENT_TAKING_LIST)):
        experiment_lines = []

        if (EXPERIMENT_TAKING_LIST[i] == 1):
            file_name = f"{CONSTRAINTS_NAME}_[0, {i + 1}]_{i + 1}.txt"
            file_path = CONSTRAINTS_PATH.joinpath(file_name)

            with open(file_path) as model:
                experiment_lines = model.readlines()

            for j in range(len(experiment_lines) - 1):
                experiment_lines[j] = experiment_lines[j][:-1]
            experiment_lines[-1] = experiment_lines[-1]
        
        all_experiment_lines.extend(experiment_lines)

    return all_experiment_lines


# inputs: the lines of the experiments, the lines of the ABN, and the list of experiments which are being taken
# outputs: creates files merging the chosen experiments and the ABN
def Create_cABN(experiment_lines, ABN_lines):
    file_name = f"{OUTPUT_NAME}.rein"
    file_path = STORAGE_PATH.joinpath(file_name)

    with open(file_path, 'w') as model:
        for line in ABN_lines:
            model.write(line + "\n")
        
        for i in range(2):
            model.write("\n")
        
        for line in experiment_lines:
            model.write(line + "\n")


ABN_lines = Get_ABN(f"{ABN_NAME}.txt")

experiment_lines = Get_Experiments()

Create_cABN(experiment_lines, ABN_lines)

print("GENERATED RE:IN cABN(S)")