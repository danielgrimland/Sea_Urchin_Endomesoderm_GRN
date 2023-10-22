"""
________________________________________________________________________________________________________________________________________
ABN EXPERIMENT MERGER

This program allows the generation of a cABNs from an ABN and multiple constraint datas in a given folder
________________________________________________________________________________________________________________________________________
INPUTS

TYPE: The specific file of the input and output data (if the ABN is of a Domain-Divided system, Full-Genome, etc.).
ABN NAME: The name of the ABN system inputed.
CONSTRAINTS NAME: The name of the constraint data inputed.
OUTPUT NAME: The name of the output file.
OUTPUT FOLDER: The folder in which the cABNs are to be stored.
CONSTRAINTS FOLDER: The folder in which the constraints are stored (for families of constraints).

STORAGE PATH: Where to store the results.
CONSTRAINTS PATH: Where to get the constraint data from. e.g. for: Domain-Divided_Constraints_[0, 2]_2,
the name is: Domain-Divided_Constraints_[0, 2],
and the experiment number is 2.

ABN PATH: Where to get the ABN from.

EXPERIMENTS IN USE: Each place is associated with an experiment (index 0: exp 1, index 1: exp 2, etc.).
A 1 in the experiments place in the list means to use the experiment in the cABN, and not otherwise.

RUN OVER INDEXES: All the file indexes which should be read
i.e. if you perturb components and you want to select only certain indexes, write it there.
________________________________________________________________________________________________________________________________________
"""


from pathlib import Path
import os
import shutil

TYPE = "Domain-Divided"
ABN_NAME = f"{TYPE}_ABN_optional"
CONSTRAINTS_NAME = f"{TYPE}_Constraints_All_KO"
OUTPUT_NAME = f"{TYPE}_cABN_[1-2-3] All_KO"
OUTPUT_FOLDER = f"[1-2-3] All_FKO"
CONSTRAINTS_FOLDER = f"All_KO"

STORAGE_PATH = Path(rf"C:\Users\Lithi\OneDrive\Documents\submission version 6\submission\artifact\Examples\Daniel Models\Sea Urchin Models\Endomesoderm_GRN\{TYPE}\{OUTPUT_FOLDER}")
ABN_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\ABN Storage\{TYPE}")
CONSTRAINTS_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Experimental Constraints Storage\{TYPE}\{CONSTRAINTS_FOLDER}")

EXPERIMENTS_IN_USE = [1, 0, 0, 0, 0, 0, 0, 0, 0]
RUN_OVER_INDEXES = ["1-1"]


# inputs: the data end symbol, and the string
# outputs: the variables of the string
def Slice_String(data_break, string):
    variable_list = []

    while True:
        ver_index =  string.find(data_break)

        if (ver_index == -1):
            variable_list.append(string)
            break

        variable_list.append(string[:ver_index])
        string = string[ver_index + 1:]

    return variable_list


# inputs: a short list description of the wanted indexes
# outputs: an explict list of wanted indexes
def Explict_Ranges():
    explict_indexes = []
    
    for r in RUN_OVER_INDEXES:
        full_list = Slice_String("-", r)

        for k in range(int(full_list[0]), int(full_list[1]) + 1):
            explict_indexes.append(k)

    return explict_indexes


# inputs: the name of a folder
# outputs: creates the folder
def Make_Folder():
    try:
        os.mkdir(STORAGE_PATH)

    except:
        for filename in os.listdir(STORAGE_PATH):
            file_path = os.path.join(STORAGE_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. This is due to: {e})")


# inputs: the list of experiments in use
# outputs: the experiment numbers in use
def Generate_Name():
    name_list = []

    for i in range(len(EXPERIMENTS_IN_USE)):
        if (EXPERIMENTS_IN_USE[i] == 1):
            name_list.append(i + 1)

    return name_list


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
def Get_Experiments(index):
    all_experiment_lines = []

    for i in range(len(EXPERIMENTS_IN_USE)):
        experiment_lines = []

        if (EXPERIMENTS_IN_USE[i] == 1):
            file_name = f"{CONSTRAINTS_NAME}_{i + 1}_{index}.txt"
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
def Create_cABN(experiment_lines, ABN_lines, index):
    file_name = f"{OUTPUT_NAME}_{Generate_Name()}_{index}.rein"
    file_path = STORAGE_PATH.joinpath(file_name)

    with open(file_path, 'w') as model:
        for line in ABN_lines:
            model.write(line + "\n")
        
        for i in range(2):
            model.write("\n")
        
        for line in experiment_lines:
            model.write(line + "\n")


# inputs: the lines of the ABN merged to
# outputs: merges all files wanted in the given folder with the ABN, and creates new cABNs
def Run(ABN_lines):
    for i in RUN_OVER_INDEXES:
        experiment_lines = Get_Experiments(i)

        Create_cABN(experiment_lines, ABN_lines, i)

    print("GENERATED RE:IN cABN(S)")
    exit()


Make_Folder()

RUN_OVER_INDEXES = Explict_Ranges()

ABN_lines = Get_ABN(f"{ABN_NAME}.txt")

Run(ABN_lines)