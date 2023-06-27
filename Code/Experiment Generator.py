from pathlib import Path


TYPE = "Domain-Divided"
INPUT_NAME = "Domain-Divided_Input_Constraints_1"
OUTPUT_NAME = "Domain-Divided_Constraints_1"

STORAGE_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Model Translator\Experimental Constraints Storage\{TYPE}")
DATA_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Model Translator\Untranslated Input Data\{TYPE}")

NUM_OF_EXPERIMENTS = 1
OSTRING_LENGTH = 10

TAKE_LIST = [[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], 
             [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],

             [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
             [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],

             [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
             [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],

             [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
             [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

FUZZY_NUMBER = 3
STRANDING_NUMBER = 10
TIMESTAMP_LENGTH = 30 + (9 * STRANDING_NUMBER)

KIND = "OString"
component_list = ['nodal_ecto_oralNSM', 'smad_not_protien_oralNSM', 'smad_oralNSM', 'not_oralNSM', 'unkn_runx_oralNSM', 'unkn_gatac_oralNSM', 'gatac_oralNSM', 'unkn_scl_oralNSM', 'scl_oralNSM', 'runx_oralNSM', 'ese_oralNSM', 'prox_oralNSM', 'r11pmdelta_oralNSM', 'r11pmdelta_nrl_protien_oralNSM', 'nrl_oralNSM', 'unkn_nrl_oralNSM', 'blimp1_oralNSM', 'blimp1_activate_oralNSM', 'hesc_oralNSM', 'ets1_oralNSM', 'unkn_ets1_oralNSM', 'otx_oralNSM', 'gcm_oralNSM', 'six12_oralNSM', 'gatae_oralNSM', 'erg_oralNSM', 'hex_oralNSM', 'tbr_oralNSM', 'not_aboralNSM', 'gcm_aboralNSM', 'six12_aboralNSM', 'gatae_aboralNSM', 'unkn_runx_aboralNSM', 'runx_aboralNSM', 'ese_aboralNSM', 'prox_aboralNSM', 'alx1_aboralNSM', 'gatac_aboralNSM', 'z166_aboralNSM', 'otx_aboralNSM', 'blimp1_aboralNSM', 'blimp1_activate_aboralNSM', 'hesc_aboralNSM', 'ets1_aboralNSM', 'unkn_ets1_aboralNSM', 'nrl_aboralNSM', 'r11pmdelta_nrl_protien_aboralNSM', 'r11pmdelta_aboralNSM', 'fog_aboralNSM', 'gatae_fog_protien_aboralNSM', 'erg_aboralNSM', 'hex_aboralNSM', 'capk_oralNSM_diff', 'decorin_oralNSM_diff', 'capk_aboralNSM_diff', 'decorin_aboralNSM_diff', 'pks_aboralNSM_diff', 'sutx_aboralNSM_diff', 'dpt_aboralNSM_diff', 'fvmo123_aboralNSM_diff', 'notch_smallMIC', 'suhn_smallMIC', 'notch_suhn_protien_smallMIC', 'suh_smallMIC', 'suh_notch_suhn_protien_smallMIC', 'foxy_smallMIC', 'unkn_soxe_smallMIC', 'soxe_smallMIC', 'smo_smallMIC', 'ptc_smallMIC', 'smo_ptc_hh_protien_smallMIC', 'foxf_smallMIC', 'gsk3_veg_endo_1', 'wnt8_veg_endo_1', 'eve_veg_endo_1', 'hox1113b_veg_endo_1', 'otx_veg_endo_1', 'hnf1_veg_endo_1', 'signalv2_veg_endo_1', 'vegf3_veg_endo_1', 'gsk3_x_protien_veg_endo_1', 'x_nbtcf_protien_veg_endo_1', 'bra_veg_endo_1', 'nbtcf_protien_veg_ecto_1', 'eve_veg_ecto_1', 'unc41_veg_ecto_1', 'vegf3_veg_ecto_1', 'unkn_soxb1_veg_endo_2', 'soxb1_veg_endo_2', 'wnt16_veg_endo_2', 'nbtcf_protien_veg_endo_2', 'eve_veg_endo_2', 'soxc_veg_endo_2', 'otx_veg_endo_2', 'blimp1_veg_endo_2', 'hox1113b_veg_endo_2', 'gatae_veg_endo_2', 'foxa_veg_endo_2', 'bra_veg_endo_2', 'gcm_veg_endo_2', 'krl_veg_endo_2', 'myc_veg_endo_2', 'brn124_veg_endo_2', 'tgif_veg_endo_2', 'hh_veg_endo_2', 'dac_veg_endo_2', 'endo16_veg_endo_2', 'wnt16_veg_endo_2_protien', 'signalv2_protien_veg_endo_1', 'g_cadherin_MAT', 'otx_MAT', 'cb_MAT', 'wnt6_MAT', 'soxb1_MAT', 'nucl_protien_PMC', 'ecns_protien_PMC', 'nbtcf_protien_PMC', 'gsk3_PMC', 'x_protien_PMC', 'blimp1_PMC', 'wnt8_PMC', 'ubiq_soxc_PMC', 'soxc_PMC', 'ubiq_es_PMC', 'es_PMC', 'pmar1_PMC', 'ubiq_hesc_PMC', 'hesc_PMC', 'gcm_PMC', 'activin_b_PMC', 'rhoa_PMC', 'rhoa_mat_soxb1_protien_PMC', 'r11pmdelta_nrl_protien_PMC', 'ubiq_hnf6_PMC', 'hnf6_PMC', 'alx1_PMC', 'ubiq_ets1_PMC', 'ets1_PMC', 'tbr_PMC', 'nrl_PMC', 'hex_PMC', 'erg_PMC', 'tgif_PMC', 'ubiq_tel_PMC', 'tel_PMC', 'foxn23_PMC', 'r11pmdelta_PMC', 'r11pmdelta_PMC', 'dri_PMC', 'foxb_PMC', 'foxo_PMC', 'vegfr_PMC', 'l1_PMC', 'l1_vegfr_vegf3_protien_PMC', 'sm27_Skel', 'sm50_Skel', 'msp130_Skel', 'mspl_Skel', 'sm30_Skel', 'ficolin_Skel', 'cyp_Skel', 'ubiq_gcadherin_Skel', 'gcadherin_Skel']

# inputs: a take list
# outputs: a list of names for each experimental constraints file
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
def Filter_Lines(line_list, NUM_OF_EXPERIMENTS):
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
        for j in range(TIMESTAMP_LENGTH):
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
def Add_Constraints_To_Timestamps(timestamp_list, experiment_list, component_list, KIND):
    sliced_constraint_data = []
    
    for i in range(len(experiment_list)):
        for c in experiment_list[i]:  
            variable_list = [c[1], i + 1]
            
            variable_list.extend(Slice_String("|", c[0]))

            if (variable_list[2] not in component_list):
                Error(f"ERROR: Nonexistant Component in Line {c[1]}")

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
    constraints = timestamp_list[experiment_num - 1][timestamp_num - 1]

    if (len(constraints) == 0):
        return ""

    restriction = f"$Restriction_{experiment_num}_{timestamp_num} :=\n" + "{\n\n"

    if (len(constraints) != 1):
        for i in range(len(constraints) - 1):
            restriction += f"   {constraints[i][0]} = {constraints[i][1]} and\n"
    restriction += f"   {constraints[-1][0]} = {constraints[-1][1]}" + "\n\n};"

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
                final_name_lists[i].append(TAKE_LIST[i][j][3] + 1)
    
    return final_name_lists


# inputs: an experiment's number
# outputs: the constraints present according to the take list in the experiment
def Generate_Constraints_List(exp_num):
    constraint_list = []

    for i in range(len(TAKE_LIST[exp_num - 1])):
        if (TAKE_LIST[exp_num - 1][i][1] == 1):
            constraint_list.append(TAKE_LIST[exp_num - 1][i][3])

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
        if (TAKE_LIST[exp_num - 1][i][1] == 1):
            for j in range(i - FUZZY_NUMBER, i + FUZZY_NUMBER + 1):
                if (j >= 0):
                    fuzzy_list[j].append(TAKE_LIST[exp_num - 1][i][3])

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
        file_name = f"{OUTPUT_NAME}_{final_name_lists[i]}_fz-{FUZZY_NUMBER}_st-{STRANDING_NUMBER}.txt"
        if (KIND == "NO NAME LISTS"):
            file_name = f"biotapestry_experiment_{i + 1}.txt"
        file_path = STORAGE_PATH.joinpath(file_name)

        with open(file_path, 'w') as exp:
            for j in range(len(TAKE_LIST[i])):
                if (TAKE_LIST[i][j][0] == 1):
                    exp.write(Create_Experiment_Timestamp_Lines(timestamp_list, i + 1, TAKE_LIST[i][j][3] + 1))
                    for _ in range(2):
                        exp.write("\n")
            exp.write(final_string_list[i])


# inputs: error message
# outputs: prints the error message and closes
def Error(error_name):
    print(error_name)
    input()
    exit()


Add_Indexes_To_Take_List()

Add_Spaces_To_Take_List()

final_name_lists = Generate_Name_Lists()

line_list = Get_Lines(f"{INPUT_NAME}.txt")

experiment_list = Filter_Lines(line_list, NUM_OF_EXPERIMENTS)

timestamp_list = Create_Timestamp_List(experiment_list, TIMESTAMP_LENGTH)

timestamp_list = Add_Constraints_To_Timestamps(timestamp_list, experiment_list, component_list, KIND)

final_string_list = []
for i in range(NUM_OF_EXPERIMENTS):
    final_string_list.append(Generate_Or_Statements(i + 1))

Create_Experiments(timestamp_list, final_string_list, "NAME LISTS")

print("DONE")