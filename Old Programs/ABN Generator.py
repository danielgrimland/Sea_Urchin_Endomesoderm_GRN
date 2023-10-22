"""
________________________________________________________________________________________________________________________________________
ABN GENERATOR

This program allows the generation of an ABN from untranslated data.
________________________________________________________________________________________________________________________________________
INPUTS

INPUT NAME: The name of the untranslated data file.
OUTPUT NAME: The main name of the output files (without specific details on the contents).

STORAGE PATH: Where to store the results.
DATA PATH: Where to get the data from.

TYPE: The specific file of the input and output data (if the ABN is of a Domain-Divided system, Full-Genome, etc.).
KIND:   optional: all interactions are optional (so give the file the ending "_optional").
        definite: all interactions are as normal (so give the file the ending "_definite").
        hours: ABN is seperated into models of it in different hours (so give each file an ending equal to its hour").  

HOUR1: The first hour of the system.
HOUR2: The last hour of the system.
O: important constant.

TIME DELAY: number of auxilary components to create for each interaction (as to induce time delays between activation and inhibitation).
________________________________________________________________________________________________________________________________________
"""


from pathlib import Path

TYPE = "Domain-Divided"
TIME_DELAY = 3

INPUT_NAME = f"{TYPE}_Input_ABN_all_optional"
OUTPUT_NAME =  f"{TYPE}_ABN_Delayed_{TIME_DELAY}"

KIND = "optional"

HOUR1 = 21
HOUR2 = 30
O = -1 * (HOUR2 - HOUR1 + 1)

STORAGE_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\ABN Storage\{TYPE}")
DATA_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Untranslated Input Data\{TYPE}")


# inputs: an array
# outputs: an array composed only of unique elements
def Remove_Copies(line_list):
    new_line_list = []
    previous_components = []
    for line in line_list:
        if (not(line[0] in previous_components)):
            new_line_list.append(line)
            previous_components.append(line[0])

    return new_line_list


# inputs: a .txt file name
# outputs: a list containing each line of the file. the lines have the default /n deleted
def Get_Lines(data_file):
    new_path = DATA_PATH.joinpath(data_file)
    with open(new_path) as model:
        line_list = model.readlines()

    for i in range(len(line_list) - 1):
        line_list[i] = [line_list[i][:-1], i + 1]
    line_list[-1] = [line_list[-1], len(line_list)] 

    return Remove_Copies(line_list)


# inputs: a list
# outputs: the elements of the list
def Print_List(list_printed):
    for e in list_printed:
        print(e)


# inputs: a line list
# outputs: filters the lines to a component line list and an interaction line list
def Filter_Lines(line_list):
    component_list = []
    interaction_list = []

    for line in line_list:
        if (line[0][0] == "*"):
            component_list.append([line[0][1:], line[1]])
        if (line[0][0] == "@"):
            interaction_list.append([line[0][1:], line[1]])

    if ((len(interaction_list) == 0) or (len(component_list) == 0)):
        Error("ERROR: No Interactions or Components Exist")
    
    return component_list, interaction_list


# inputs: the interaction list, and component list
# outputs: adds a number of auxilary components instead of every interaction
def Add_Auxilary_Components(interaction_list, component_list):
    global_auxilary_count = 0
    v_l = []
    new_interaction_list = []
    
    for IS in interaction_list:
        v_l = Get_Variable_List(IS, "interaction")

        for _ in range(TIME_DELAY - 1):
            component_list.append([f"A{global_auxilary_count}|1|17|{v_l[0]}", -1])
            global_auxilary_count += 1

        new_interaction_list.append([f"{v_l[1]}|A{global_auxilary_count - TIME_DELAY + 1}|pos|def|{v_l[0]}", -1])

        for i in range(TIME_DELAY - 2):
            new_interaction_list.append([f"A{global_auxilary_count - TIME_DELAY + 1 + i}|A{global_auxilary_count - TIME_DELAY + 2 + i}|pos|def|{v_l[0]}", -1])

        new_interaction_list.append([f"A{global_auxilary_count - 1}|{v_l[2]}|{v_l[3]}|{v_l[4]}|{v_l[0]}", -1])

    return component_list, new_interaction_list


# inputs: a component list
# outputs: the component list in REIN format
def Translate_Component_Lines(component_list):
    REIN_component_list = []
    component_name_list = []

    for CS in component_list:
        v_l = Get_Variable_List(CS, "component")
        REIN_component_list.append(Generate_Component_Line(v_l[0], v_l[1], v_l[2], v_l[3], CS[1]))
        component_name_list.append(v_l[1])

    return REIN_component_list, component_name_list


# inputs: variables from a component variable list
# outputs: the REIN component statement corresponding to the variables
def Generate_Component_Line(occurance_string, name, x, y, line_index):
    if (not((0 <= int(x)) and (int(x) <= 17) and (0 <= int(y)) and (int(y) <= 17) and (int(x) <= int(y)))):
        Error(f"ERROR: Impossible Regulation Condition Range in Line {line_index}")
    
    return f"{name}[-+]({x}..{y});{occurance_string}"


# inputs: an interaction list
# outputs: the interaction list in REIN format
def Translate_Interaction_Lines(interaction_list, component_name_list):
    REIN_interaction_list = []

    for IS in interaction_list:
        name1_non_existent = True
        name2_non_existent = True

        v_l = Get_Variable_List(IS, "interaction")

        for name in component_name_list:
            if (v_l[1] == name):
                name1_non_existent = False
            if (v_l[2] == name):
                name2_non_existent = False

        if (name1_non_existent):
            Error(f"ERROR: First Component in Interaction Does not Exist in the Current Context in Line {IS[1]}")
        if (name2_non_existent):
            Error(f"ERROR: Second Component in Interaction Does not Exist in the Current Context in Line {IS[1]}")
                
        REIN_interaction_list.append(Generate_Interaction_Line(v_l[0], v_l[1], v_l[2], v_l[3], v_l[4], IS[1]))
    
    return REIN_interaction_list


# inputs: variables from a interaction variable list
# outputs: the REIN interaction statement corresponding to the variables
def Generate_Interaction_Line(occurance_string, c1, c2, pos_or_neg, def_or_op, line_index):

    if (pos_or_neg == "pos"):
        pos_or_neg = "positive"
    elif (pos_or_neg == "neg"):
        pos_or_neg = "negative"
    else:
        Error(f"ERROR: The Sign (pos or neg) of the Interaction is not Present in Line {line_index}")

    if (def_or_op == "def"):
        return f"{c1} {c2} {pos_or_neg};{occurance_string}"
    elif (def_or_op == "op"):
        return f"{c1} {c2} {pos_or_neg} optional;{occurance_string}"
    else:
        Error(f"ERROR: The Type (def or op) of the Interaction is not Present in Line {line_index}")


# inputs: a statement (interaction or component)
# outputs: the variables of the statement (occurance string always first)
def Get_Variable_List(s, type):
    if (not(s[0][O:].isnumeric())):
        Error(f"ERROR: Occurance String ({-1 * O} Zeros and Ones) is Too Short in Line {s[1]}")  
    
    variable_list = [s[0][O:]]
    s[0] = s[0][:O - 1]
    ver_index = 0
    
    while True:

        ver_index =  s[0].find("|")

        if (ver_index == -1):
            variable_list.append(s[0])
            break

        variable_list.append(s[0][:ver_index])
        s[0] = s[0][ver_index + 1:]

    if ((type == "component") and (len(variable_list) != 4)):
        Error(f"ERROR: Component Line {s[1]} isn't Written Correctly (You May Have Made the Occurance String Too Long or Short)")
    if ((type == "interaction") and (len(variable_list) != 5)):
        Error(f"ERROR: Interaction Line {s[1]} isn't Written Correctly (You May Have Made the Occurance String Too Long or Short)")

    return variable_list


# inputs: the starting hour, the ending hour, the REIN component and interaction list
# outputs: creates a REIN file for each hour between the starting and ending hours
def Create_REIN_Programs(HOUR1, HOUR2, REIN_components, REIN_interactions, KIND, OUTPUT_NAME):
    if (KIND == "hours"):
        for i in range (HOUR2 - HOUR1 + 1):
            file_name = f"{OUTPUT_NAME}_hour_{i + HOUR1}.txt"
            file_path = STORAGE_PATH.joinpath(file_name)
            Write_Lines_Into_Programs(file_path, REIN_components, REIN_interactions, i)
            print("MODEL(S) GENERATED")
            exit()
        
    if (KIND == "definite"):
        file_name = f"{OUTPUT_NAME}_definite.txt"
        file_path = STORAGE_PATH.joinpath(file_name)
        Write_Lines_Into_Programs(file_path, REIN_components, REIN_interactions, 0)
        print("MODEL(S) GENERATED")
        exit()

    if (KIND == "optional"):
        file_name = f"{OUTPUT_NAME}_optional.txt"
        file_path = STORAGE_PATH.joinpath(file_name)
        Write_Lines_Into_Programs(file_path, REIN_components, REIN_interactions, 0)
        print("MODEL(S) GENERATED")
        exit()


# inputs: a file path, a component list, an interactions list, and a hour
# outputs:  creates a REIN file for the specific hour
def Write_Lines_Into_Programs(file_path, REIN_components, REIN_interactions, i):
    with open(file_path, 'w') as model:
        for RCS in REIN_components:
            if RCS[O:][i] == "1":
                model.write(f"{RCS[:O]}\n")
                model.write("\n")

        for j in range(2):
            model.write("\n")

        for RIS in REIN_interactions:
            if RIS[O:][i] == "1":
                model.write(f"{RIS[:O]}\n")
                model.write("\n")


# inputs: error message
# outputs: prints the error message and closes
def Error(error_name):
    print(error_name)
    input()
    exit()


line_list = Get_Lines(f"{INPUT_NAME}.txt")

component_list, interaction_list = Filter_Lines(line_list)

if (TIME_DELAY != 0):
    component_list, interaction_list = Add_Auxilary_Components(interaction_list, component_list)

component_list, component_name_list = Translate_Component_Lines(component_list)

interaction_list =  Translate_Interaction_Lines(interaction_list, component_name_list)

Create_REIN_Programs(HOUR1, HOUR2, component_list, interaction_list, KIND, OUTPUT_NAME)