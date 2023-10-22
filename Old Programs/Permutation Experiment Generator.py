"""
________________________________________________________________________________________________________________________________________
PERMUTATION EXPERIMENT GENERATOR

This program allows the generation of RE:IN experimental constraints by locating untranslated input data
from a file, and translating it to constraints for several experiments.

The general experiment generator also allows to generate all ways constraints can occur in time according to given data.
Furthermore, the general experiment generator can delete parts of constraints to ease them, and write down the deleted information.
________________________________________________________________________________________________________________________________________
INPUTS

TAKE LIST: Explained below.

INPUT NAME: The name of the untranslated data file.
OUTPUT NAME: The main name of the output files (doesn't include restrictions used, only the number of experiment in some experiment)
OUTPUT_FILES_FOLDER: The file in which the constraints are stored (for families of constraints).

STORAGE PATH: Where to store the results.
DATA PATH: Where to get the data from.

NUM OF EXPERIMENTS: The number of experiments in the TAKE LIST.
DELETE FRAC: The fraction of elements to delete from constraints that are needed to be shaved.
OSTRING LENGTH: If the constraint data is written in OStrings, how long each is.

COMPONENT LIST: The list of all legal components in an ABN.
________________________________________________________________________________________________________________________________________
FORCED EXPRESSION KNOCKOUT LIST: A list of all components which should be FEed or KOed.
The list can be defined 2 ways:

1. Generate all combinations of certain genes: in which case specify in this format:

["COMB", [(1)], (2), [(3)], (4)]

(1) - List of components to perturb. Everey element in the list is a tuple of components which would be treated as a single element.
(2) - The number of components in a combination (i.e. all combinations of 3 components).
(3) - List of experiments to perturb in.
(4) - Whether to KO or FE (0 and 1 respectively).
CURRENTLY THERE IS NO FUNCTIONALITY TO GENERATE COMBINATIONS OF DIFFERENTLY PERTURBED GENES.

2. Perturb specific genes: in which case specify in this format:

["REG", [(1), [(2)], (3)], ... [(1), [(2)], (3)]]

(1) - The name of a perturbed component.
(2) - List of experiments to perturb in.
(3) - Whether to KO or FE (0 and 1 respectively).

3. Not perturb:

[]

Leave the list empty, and the program will automatically recognize no perturbation needs to take place.
________________________________________________________________________________________________________________________________________
"""


import pathlib as p
import random as r
import os
import shutil
import itertools as itt


# first element in [1, ["1-1", "1-2"], 0] tells whether to use the constraint on the timestamp or not
# the second element in [1, ["1-1", "1-2"], 0] tells in what time ranges the constraint can appear
# the third element tells whether to delete interactions in it or not


fz = 5
st = 10
name = f"Hours 21, 24, 25, 26"


TAKE_LIST = [[[1, [f"0-{fz}"], 1], [0, [f"{st + 1 - fz}-{st + 1 + fz}"], 1], [0, [f"{2*(st + 1) - fz}-{2*(st + 1) + fz}"], 1], [1, [f"{3*(st + 1) - fz}-{3*(st + 1) + fz}"], 1], [1, [f"{4*(st + 1) - fz}-{4*(st + 1) + fz}"], 1], 
              [1, [f"{5*(st + 1) - fz}-{5*(st + 1) + fz}"], 1], [0, [f"{6*(st + 1) - fz}-{6*(st + 1) + fz}"], 1], [0, [f"{7*(st + 1) - fz}-{7*(st + 1) + fz}"], 1], [0, [f"{8*(st + 1) - fz}-{8*(st + 1) + fz}"], 1], [0, [f"{9*(st + 1) - fz}-{9*(st + 1) + fz}"], 1]]]


TYPE = "Domain-Divided"
INPUT_NAME = f"{TYPE}_Input_Constraints"
OUTPUT_NAME = f"{TYPE}_Constraints_{name}"
OUTPUT_FILES_FOLDER = f"{name}"

STORAGE_PATH = p.Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Experimental Constraints Storage\{TYPE}\{OUTPUT_FILES_FOLDER}")
DATA_PATH = p.Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Untranslated Input Data\{TYPE}")

NUM_OF_EXPERIMENTS = len(TAKE_LIST)

max = 0
PERTURBATION_PLACE = []
no_first_stamp = True

for i in range(len(TAKE_LIST)):
    no_first_stamp = True

    for j in range(len(TAKE_LIST[i])):
        if (TAKE_LIST[i][j][0] == 1):
            PERTURBATION_PLACE.append(j)
            no_first_stamp = False
            break
    if (no_first_stamp):
        PERTURBATION_PLACE.append(-1)

for i in range(len(TAKE_LIST)):
    if (len(TAKE_LIST[i]) > max):
        max = len(TAKE_LIST[i])

NUM_OF_TIMESTAMPS = max

DELETE_FRAC = 0
OSTRING_LENGTH = 10
CONSTRAINT_FORMAT = "OString"

COMPONENT_LIST = ['nodal_ecto_oralNSM', 'smad_not_protien_oralNSM', 'smad_oralNSM', 'not_oralNSM', 'unkn_runx_oralNSM', 'unkn_gatac_oralNSM', 'gatac_oralNSM', 'unkn_scl_oralNSM', 'scl_oralNSM', 'runx_oralNSM', 'ese_oralNSM', 'prox_oralNSM', 'r11pmdelta_oralNSM', 'r11pmdelta_nrl_protien_oralNSM', 'nrl_oralNSM', 'unkn_nrl_oralNSM', 'blimp1_oralNSM', 'blimp1_activate_oralNSM', 'hesc_oralNSM', 'ets1_oralNSM', 'unkn_ets1_oralNSM', 'otx_oralNSM', 'gcm_oralNSM', 'six12_oralNSM', 'gatae_oralNSM', 'erg_oralNSM', 'hex_oralNSM', 'tbr_oralNSM', 'not_aboralNSM', 'gcm_aboralNSM', 'six12_aboralNSM', 'gatae_aboralNSM', 'unkn_runx_aboralNSM', 'runx_aboralNSM', 'ese_aboralNSM', 'prox_aboralNSM', 'alx1_aboralNSM', 'gatac_aboralNSM', 'z166_aboralNSM', 'otx_aboralNSM', 'blimp1_aboralNSM', 'blimp1_activate_aboralNSM', 'hesc_aboralNSM', 'ets1_aboralNSM', 'nrl_aboralNSM', 'r11pmdelta_nrl_protien_aboralNSM', 'r11pmdelta_aboralNSM', 'fog_aboralNSM', 'gatae_fog_protien_aboralNSM', 'erg_aboralNSM', 'hex_aboralNSM', 'capk_oralNSM_diff', 'decorin_oralNSM_diff', 'capk_aboralNSM_diff', 'decorin_aboralNSM_diff', 'pks_aboralNSM_diff', 'sutx_aboralNSM_diff', 'dpt_aboralNSM_diff', 'fvmo123_aboralNSM_diff', 'notch_smallMIC', 'suhn_smallMIC', 'notch_suhn_protien_smallMIC', 'suh_smallMIC', 'suh_notch_suhn_protien_smallMIC', 'foxy_smallMIC', 'unkn_soxe_smallMIC', 'soxe_smallMIC', 'smo_smallMIC', 'ptc_smallMIC', 'smo_ptc_hh_protien_smallMIC', 'foxf_smallMIC', 'gsk3_veg_endo_1', 'wnt8_veg_endo_1', 'frizzled_veg_endo_1', 'eve_veg_endo_1', 'hox1113b_veg_endo_1', 'otx_veg_endo_1', 'hnf1_veg_endo_1', 'signalv2_veg_endo_1', 'vegf3_veg_endo_1', 'gsk3_x_protien_veg_endo_1', 'gsk3_x_nbtcf_protien_veg_endo_1', 'bra_veg_endo_1', 'nbtcf_protien_veg_ecto_1', 'eve_veg_ecto_1', 'unc41_veg_ecto_1', 'vegf3_veg_ecto_1', 'unkn_soxb1_veg_endo_2', 'soxb1_veg_endo_2', 'wnt16_veg_endo_2', 'nbtcf_protien_veg_endo_2', 'eve_veg_endo_2', 'soxc_veg_endo_2', 'otx_veg_endo_2', 'blimp1_veg_endo_2', 'hox1113b_veg_endo_2', 'gatae_veg_endo_2', 'foxa_veg_endo_2', 'bra_veg_endo_2', 'gcm_veg_endo_2', 'krl_veg_endo_2', 'myc_veg_endo_2', 'brn124_veg_endo_2', 'tgif_veg_endo_2', 'hh_veg_endo_2', 'dac_veg_endo_2', 'endo16_veg_endo_2', 'wnt16_hox1113b_protien_veg_endo_2', 'signalv2_protien_veg_endo_1', 'g_cadherin_MAT', 'otx_MAT', 'cb_MAT', 'wnt6_MAT', 'soxb1_MAT', 'nucl_protien_PMC', 'ecns_protien_PMC', 'nbtcf_protien_PMC', 'gsk3_PMC', 'x_protien_PMC', 'blimp1_PMC', 'wnt8_PMC', 'ubiq_soxc_PMC', 'soxc_PMC', 'ubiq_es_PMC', 'es_PMC', 'pmar1_PMC', 'ubiq_hesc_PMC', 'hesc_PMC', 'gcm_PMC', 'activin_b_PMC', 'rhoa_PMC', 'rhoa_mat_soxb1_protien_PMC', 'r11pmdelta_nrl_protien_PMC', 'ubiq_hnf6_PMC', 'hnf6_PMC', 'alx1_PMC', 'ubiq_ets1_PMC', 'ets1_PMC', 'tbr_PMC', 'nrl_PMC', 'hex_PMC', 'erg_PMC', 'tgif_PMC', 'ubiq_tel_PMC', 'tel_PMC', 'foxn23_PMC', 'r11pmdelta_PMC', 'dri_PMC', 'foxb_PMC', 'foxo_PMC', 'vegfr_PMC', 'l1_PMC', 'l1_vegfr_vegf3_protien_PMC', 'sm27_Skel', 'sm50_Skel', 'msp130_Skel', 'mspl_Skel', 'sm30_Skel', 'ficolin_Skel', 'cyp_Skel', 'ubiq_gcadherin_Skel', 'gcadherin_Skel']

FE_KO_LIST = []

#["COMB", [("blimp1_oralNSM", "blimp1_aboralNSM", "blimp1_veg_endo_2", "blimp1_PMC"), ("bra_veg_endo_1", "bra_veg_endo_2"), ("eve_veg_endo_1", "eve_veg_endo_2", "eve_veg_ecto_1"), ("foxa_veg_endo_2",), ("gatae_oralNSM", "gatae_aboralNSM", "gatae_veg_endo_2"), ("gcm_oralNSM", "gcm_aboralNSM", "gcm_veg_endo_2", "gcm_PMC"), ("hox1113b_veg_endo_1", "hox1113b_veg_endo_2"), ("krl_veg_endo_2",), ("myc_veg_endo_2",), ("otx_oralNSM", "otx_aboralNSM", "otx_veg_endo_2", "otx_veg_endo_1"), ("soxc_veg_endo_2",)], 2, [1], 1]

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


# inputs: error message
# outputs: prints the error message and closes
def Error(error_name):
    print(error_name)
    input()
    exit()


# inputs: a list
# outputs: the elements of the list
def Print_List(list_printed):
    for e in list_printed:
        print(e)


# inputs: the name of the input file of the constraints
# outputs: the lines of the input file, and their placement in the file
def Get_Lines(constraint_file):
    new_path = DATA_PATH.joinpath(constraint_file)
    with open(new_path) as exp:
        line_list = exp.readlines()

    for i in range(len(line_list) - 1):
        line_list[i] = [line_list[i][:-1], i + 1]
    line_list[-1] = [line_list[-1], len(line_list)] 

    return line_list


# inputs: a line list, the number of experiments
# outputs: filters the lines into a list of ESs in their respective experiments
def Filter_Lines(line_list):
    constraint_in_exp = []
    for _ in range(NUM_OF_EXPERIMENTS):
        constraint_in_exp.append([])

    for line in line_list: # delete # before constraint line
        if (line[0][0] == "#"):
            line[0] = line[0][1:]

            stop_place = line[0].find("|")
            if (stop_place != -1):
                exp_num = int(line[0][:stop_place])

                if (not((0 < exp_num) and (exp_num <= NUM_OF_EXPERIMENTS))):
                    Error(f"Line {line[1]} uses experiments not in the set range of 1 to {NUM_OF_EXPERIMENTS}")

                constraint_in_exp[exp_num - 1].append([line[0][stop_place + 1:], line[1]])
            else:
                Error(f"No '|' after experiment number in line {line[1]}")

    return constraint_in_exp


# inputs: ESs seperated into experiments, and the number of timestamps
# outputs: a list of experiment lists of timestamp lists of components and their values at the stamps
def Initialize_Stamp_List():
    stamp_list = []

    for _ in range(len(TAKE_LIST)):
        stamp_list.append([])

    for i in range(len(TAKE_LIST)):    
        for _ in range(NUM_OF_TIMESTAMPS):
            stamp_list[i].append([])

    return stamp_list


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
def Add_Constraints_To_Timestamps(stamp_list, constraint_in_exp, component_list, perturbed_list):
    sliced_constraint_data = []

    for i in range(NUM_OF_EXPERIMENTS):
        previous_name_list = []

        for c in constraint_in_exp[i]:  
            variable_list = [c[1], i + 1]
            variable_list.extend(Slice_String("|", c[0]))

            if (variable_list[2] not in component_list) or (variable_list[2] in previous_name_list):
                if (variable_list[2][3:-1] not in component_list):
                    Error(f"ERROR: Nonexistant or Duplicate Component in Line {c[1]}")

            previous_name_list.append(variable_list[2])

            if (len(variable_list) != 4):
                Error(f"ERROR: Missing Vertical Slashes in line {c[1]}")

            sliced_constraint_data.append(variable_list)

    if (CONSTRAINT_FORMAT == "Range"):
        for j in range(len(sliced_constraint_data)):
            range_list = Slice_String("/", sliced_constraint_data[j][3])

            for i in range(len(range_list)):
                new_r = Slice_String("-", range_list[i])
                range_list[i] = new_r

            sliced_constraint_data[j][3] = range_list

    if (CONSTRAINT_FORMAT == "Range"):
        for c in sliced_constraint_data:
            if c[3][0][0] == "P":
                stamp_list[c[1] - 1][PERTURBATION_PLACE[c[1] - 1]].append([c[2], c[3][0][1]])

        for i in range(NUM_OF_TIMESTAMPS):
            for c in sliced_constraint_data:
                if c[3][0][0] == "P":
                    pass
                else:
                    if c[2] not in perturbed_list:
                        for r in c[3]:
                            if((int(r[0]) <= i + 1) and (int(r[1]) >= i + 1)):
                                stamp_list[c[1] - 1][i].append([c[2], r[2]])

    elif (CONSTRAINT_FORMAT == "OString"):
        for c in sliced_constraint_data:
            if c[3][0] == "P":
                stamp_list[c[1] - 1][PERTURBATION_PLACE[c[1] - 1]].append([c[2], c[3][1]])

        for j in range(OSTRING_LENGTH):
            for c in sliced_constraint_data:
                if c[3][0] == "P":
                    pass
                else:
                    if c[2] not in perturbed_list:
                        if (c[3][j] == "0"):
                            stamp_list[c[1] - 1][j].append([c[2], "0"])
                        else:
                            stamp_list[c[1] - 1][j].append([c[2], "1"])

    else:
        Error("ERROR: Illegal or missing CONSTRAINT_FORMAT (OSTRING or Range)")

    return stamp_list


# inputs: the timestamp list, and the specific experiment and timestamp
# outputs: the RE:IN formatted constraint of the timestamp
def Create_Experiment_Timestamp_Lines(stamp_list, exp_num, stamp_num):
    constraints = stamp_list[exp_num][stamp_num]

    if (len(constraints) == 0):
        return ""
    
    none_counter = 0
    for e in constraints:
        if (e == None):
            none_counter += 1

    restriction = f"$Restriction_{exp_num + 1}_{stamp_num + 1} :=\n" + "{\n\n"

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
# outputs: a last to first list of timestamps with ranges
def Generate_Stamp_Constraint_List():
    stamp_constraint_list = []
    for _ in range(len(TAKE_LIST)):
        stamp_constraint_list.append([])

    for i in range(len(TAKE_LIST)):
        for j in range(len(TAKE_LIST[i])):
            if (TAKE_LIST[i][j][0] == 1):
                range_list = []
                for r in TAKE_LIST[i][j][1]:
                    full_list = Slice_String("-", r)
                    for k in range(int(full_list[0]), int(full_list[1]) + 1):
                        range_list.append(k)

                stamp_constraint_list[i].append([i , j, range_list, TAKE_LIST[i][j][2]]) # j is the exp num, i is the timestamp num

    for i in range(len(stamp_constraint_list)):
        stamp_constraint_list[i].reverse()

    return stamp_constraint_list


# inputs: a last to first list of timestamps
# outputs: all possible downward trend permutations of the timestamps with their ranges of a single experiment
def Generate_Permutations_1_Experiment(reversed_stamp_constraint_list_1_exp):
    permutation_list = []

    for e in reversed_stamp_constraint_list_1_exp[0][2]:
        permutation_list.append([[e, reversed_stamp_constraint_list_1_exp[0][0], reversed_stamp_constraint_list_1_exp[0][1]]])

    for i in range(len(reversed_stamp_constraint_list_1_exp) - 1):
        new_permutation_list = []
        for p in permutation_list:
            for smaller in Find_All_Smaller(p[i][0], reversed_stamp_constraint_list_1_exp[i + 1]):
                pending_list = []
                for e in p:
                    pending_list.append(e)
                pending_list.append(smaller)

                new_permutation_list.append(pending_list)

        permutation_list = new_permutation_list

    for i in range(len(permutation_list)):
        permutation_list[i].reverse()

    return permutation_list


# inputs: a last to first list of timestamps
# outputs: all possible downward trend permutations of the timestamps with their ranges of all experiments
def Generate_Permutations_All_Experiments(reversed_stamp_constraint_list):
    all_permutations = []

    for i in range(len(reversed_stamp_constraint_list)):
        all_permutations.append(Generate_Permutations_1_Experiment(reversed_stamp_constraint_list[i]))

    return all_permutations


# inputs: a constraint and a number
# outputs: all elements in the list smaller than the number
def Find_All_Smaller(num, constraint):
    new_constraint = []

    for e in constraint[2]:
        if (e < num):
            new_constraint.append([e, constraint[0], constraint[1]])

    return new_constraint


# inputs: a permutation
# outputs: a stamped constraint statment as written in RE:IN
def Generate_Constraint_Line(permutation):
    line = "("

    for i in range(len(permutation) - 1):
        line += f"(#Experiment_{permutation[i][1] + 1}[{permutation[i][0]}] |= $Restriction_{permutation[i][1] + 1}_{permutation[i][2] + 1}) and\n"
    line += f"(#Experiment_{permutation[-1][1] + 1}[{permutation[-1][0]}] |= $Restriction_{permutation[-1][1] + 1}_{permutation[-1][2] + 1})) or\n\n"

    return line


# inputs: a permutation list
# outputs: all stamped constraint statments in RE:IN format
def Generate_Constraint_Lines(permutation_list):
    exp_line_list = []

    for i in range(len(permutation_list)):
        exp_line = ""

        for j in range(len(permutation_list[i])):
            exp_line += Generate_Constraint_Line(permutation_list[i][j])
            
        exp_line_list.append(f"{exp_line[:-5]};\n\n\n")

    return exp_line_list


stamp_constraint_list = Generate_Stamp_Constraint_List()

permutation_list = Generate_Permutations_All_Experiments(stamp_constraint_list)

exp_line_list = Generate_Constraint_Lines(permutation_list)


# inputs: a timestamp list
# outputs: deletes constraints in all of those which are needed
def Delete_Constraints_In_Timestamps(stamp_list):
    for i in range(len(TAKE_LIST)):
        for j in range(len(TAKE_LIST[i])): 
            delete_num = int((DELETE_FRAC) * len(stamp_list[i][j]))
            delete_list = Generate_Delete_List(delete_num, stamp_list[i][j])

            if (TAKE_LIST[i][j][2] == 1):
                for k in range(len(stamp_list[i][j])):
                    if (k in delete_list):
                        print(f"DELETED: {stamp_list[i][j][k][0]} = {stamp_list[i][j][k][1]} | EXP: {i + 1} | TIMESTAMP: {j + 1}\n")
                        stamp_list[i][j][k] = None

    return stamp_list


# inputs: the number of constraints to delete, and a timestamp
# outputs: a list of random elements to delete
def Generate_Delete_List(delete_num, timestamp):
    delete_list = []

    while (len(delete_list) != delete_num):
        new_num = r.randint(0, len(timestamp) - 1)
        if (new_num not in delete_list):
            delete_list.append(new_num)

    return delete_list


# inputs: the timestamp list
# outputs: the experiments formatted to specific files
def Create_Experiments(stamp_lists, exp_line_list, count):
    for i in range(NUM_OF_EXPERIMENTS):
        file_name = f"{OUTPUT_NAME}_{i + 1}_{count}.txt"
        file_path = STORAGE_PATH.joinpath(file_name)

        with open(file_path, 'w') as exp:
            for j in range(len(stamp_lists[i])):
                exp.write(Create_Experiment_Timestamp_Lines(stamp_lists, i, j))

            for _ in range(2):
                exp.write("\n")
            exp.write(exp_line_list[i])


# inputs: the original line list
# outputs: runs all experiment creation steps over the perturbed components
def Run_With_Perturbations():
    if not FE_KO_LIST:
        line_list = Get_Lines(f"{INPUT_NAME}.txt")

        Run(line_list, [], 1)

        print("EXPERIMENT(S) CREATED SUCCESFULLY")
        exit()

    elif FE_KO_LIST[0] == "COMB":
        if FE_KO_LIST[1][0] == "ALL":
            components_in_tuples = []

            for c in COMPONENT_LIST:
                components_in_tuples.append((c,))

            used_list = list(itt.combinations(components_in_tuples, FE_KO_LIST[2]))
        else:
            used_list = list(itt.combinations(FE_KO_LIST[1], FE_KO_LIST[2]))

        count = 0

        for tuple in used_list:
            count += 1   
            perturbed_elements = []

            for t in tuple:
                for e in t:
                    if (e not in perturbed_elements):
                        perturbed_elements.append(e)

            line_list = Get_Lines(f"{INPUT_NAME}.txt")

            for c in perturbed_elements:

                for exp in FE_KO_LIST[3]:

                    if CONSTRAINT_FORMAT == "OString":
                        if (FE_KO_LIST[4] == 0):
                            line_list.append([f"#{exp}|KO({c})|P{FE_KO_LIST[4]}", -1])
                        else:
                            line_list.append([f"#{exp}|FE({c})|P{FE_KO_LIST[4]}", -1])

                    elif CONSTRAINT_FORMAT == "Range":
                        if (FE_KO_LIST[4] == 0):
                            line_list.append([f"#{exp}|KO({c})|P{FE_KO_LIST[4]}", -1])
                        else:
                            line_list.append([f"#{exp}|FE({c})|P{FE_KO_LIST[4]}", -1])
                    
                    else:
                        Error("ERROR: Missing Component Appearence Input Data Type (OSTRING or Range)")

            Run(line_list, perturbed_elements, count)

        print("EXPERIMENT(S) CREATED SUCCESFULLY")
        exit()

    elif FE_KO_LIST[0] == "REG":
        line_list = Get_Lines(f"{INPUT_NAME}.txt")
        for c in FE_KO_LIST[1:]:

            if c[0] in COMPONENT_LIST:
                perturbed_list = []
                perturbed_list.append(c[0])

                for exp in c[1]:
                    if CONSTRAINT_FORMAT == "OString":
                        if (c[2] == 0):
                            line_list.append([f"#{exp}|KO({c[0]})|P{c[2]}", -1])
                        else:
                            line_list.append([f"#{exp}|FE({c[0]})|P{c[2]}", -1])

                    elif CONSTRAINT_FORMAT == "Range":
                        if (c[2] == 0):
                            line_list.append([f"#{exp}|KO({c[0]})|P{c[2]}", -1])
                        else:
                            line_list.append([f"#{exp}|FE({c[0]})|P{c[2]}", -1])
                    
                    else:
                        Error("ERROR: Missing Component Appearence Input Data Type (OSTRING or Range)")

            else:
                Error(f"ERROR: The component {c[0]}, which is perturbed, does not exist in the component list provided")

        Run(line_list, perturbed_list, 1)

        print("EXPERIMENT(S) CREATED SUCCESFULLY")
        exit()

    else:
        Error(f'ERROR: No FE_KO_LIST format specified (No perturbations, "COMB", or "REG")')


# inputs: a line list
# outputs: creates an experiment for the line list
def Run(line_list, perturbed_list, count):
    constraint_in_exp = Filter_Lines(line_list)

    stamp_list = Initialize_Stamp_List()

    stamp_list = Add_Constraints_To_Timestamps(stamp_list, constraint_in_exp, COMPONENT_LIST, perturbed_list)

    stamp_list = Delete_Constraints_In_Timestamps(stamp_list)

    Create_Experiments(stamp_list, exp_line_list, count)


Make_Folder()

Run_With_Perturbations()