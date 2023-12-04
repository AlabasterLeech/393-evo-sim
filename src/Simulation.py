import random

from src.Organism import Organism
from src.Environment import Environment

class Simulation:
    def __init__(self, width, height, population, survival_function, age_max):
        #Initialize new simulation
        self.env = Environment(width, height)
        self.age = 0
        self.gen = 0
        self.population = population
        self.survival_function = survival_function
        self.age_max = age_max
        self.genome_length = 512
        self.mutation = 0.1
        #Create first generation with random genomes
        for _ in range(self.population):
            patient = Organism({
                "x": random.randint(0, self.env.width - 1),
                "y": random.randint(0, self.env.height - 1),
                "dir": random.randint(0, 3)
            })
            genome = []
            for __ in range(self.genome_length):
                genome.append(bytes([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))
            patient.set_genome(genome)
            patient.build_network()
            while not self.env.space_open(patient.x, patient.y):
                patient.x, patient.y = random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1)
            self.env.organisms.append(patient)
    
    def load_json(self, filename):
        #Load state from JSON
        None

    def save_json(self, filename):
        #Save state to JSON
        None
    
    def step(self):
        #Calculate all organism behaviors and act on them
        state = self.env.get_state()
        for org in state["organisms"]:
            org.think(self.env)
        for org in state["organisms"]:
            org.act(self.env)
        self.age += 1
        if self.age >= self.age_max:
            self.step_gen()
    
    def step_gen(self):
        #Create new generation of organisms
        parents = []
        for organism in self.env.organisms:
            if self.survival_function(organism, self.env):
                parents.append(organism)
        self.env.organisms = []
        for _ in range(self.population):
            offspring = self.env.breed(random.choice(parents, random.choice(parents)))
            offspring.mutate(self.mutation)
            offspring.build_network()
            offspring.x, offspring.y = random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1)
            while not self.env.organisms.space_open(offspring.x, offspring.y):
                offspring.x, offspring.y = random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1)
            self.env.organisms.append(offspring)
        #Set counters
        self.age = 0
        self.gen += 1
