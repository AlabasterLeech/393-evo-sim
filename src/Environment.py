#!/usr/bin/env python
# coding: utf-8

# In[ ]:

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
        new_organism = Organism(state)
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
        crossover_point = random.randint(0, len(genome1) - 1)
        new_genome = genome1[:crossover_point] + genome2[crossover_point:]
        return new_genome

