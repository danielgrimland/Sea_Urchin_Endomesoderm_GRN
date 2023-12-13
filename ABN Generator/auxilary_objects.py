import functions as f


class Component:


    def __init__(self, name, start_range, end_range):
        self.name = name
        self.start_range = start_range
        self.end_range = end_range

    
    def __str__(self):
        return f"{self.name}[-+]({self.start_range}..{self.end_range});"


class Interaction:


    def __init__(self, initiator, target, is_pos, is_def, delays):
        self.initiator = initiator
        self.target = target
        self.is_pos = is_pos
        self.is_def = is_def
        self.delays = delays

    
    def __str__(self):
        if (self.is_pos == "pos"):
            if(self.is_def == "def"):
                return f"{self.initiator} {self.target} positive;"
            else:
                return f"{self.initiator} {self.target} positive optional;"
        else:
            if(self.is_def == "def"):
                return f"{self.initiator} {self.target} negative;"
            else:
                return f"{self.initiator} {self.target} negative optional;"