import py4cytoscape as p4c
import pandas as pd
from pathlib import Path
import re


DATA_FILE = "Kidney_abn"
DATA_PATH = Path(rf"C:\Users\Lithi\OneDrive\שולחן העבודה\Alpha Research")
GROUPS = []


# inputs: error message
# outputs: prints the error message and closes
def error(error_name):
    print(error_name)
    input()
    exit()


# Inputs: the name of the data file, and the path to its folder.
# Outputs: a list of the lines of the files without the deafult \n at the start.
def get_lines():
    path = DATA_PATH.joinpath(f"{DATA_FILE}.rein")
    with open(path) as data:
        lines = data.readlines()

    new_lines = []

    for i in range(len(lines)):
        new_line = (lines[i].replace("\n", ""))

        if (len(new_line) != 0):
            new_lines.append([new_line, i + 1])

    return new_lines


# Inputs: the name of the data file, and the path to its folder.
# Outputs: a list of the lines of the files without the deafult \n at the start.
def get_nodes_and_edges(lines):
    node_names = []
    node_groups = []
    
    sources = []
    targets = []
    pos_or_neg = []
    def_or_op = []
    
    for line in lines:
        is_component = re.search("^[^\/](.*)\(([0-9]|1[0-7])..([0-9]|1[0-7])\);$", line[0])
        is_interaction = re.search("^(.*) (.*) ((positive)|(negative))( optional)?;$", line[0])
        
        if (is_component):   
            line[0] = line[0].replace(" ", "")
            with_specification = re.search("(\[\+-\])|(\[-\+\])|(\[-\])|(\[\+\])|(\[!\])", line[0])
            
            if (with_specification):
                last = line[0].rfind("[")
            
            else:
                last = line[0].rfind("(")

            node_names.append(line[0][:last])
            
            if (len(GROUPS) != 0):
                start_group = line[0].rfind("_") + 1
                
                if (start_group == 0):
                    error(f"Componenet in line << {line[1]} >> doesn't have a specified group, despite requesting grouping components.")
                
                group = line[0][:last][start_group:]
                
                if (group not in GROUPS):
                    error(f"Componenet in line << {line[1]} >> is specified a group not present in user specification.")
                    
                node_groups.append(line[0][:last][start_group:])
        
        elif (is_interaction):
            sections = re.split(" ", line[0])
            sources.append(sections[0])
            targets.append(sections[1])
            
            if (len(sections) == 3):
                if (sections[2][:-1] == "positive"):
                    pos_or_neg.append("activates")
                else:
                    pos_or_neg.append("inhibits")     
                    
                def_or_op.append("definite")
            
            else:
                if (sections[2] == "positive"):
                    pos_or_neg.append("activates")
                else:
                    pos_or_neg.append("inhibits")     
                    
                def_or_op.append("optional")
                
    nodes = {"id" : node_names}
    
    if (len(GROUPS) != 0):
        nodes = {"id" : node_names, "group" : node_groups}
        
    edges = {"source": sources, "target": targets, "interaction": pos_or_neg, "linetype" : def_or_op}
    
    return nodes, edges


lines = get_lines()

nodes, edges = get_nodes_and_edges(lines)

nodes = pd.DataFrame(nodes)

edges = pd.DataFrame(edges)

print(nodes)
print()
print(edges)

p4c.create_network_from_data_frames(nodes, edges, DATA_FILE, DATA_FILE)

print("Cytoscape Model Generated")
