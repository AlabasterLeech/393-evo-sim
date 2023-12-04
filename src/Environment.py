import random
from src.Organism import Organism
from src.Object import Object


class Environment:
    def __init__(self, width, height):
        # Initializes the environment with default parameters
        self.width = width
        self.height = height
        self.organisms = []  # A list to store all organisms in the environment
        self.objects = []  # A list to store non-living entities like food and obstacles
        self.survival_function = None  # The function to determine organism survival probability
        self.check_function = [
            self.check_move_forward,
            self.check_move_backward,
            self.check_turn_left,
            self.check_turn_right,
            self.check_consume,
            self.check_kill
        ]

    def get_state(self):
        # Return the current state of the environment
        state = {}
        state["organisms"] = [organism.get_state() for organism in self.organisms]
        state["objects"] = [object.get_state() for object in self.objects]
        return state

    def set_state(self, state):
        # Clears the current state and regenerate the environment with provided data
        self.organisms = []
        for organism_state in state["organisms"]:
            organism = Organism(organism_state)
            self.organisms.append(organism)

        self.objects = []
        for object_state in state["objects"]:
            object = Object(object_state["x"],
                            object_state["y"],
                            object_state["object_type"],
                            object_state["density"])
            self.objects.append(object)

    def breed(self, organism1, organism2):
        # Produces a new organism using a genome derived from the genomes of two specified organisms
        new_genome = self.crossover(organism1.get_genome(), organism2.get_genome())
        new_organism = Organism({"x": 0,
                                 "y": 0})
        new_organism.set_genome(new_genome)
        return new_organism

    def space_open(self, x, y):
        # Checks if the specified coordinates are within the bounds of the environment and are not occupied by any organisms or objects
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            return False

        for organism in self.organisms:
            if organism.get_location() == (x, y):
                return False

        for obj in self.objects:
            if obj.get_location() == (x, y):
                return False

        return True

    def set_survival_function(self, survival_function):
        # Replaces the current survival probability function with the provided function
        self.survival_function = survival_function

    def crossover(self, genome1, genome2):
        # Creates a new genome by combining the two parents genomes at the crossover point
        new_genome = []
        for i in range(min(len(genome1), len(genome2))):
            # Performs crossover for each gene pair
            selected_gene = genome1[i] if random.choice([True, False]) else genome2[i]
            new_genome.append(selected_gene)
        return new_genome

    def check(self, actions, organism):
        # Checks the validity of the desired actions 
        valid_actions = []
        for action in actions:
            if self.check_function[action](organism):
                valid_actions.append(action)
        return valid_actions

    def check_move_forward(self, organism):
        x, y = organism.get_location()
        if organism.dir == Organism._NORTH and self.space_open(x, y - 1):
            return True
        elif organism.dir == Organism._EAST and self.space_open(x + 1, y):
            return True
        elif organism.dir == Organism._SOUTH and self.space_open(x, y + 1):
            return True
        elif organism.dir == Organism._WEST and self.space_open(x - 1, y):
            return True
        return False

    def check_move_backward(self, organism):
        x, y = organism.get_location()
        if organism.dir == Organism._NORTH and self.space_open(x, y + 1):
            return True
        elif organism.dir == Organism._EAST and self.space_open(x - 1, y):
            return True
        elif organism.dir == Organism._SOUTH and self.space_open(x, y - 1):
            return True
        elif organism.dir == Organism._WEST and self.space_open(x + 1, y):
            return True
        return False

    def check_turn_left(self, organism):
        return True  # Turning left is always allowed

    def check_turn_right(self, organism):
        return True  # Turning right is always allowed

    def check_consume(self, organism):
        x, y = organism.get_location()
        if organism.dir == Organism._NORTH and self.object_in_front(x, y - 1, 'food'):
            return True
        elif organism.dir == Organism._EAST and self.object_in_front(x + 1, y, 'food'):
            return True
        elif organism.dir == Organism._SOUTH and self.object_in_front(x, y + 1, 'food'):
            return True
        elif organism.dir == Organism._WEST and self.object_in_front(x - 1, y, 'food'):
            return True
        return False

    def check_kill(self, organism):
        x, y = organism.get_location()
        if organism.dir == Organism._NORTH and self.organism_in_front(x, y - 1):
            return True
        elif organism.dir == Organism._EAST and self.organism_in_front(x + 1, y):
            return True
        elif organism.dir == Organism._SOUTH and self.organism_in_front(x, y + 1):
            return True
        elif organism.dir == Organism._WEST and self.organism_in_front(x - 1, y):
            return True
        return False

    def object_in_front(self, x, y, obj_type):
        for obj in self.objects:
            if obj.get_location() == (x, y) and obj.object_type == obj_type:
                return True
        return False

    def organism_in_front(self, x, y):
        for org in self.organisms:
            if org.get_location() == (x, y):
                return True
        return False

