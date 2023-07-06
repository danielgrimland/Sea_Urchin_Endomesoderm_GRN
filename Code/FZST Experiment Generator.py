"""
________________________________________________________________________________________________________________________________________
FZST EXPERIMENT GENERATOR

This program allows the generation of RE:IN experimental constraints by locating untranslated input data
from a file, and translating it to constraints for several experiments.

The general experiment generator also allows to generate constraints such that
solutions would be generated in multiple scenarios of the mode.
Furthermore, the general experiment generator can delete parts of constraints to ease them, and write down the deleted information.
________________________________________________________________________________________________________________________________________
INPUTS

TAKE LIST: Explained below.

INPUT NAME: The name of the untranslated data file.
OUTPUT NAME: The main name of the output files (without specific details on the contents).

STORAGE PATH: Where to store the results.
DATA PATH: Where to get the data from.

NUM OF EXPERIMENTS: The number of experiments in the TAKE LIST.
KEEP FRAC: The fraction of elements to keep from constraints that are needed to be shaved.
OSTRING LENGTH: If the constraint data is written in OStrings, how long each is.
TIMESTAMP LENGTH: How many timestamps to use in each experiment.

FUZZY NUMBER: How much to allow to strech and allow constraints to occur on diffent times.
A fuzzy number of 3 for example would mean that a constraint in timestamp 4 can be met at timestamps 1-7.

STRANDING NUMBER: How much timestamps are in one hour.

COMPONENT LIST: The list of all legal components in an ABN.
________________________________________________________________________________________________________________________________________
"""


from pathlib import Path
import random as r


TYPE = "Full-Genome"
INPUT_NAME = f"{TYPE}_Input_Constraints"
OUTPUT_NAME = f"{TYPE}_Constraints"

STORAGE_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Experimental Constraints Storage\{TYPE}")
DATA_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Untranslated Input Data\{TYPE}")

NUM_OF_EXPERIMENTS = 9
OSTRING_LENGTH = 10 

# each element of the take list is an experiment list, where each element of the list is a constraint in some hour of the model
# if the first element of the constraint list is 1, use the constraint
# if the second element of the constraint is 1, fuzzify the constraint by the fuzzy number
# if the third element of the cosntraint is 1, strand the constraint by the stranding number
# if the fourth element of the constraint is 1, delete parts of the constraint by the keep fraction

TAKE_LIST = [[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],

             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],

             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],

             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],

             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],

             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
             
             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],

             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],

             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
            
             [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], 
             [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]]

FUZZY_NUMBER = 5
KEEP_FRAC = 1
STRANDING_NUMBER = 10
TIMESTAMP_LENGTH = 30 + (9 * STRANDING_NUMBER)

KIND = "OString"
COMPONENT_LIST = ['nodal_ecto', 'smad_not_gene_protien', 'smad', 'not_gene', 'unkn_runx', 'unkn_gatac', 'gatac', 'unkn_scl', 'scl', 'runx', 'ese', 'prox', 'r11pmdelta', 'r11pmdelta_nrl_protien', 'nrl', 'unkn_nrl', 'blimp1', 'blimp1_activate', 'hesc', 'ets1', 'unkn_ets1', 'otx', 'gcm', 'six12', 'gatae', 'erg', 'hex', 'tbr', 'not', 'gcm', 'six12', 'gatae', 'unkn_runx', 'runx', 'ese', 'prox', 'alx1', 'gatac', 'z166', 'otx', 'blimp1', 'blimp1_activate', 'hesc', 'ets1', 'nrl', 'r11pmdelta_nrl_protien', 'r11pmdelta', 'fog', 'gatae_fog_protien', 'erg', 'hex', 'capk', 'decorin', 'capk', 'decorin', 'pks', 'sutx', 'dpt', 'fvmo123', 'notch', 'suhn', 'notch_suhn_protien', 'suh', 'suh_notch_suhn_protien', 'foxy', 'unkn_soxe', 'soxe', 'smo', 'ptc', 'smo_ptc_hh_protien', 'foxf', 'gsk3', 'wnt8', 'frizzled', 'eve', 'hox1113b', 'otx', 'hnf1', 'signalv2', 'vegf3', 'gsk3_x_protien', 'gsk3_x_nbtcf_protien', 'bra', 'nbtcf_protien', 'eve', 'unc41', 'vegf3', 'unkn_soxb1', 'soxb1', 'wnt16', 'nbtcf_protien', 'eve', 'soxc', 'otx', 'blimp1', 'hox1113b', 'gatae', 'foxa', 'bra', 'gcm', 'krl', 'myc', 'brn124', 'tgif', 'hh', 'dac', 'endo16', 'wnt16_hox1113b_protien', 'signalv2_protien', 'g_cadherin', 'otx', 'cb', 'wnt6', 'soxb1', 'nucl_protien', 'ecns_protien', 'nbtcf_protien', 'gsk3', 'x_protien', 'blimp1', 'wnt8', 'ubiq_soxc', 'soxc', 'ubiq_es', 'es', 'pmar1', 'ubiq_hesc', 'hesc', 'gcm', 'activin_b', 'rhoa', 'rhoa_soxb1_protien', 'r11pmdelta_nrl_protien', 'ubiq_hnf6', 'hnf6', 'alx1', 'ubiq_ets1', 'ets1', 'tbr', 'nrl', 'hex', 'erg', 'tgif', 'ubiq_tel', 'tel', 'foxn23', 'r11pmdelta', 'r11pmdelta', 'dri', 'foxb', 'foxo', 'vegfr', 'l1', 'l1_vegfr_vegf3_protien', 'sm27', 'sm50', 'msp130', 'mspl', 'sm30', 'ficolin', 'cyp', 'ubiq_gcadherin', 'gcadherin']


# inputs: a take list
# outputs: adds indexes to each timestamp of the list
def Add_Indexes_To_Take_List():
    for experiment in TAKE_LIST:
        for i in range(len(experiment)):
            experiment[i].append(i)

            
# inputs: a .txt file name
# outputs: a list containing each line of the file. the lines have the default /n deleted
def Get_Lines(data_file):
    new_path = DATA_PATH.joinpath(data_file)
    with open(new_path) as exp:
        line_list = exp.readlines()

    for i in range(len(line_list) - 1):
        line_list[i] = [line_list[i][:-1], i + 1]
    line_list[len(line_list) - 1] = [line_list[len(line_list) - 1], len(line_list)] 

    return line_list


# inputs: a list
# outputs: the elements of the list
def Print_List(list_printed):
    for e in list_printed:
        print(e)


# inputs: a line list, the number of experiments
# outputs: filters the lines into a giant list of all experiments
def Filter_Lines(line_list):
    component_data_list = []
    experiment_list = []

    for i in range(NUM_OF_EXPERIMENTS):
        experiment_list.append([])

    for line in line_list:
        if (line[0][0] == "#"):
            component_data_list.append([line[0][1:], line[1]])

    for line in component_data_list:
        for i in range(NUM_OF_EXPERIMENTS):
            if (str(i + 1) == line[0][0]):
                discard_len = len(str(i + 1)) + 1
                experiment_list[i].append([line[0][discard_len:], line[1]])

    for i in range(NUM_OF_EXPERIMENTS):
        if (len(experiment_list[i]) == 0):
            Error(f"Experiment {i + 1} has no constraints")

    return experiment_list


# inputs: ES's seperated into experiments, and the number of timestamps
# outputs: a list of the timestamps of the experiments
def Create_Timestamp_List(experiment_list, TIMESTAMP_LENGTH):
    timestamp_list = []

    for i in range(len(experiment_list)):
        timestamp_list.append([])

    for i in range(len(experiment_list)):    
        for _ in range(TIMESTAMP_LENGTH):
            timestamp_list[i].append([])

    return timestamp_list


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


# inputs: the timestamp list, and the experiment list
# outputs: the timestamp list with restrictions
def Add_Constraints_To_Timestamps(timestamp_list, experiment_list, COMPONENT_LIST, KIND):
    sliced_constraint_data = []

    for i in range(len(experiment_list)):
        duplicate_catching_list = []

        for c in experiment_list[i]:  
            variable_list = [c[1], i + 1]
            
            variable_list.extend(Slice_String("|", c[0]))

            if (variable_list[2] not in COMPONENT_LIST) or (variable_list[2] in duplicate_catching_list):
                Error(f"ERROR: Nonexistant or duplicate Component in Line {c[1]}")
            duplicate_catching_list.append(variable_list[2])

            if (len(variable_list) != 4):
                Error(f"ERROR: Missing Vertical Slashes in line {c[1]}")

            sliced_constraint_data.append(variable_list)

    if (KIND == "Range"):
        for j in range(len(sliced_constraint_data)):
            range_list = Slice_String("/", sliced_constraint_data[j][3])

            for i in range(len(range_list)):
                new_r = Slice_String("-", range_list[i])
                range_list[i] = new_r

            sliced_constraint_data[j][3] = range_list

    if (KIND == "Range"):
        for i in range(TIMESTAMP_LENGTH):
            for c in sliced_constraint_data:
                for r in c[3]:
                    if((int(r[0]) <= i + 1) and (int(r[1]) >= i + 1)):
                        timestamp_list[c[1] - 1][i].append([c[2], r[2]])

    elif (KIND == "OString"):
        for j in range(OSTRING_LENGTH):
            for c in sliced_constraint_data:
                if (c[3][j] == "0"):
                    timestamp_list[c[1] - 1][j].append([c[2], "0"])
                else:
                    timestamp_list[c[1] - 1][j].append([c[2], "1"])

    else:
        Error("ERROR: Missing Component Appearence Input Data Type (OSTRING or Range)")

    return timestamp_list


# inputs: the timestamp list, and the specific experiment and timestamp
# outputs: the RE:IN formatted constraint of the timestamp
def Create_Experiment_Timestamp_Lines(timestamp_list, experiment_num, timestamp_num):
    constraints = timestamp_list[experiment_num][timestamp_num]

    if (len(constraints) == 0):
        return ""
    
    none_counter = 0
    for e in constraints:
        if (e == None):
            none_counter += 1

    restriction = f"$Restriction_{experiment_num + 1}_{timestamp_num + 1} :=\n" + "{\n\n"

    if (len(constraints) != 1):
        for i in range(len(constraints) - 1):
            if (constraints[i] != None):
                restriction += f"   {constraints[i][0]} = {constraints[i][1]} and\n"

    if (constraints[-1] != None):
        restriction += f"   {constraints[-1][0]} = {constraints[-1][1]}" + "\n\n};\n\n"
    else:
        if (none_counter != len(constraints)):
            restriction = restriction[:-5] + "\n\n};\n\n"
        else:
            restriction += "\n\n};\n\n"

    return restriction


# inputs: a take list
# outputs: a list of names for each experimental constraints file
def Generate_Name_Lists():
    final_name_lists = []

    for i in range(NUM_OF_EXPERIMENTS):
        final_name_lists.append([])

    for i in range(NUM_OF_EXPERIMENTS):
        for j in range(len(TAKE_LIST[i])):
            if (TAKE_LIST[i][j][0] == 1):
                final_name_lists[i].append(TAKE_LIST[i][j][4] + 1)
    
    return final_name_lists


# inputs: an experiment's number
# outputs: the constraints present according to the take list in the experiment
def Generate_Constraints_List(exp_num):
    constraint_list = []

    for i in range(len(TAKE_LIST[exp_num - 1])):
        if ((TAKE_LIST[exp_num - 1][i][1] == 1) and (TAKE_LIST[exp_num - 1][i][0] == 1)):
            constraint_list.append(TAKE_LIST[exp_num - 1][i][4])

    return constraint_list


# inputs: a take list
# outputs: strands all necassary components
def Add_Spaces_To_Take_List():
    for experiment in TAKE_LIST:
        total = len(experiment)
        i = 0
        while( i < total):
            if (experiment[i][2] == 1):
                for j in range(STRANDING_NUMBER):
                    experiment.insert(i + 1 + j, [0, 0, 0])
                    total += 1
            i += 1

    
# inputs: an experiment's number
# outputs: a line containing the experimental constraints of the experiment fuzzified using or statements
def Generate_Or_Statements(exp_num):    
    fuzzy_list = []
    or_statement_list = []
    final_string = ""

    for _ in range(len(TAKE_LIST[exp_num - 1]) + FUZZY_NUMBER):
        fuzzy_list.append([])

    for i in range(len(TAKE_LIST[exp_num - 1])):
        if ((TAKE_LIST[exp_num - 1][i][1] == 1) and (TAKE_LIST[exp_num - 1][i][0] == 1)):
            for j in range(i - FUZZY_NUMBER, i + FUZZY_NUMBER + 1):
                if (j >= 0):
                    fuzzy_list[j].append(TAKE_LIST[exp_num - 1][i][4])

    for c in Generate_Constraints_List(exp_num):
        line = ""
        for t in range(len(fuzzy_list)):
            if (c in fuzzy_list[t]):
                line  += f"(#Experiment_{exp_num}[{t}] |= $Restriction_{exp_num}_{c + 1}) or\n "
        line = line[:-5]

        or_statement_list.append(line)
    
    if (len(or_statement_list) != 0):
        for i in range(len(or_statement_list) - 1):
            final_string += f"{or_statement_list[i]}; \n\n"
        final_string += f"{or_statement_list[-1]};"
    
    return final_string


# inputs: the timestamp list
# outputs: the experiments formatted to specific files
def Create_Experiments(timestamp_list, final_string_list, KIND):
    for i in range(NUM_OF_EXPERIMENTS):
        file_name = f"{OUTPUT_NAME}_{final_name_lists[i]}_fz-{FUZZY_NUMBER}_st-{STRANDING_NUMBER}_{i}.txt"

        if (KEEP_FRAC != 1):
            file_name = f"{OUTPUT_NAME}_{final_name_lists[i]}_fz-{FUZZY_NUMBER}_st-{STRANDING_NUMBER}_frac-{KEEP_FRAC}.txt"

        if (KIND == "NO NAME LISTS"):
            file_name = f"biotapestry_experiment_{i + 1}.txt"
        file_path = STORAGE_PATH.joinpath(file_name)

        with open(file_path, 'w') as exp:
            for j in range(len(TAKE_LIST[i])):
                if (TAKE_LIST[i][j][0] == 1):
                    exp.write(Create_Experiment_Timestamp_Lines(timestamp_list, i + 1, TAKE_LIST[i][j][4] + 1))
                    for _ in range(2):
                        exp.write("\n")
            exp.write(final_string_list[i])


# inputs: error message
# outputs: prints the error message and closes
def Error(error_name):
    print(error_name)
    input()
    exit()


# inputs: a timestamp list
# outputs: deletes constraints in all of those which are needed
def Delete_Constraints_In_Timestamps(timestamp_list):
    for i in range(len(TAKE_LIST)):
        for j in range(len(TAKE_LIST[i])): 
            delete_num = int((1 - KEEP_FRAC) * len(timestamp_list[0][j]))
            delete_list = Generate_Delete_List(delete_num, timestamp_list[0][j])

            if (TAKE_LIST[i][j][3] == 1):
                for k in range(len(timestamp_list[0][j])):
                    if (k in delete_list):
                        print(f"DELETED: {timestamp_list[i][j][k][0]} = {timestamp_list[i][j][k][1]} | EXP: {i + 1} | TIMESTAMP: {j + 1}\n")
                        timestamp_list[0][j][k] = None
                        
    return timestamp_list


# inputs: the number of constraints to delete, and a timestamp
# outputs: a list of random elements to delete
def Generate_Delete_List(delete_num, timestamp):
    delete_list = []

    while (len(delete_list) != delete_num):
        new_num = r.randint(0, len(timestamp) - 1)
        if (new_num not in delete_list):
            delete_list.append(new_num)

    return delete_list


line_list = Get_Lines(f"{INPUT_NAME}.txt")

experiment_list = Filter_Lines(line_list, NUM_OF_EXPERIMENTS)

timestamp_list = Create_Timestamp_List(experiment_list, TIMESTAMP_LENGTH)

timestamp_list = Add_Constraints_To_Timestamps(timestamp_list, experiment_list, COMPONENT_LIST, KIND)

timestamp_list = Delete_Constraints_In_Timestamps(timestamp_list)

Add_Indexes_To_Take_List()

Add_Spaces_To_Take_List()

final_name_lists = Generate_Name_Lists()

final_string_list = []
for i in range(NUM_OF_EXPERIMENTS):
    final_string_list.append(Generate_Or_Statements(i + 1))

Create_Experiments(timestamp_list, final_string_list, "NAME LISTS")

print("EXPERIMENT(S) CREATED SUCCESFULLY")