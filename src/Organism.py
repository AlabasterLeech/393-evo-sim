import math
import random

class Organism:
    def __init__(self, state):
        #Initialize minimally functional default state
        self.x, self.y = 0, 0
        self.genome = []

        #Copy initializer state into members
        self.set_state(state)
    
    def get_state(self):
        #Return functional current state
        return {
            "x": self.x,
            "y": self.y,
            "genome": self.genome
        }

    def set_state(self, state):
        #Copy initializer state into members
        for attr in state:
            setattr(self, attr, state[attr])

    def think(self):
        #Generate list of desired actions
        actions = {}
        return actions
    
    def act(self, actions):
        #Carry out actions
        None

    def consume(self, object):
        #...
        None

    def mutate(self, chance):
        #...
        None
    
    def build_network(self):
        #Generate neural network from stored genome
        None

    def get_genome(self):
        return self.genome
    
    def set_genome(self, new_genome):
        self.genome = new_genome
    
    def get_location(self):
        return (self.x, self.y)

    class Neuron:
        def __init__(self):
            self.output = 0
            self.bias = 0
            self.threshold = 0.8
            self.inputs = []
            self.outputs = []

        def get_output(self):
            return self.output
        
        def activation(self, signal):
            sigmoid = 1 / (1 + math.exp(-2 * signal))
            return math.tanh(2 * sigmoid - 1)

        def calc_output(self):
            signal = sum([neuron[0].get_output() * neuron[1] for neuron in self.inputs])
            signal += self.bias
            self.output = self.activation(signal)