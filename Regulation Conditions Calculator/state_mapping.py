import functions as f

class State_Mapping:


    # Inputs: a list of states of sets of activators and repressors, and a list of values a gene may be in.
    # Outputs: a RC mapping between sets of activators and repressors of a gene (whose states are tuples (x, y) respectively)
    # to its new state.
    def __init__(self, domain_values, codomain):
        if (not(f.list_numeric(domain_values)) or not(f.list_numeric(codomain))):
            f.error("Codomain or Domain Values are not numeric in their entirety")
        values = list(f.remove_duplicates(domain_values))
        values.sort()
        self.domain_values = values
        self.domain = f.prod(f.remove_duplicates(domain_values))
        self.codomain = list(f.remove_duplicates(codomain))
        self.dict = {}


    # Inputs: a GRC object.
    # Outputs: a string containing the data of all fields of the object.
    def __str__(self):
        return f"Domain = {self.domain}\nCodomain = {self.codomain}\nMapping = {self.dict}"


    # Inputs: an element d in the domain of an RC object, and an element c in the codomain of it.
    # Outputs: adds the pair {d : c} to the dictionary of the object, or changes the element d correspodns to.
    def add_or_modify_pair(self, element, image):
        if ((element not in self.domain) or (image not in self.codomain)):
            f.Error("Attempted to add a pair to a map whose element or image don't exist in the domain or codomain respectively")
        else:
            self.dict.update({element : image})


    # Inputs: a GRC object.
    # Outputs: whether the object is a monotonic function or not.
    def monotonic(self):
        if ((self.dict.get((max(self.domain_values), min(self.domain_values[1:]))) != max(self.codomain)) or
            (self.dict.get((min(self.domain_values[1:]), max(self.domain_values))) != min(self.codomain))):
            return False

        if ((self.dict.get((min(self.domain_values), min(self.domain_values[1:]))) != max(self.codomain)) or 
            (self.dict.get((min(self.domain_values), max(self.domain_values))) != min(self.codomain)) or 
            (self.dict.get((min(self.domain_values[1:]), min(self.domain_values))) != min(self.codomain)) or 
            (self.dict.get((max(self.domain_values), min(self.domain_values))) != max(self.codomain))):
            return False
        
        new_values = self.domain_values
        new_values.remove(min(self.domain_values[1:]))
        new_values.remove(max(self.domain_values))
        
        for v in new_values:
            if (v == min(self.domain_values)):
                if (self.dict.get((min(self.domain_values), min(self.domain_values))) != self.dict.get((min(self.domain_values[1:]), min(self.domain_values[1:])))):
                    return False
            else:
                if ((self.dict.get((v, min(self.domain_values))) != self.dict.get((v, min(self.domain_values[1:])))) or
                    (self.dict.get((min(self.domain_values), v))) != self.dict.get((min(self.domain_values[1:]), v))):
                    return False
        
        for v1 in self.domain_values[1:]:
            activators_pre = self.dict.get((v1, min(self.domain_values[1:])))
            inhibitors_pre = self.dict.get((min(self.domain_values[1:]), v1))
            
            for v2 in self.domain_values[1:]:
                if ((self.dict.get((v1, v2)) > activators_pre)):
                    return False
                
                if ((self.dict.get((v2, v1)) < inhibitors_pre)):
                    return False

                activators_pre = self.dict.get((v1, v2))
                inhibitors_pre = self.dict.get((v2, v1))

        return True