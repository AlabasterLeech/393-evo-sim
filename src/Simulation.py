import json
import random
import time
import os.path

from src.Organism import Organism
from src.Environment import Environment


class Simulation:
    # Survival functions
    SURVIVAL = {
        "None": lambda organism, env: True,
        "North quarter": lambda organism, env: organism.y <= env.height // 4,
        "South quarter": lambda organism, env: organism.y >= env.height * 3 // 4,
        "East quarter": lambda organism, env: organism.x >= env.width * 3 // 4,
        "West quarter": lambda organism, env: organism.x <= env.width // 4
    }

    def __init__(self, width, height, food_density, population, survival_function, age_max):
        # Initialize new simulation
        self.env = Environment(width, height)
        self.age = 0
        self.gen = 0
        self.population = population
        self.food_density = food_density
        self.age_max = age_max
        self.genome_length = 512
        self.mutation = 0.1
        self.set_survival_function(survival_function)
        # Create first generation with random genomes
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
        # Load state from JSON
        save_file = open(filename, "r")
        state = json.loads(save_file.read())
        # Validate loaded state
        for arg in ["width", "height", "env", "age", "gen", "population", "age_max", "genome_length", "mutation_rate", "survival_function"]:
            if arg not in state:
                save_file.close()
                return False
        if "organisms" not in state["env"] or "objects" not in state["env"]:
            save_file.close()
            return False
        # Recreate saved state
        self.env = Environment(state["width"], state["height"])
        self.env.set_state(state["env"])
        self.age = state["age"]
        self.gen = state["gen"]
        self.population = state["population"]
        self.age_max = state["age_max"]
        self.genome_length = state["genome_length"]
        self.mutation = state["mutation_rate"]
        self.set_survival_function(state["survival_function"])
        save_file.close()
        return True

    def save_json(self, filename):
        # Save state to JSON
        state = {
            "width": self.env.width,
            "height": self.env.height,
            "env": self.env.get_state(),
            "age": self.age,
            "gen": self.gen,
            "population": self.population,
            "age_max": self.age_max,
            "genome_length": self.genome_length,
            "mutation_rate": self.mutation,
            "survival_function": self.survival_function_name
        }
        save_file = open(filename, "w")
        save_file.write(json.dumps(state))
        save_file.close()
        return True

    def auto_save(self, filename):
        # Save state to JSON with automatically generated file path
        saveName = "AUTO-SAVE-" + time.asctime().replace(':', '-').replace(' ', '-') + ".json"
        savePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", saveName))
        self.save_json(savePath)

    def set_survival_function(self, survival_function):
        self.survival_function_name = survival_function
        self.survival_function = Simulation.SURVIVAL[survival_function if survival_function in Simulation.SURVIVAL else "None"]

    def step(self):
        # Calculate all organism behaviors and act on them
        organisms = self.env.get_organisms()
        for org in organisms:
            org.think(self.env)
        for org in organisms:
            org.act(self.env)
        self.age += 1
        if self.age >= self.age_max:
            self.step_gen()

    def step_gen(self):
        # Create new generation of organisms
        parents = []
        for organism in self.env.organisms:
            if self.survival_function(organism, self.env):
                parents.append(organism)
        self.env.organisms = []
        for _ in range(self.population):
            offspring = self.env.breed(random.choice(parents), random.choice(parents))
            offspring.mutate(self.mutation)
            offspring.build_network()
            offspring.x, offspring.y = random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1)
            while not self.env.space_open(offspring.x, offspring.y):
                offspring.x, offspring.y = random.randint(0, self.env.width - 1), random.randint(0, self.env.height - 1)
            self.env.organisms.append(offspring)
        # Set counters
        self.age = 0
        self.gen += 1
