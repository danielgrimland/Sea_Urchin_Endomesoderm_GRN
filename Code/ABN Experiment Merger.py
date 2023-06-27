from pathlib import Path

TYPE = "Domain-Divided"
ABN_NAME = "Domain-Divided_ABN_optional"
CONSTRAINTS_NAME = "Domain-Divided_Constraints_1_[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]_fz-3_st-10"
OUTPUT_NAME = "Domain-Divided_cABN_[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"

STORAGE_PATH = Path(rf"C:\Users\Lithi\OneDrive\Documents\submission version 6\submission\artifact\Examples\Daniel Models\Sea Urchin Models\Endomesoderm_GRN\Biotapestry Models\{TYPE}")
ABN_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Model Translator\ABN Storage\{TYPE}")
CONSTRAINTS_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Model Translator\Experimental Constraints Storage\{TYPE}")

EXPERIMENT_TAKING_LIST = [1, 0, 0, 0]


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
            file_name = f"{CONSTRAINTS_NAME}.txt"
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

print("DONE")