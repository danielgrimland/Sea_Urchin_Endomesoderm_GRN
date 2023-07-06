"""
________________________________________________________________________________________________________________________________________
CYTOSCAPE MODEL GENERATOR

This program allows the generation of a Cytoscape model from untranslated data.
________________________________________________________________________________________________________________________________________
INPUTS

DOMAINS: The list of all legal domains of the components of the model. 
DEFAULTS: The list of all default variable settings for the components of the model

TYPE: The specific file of the input and output data (if the ABN is of a Domain-Divided system, Full-Genome, etc.).
INPUT NAME: The name of the inputed file.
DATA PATH: The name of the path with the untranslated input data.
________________________________________________________________________________________________________________________________________
TODO
Work on visual style generator.
________________________________________________________________________________________________________________________________________
"""


import py4cytoscape as p4c
import pandas as pd
from pathlib import Path


DOMAINS = ["aboralNSM_diff", "oralNSM_diff", "smallMIC", "veg_endo_1", "veg_ecto_1", "veg_endo_2", "MAT", "PMC", "Skel","aboralNSM", "oralNSM"]
DEFAULTS = {'NODE_SHAPE': "elipse", 'NODE_SIZE': 30, 'EDGE_TRANSPARENCY': 120, 'NODE_LABEL_POSITION': "W,E,c,0.00,0.00"}
TYPE = "Domain-Divided"
INPUT_NAME = "Domain-Divided_Input_ABN_all_optional"
DATA_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research\Programs\Sea Urchin Endomesoderm Models and Tools\Untranslated Input Data\{TYPE}")


#Inputs: Left and right lists
#Outpus: sorted merge of lists
def Merge(left, right):
    if (len(left) == 0):
        return right
    
    if (len(right) == 0):
        return left
    
    result = []

    indexLeft = indexRight = 0

    while (len(result) < len(left) + len(right)):
        if (len(left[indexLeft]) <= len(right[indexRight])):
            result.append(left[indexLeft])
            indexLeft += 1
        else:
            result.append(right[indexRight])
            indexRight += 1
    
        if (indexRight == len(right)):
            result += left[indexLeft:]
            break

        if (indexLeft == len(left)):
            result += right[indexRight:]
            break
    
    return result


# inputs: domain list
# outpus: sorted domain list with merge sort
def Sort_Domains(DOMAINS):
    if (len(DOMAINS) < 2):
        return DOMAINS
    
    midpoint = len(DOMAINS) // 2

    return Merge(left = Sort_Domains(DOMAINS[:midpoint]), right = Sort_Domains(DOMAINS[midpoint:]))


#TODO: Finish generate visual style function
def Generate_And_Set_Visual_Style(style_name):
    node_labels = p4c.map_visual_property("node label", "id", "p", style_name)

    p4c.set_edge_source_arrow_shape_mapping(**p4c.gen_edge_arrow_map("linetype", style_name = style_name))
    p4c.set_node_color_mapping(**p4c.gen_node_color_map("group", mapping_type = "d", style_name = style_name))
    p4c.set_edge_target_arrow_shape_mapping(**p4c.gen_edge_arrow_map("interaction", style_name = style_name))
    p4c.create_visual_style(style_name, DEFAULTS, [node_labels])

    p4c.set_visual_style(style_name)


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


# inputs: a component list
# outputs: a list of all nodes and their details in Cytoscape format
def Get_All_Nodes(component_list):
    node_name_list = []
    domain_list = []

    for CS in component_list:
        component = Slice_String("|", CS[0])
        node_name_list.append(component[0])

        domain_list.append(Find_Group(CS[0]))

    node_dic = {"id" : node_name_list, "group" : domain_list}
        
    return node_dic


# inputs: the name of a component
# outputs: the domain the component is in according to the domain list
def Find_Group(component_name):
    for p in DOMAINS:
        if (p in component_name):
            return p

    return None


# inputs: an interaction list
# outputs: a list of all interactions and their details in Cytoscape format
def Get_All_Interactions(interaction_list):
    source_list = []
    target_list = []
    kind_list = []
    line_type_list = []

    for IS in interaction_list:
        interaction = Slice_String("|", IS[0])
        source_list.append(interaction[0])
        target_list.append(interaction[1])
        
        kind = ""
        if (interaction[2] == "pos"):
            kind += "activates"
        elif (interaction[2] == "neg"):
            kind += "inhibits"
        else:
            Error(f"ERROR: No interaction type (pos or neg) in line {IS[1]}")
        
        type = ""
        if (interaction[3] == "op"):
            type += "optional"
        elif (interaction[3] == "def"):
            type += "definite"
        else:
            Error(f"ERROR: No interaction type (op or def) in line {IS[1]}")
        kind_list.append(kind)
        line_type_list.append(type)
    
    
    edge_dic = {"source": source_list, "target": target_list, "interaction": kind_list, "linetype" : line_type_list}
        
    return edge_dic


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


# inputs: error message
# outputs: prints the error message and closes
def Error(error_name):
    print(error_name)
    input()
    exit()

DOMAINS = Sort_Domains(DOMAINS)
DOMAINS.reverse()

line_list = Get_Lines(f"{INPUT_NAME}.txt")

component_list, interaction_list = Filter_Lines(line_list)

nodes = pd.DataFrame(Get_All_Nodes(component_list))

edges = pd.DataFrame(Get_All_Interactions(interaction_list))

p4c.create_network_from_data_frames(nodes, edges, title = "current", collection = "DataFrame Example")

print("CYTOSCAPE MODEL GENERATED")