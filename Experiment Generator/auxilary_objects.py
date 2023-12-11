import functions as f


class Range:


    def __init__(self, start, end, val, line_index):
        self.start = start
        self.end = end
        self.range = range(start, end + 1)
        self.val = val
        self.line_index = line_index


    def disjoint(self, other):
        for t in self.range:
            if (t in other.range):
                return False
            
        return True




class Constraint:


    def __init__(self, name):
        self.name = name
        self.dict = {}


    def __str__(self):
        string = ""

        for component in self.dict:
            string += f"   {component} = {self.dict[component]} and\n"
        string = string[:-5] + "\n\n"

        return f"${self.name} :=\n" + "{\n\n" + string + "};"
    

class Perturbation(Constraint):


    def __str__(self):
        string = ""

        for component in self.dict:
            if (self.dict[component] == 1):
                string += f"   FE({component}) = 1 and\n"
            else:
                string += f"   KO({component}) = 1 and\n"
        string = string[:-5] + "\n\n"

        return f"${self.name} :=\n" + "{\n\n" + string + "};"


class SPT:


    def __init__(self, component, experiments, val):
        self.component = component
        experiments.sort()
        self.experiments = experiments
        self.val = val


    def __eq__(self, other):
        return (self.component == other.component) and (self.experiments == other.experiments) and (self.val == other.val)
    

    def __str__(self):
        return f"{self.component}, {self.experiments}, {self.val}"
    

class Constraint_Appearences:


    def __init__ (self, name, appearences, constraint_n):
        self.name = name
        self.appearences = appearences
        self.constraint_n = constraint_n


class Experiment_Expression:


    def __init__ (self, experiment, constraints, permutations):
        self.experiment = experiment
        self.constraints = constraints
        self.permutations = permutations


    def __str__ (self):
        string = ""
        
        for permutation in self.permutations:
            temp_string = f"((#Experiment_{self.experiment}[{permutation[0]}] |= Restriction_{self.experiment}_{self.constraints[0]}) and\n"

            for i in range(1, len(permutation)):
                temp_string += f"(Experiment_{self.experiment}[{permutation[i]}] |= Restriction_{self.experiment}_{self.constraints[i]}) and\n"

            temp_string = temp_string[:-5] + ") or\n\n"

            string += temp_string

        return string[:-5] + ";\n\n"
                