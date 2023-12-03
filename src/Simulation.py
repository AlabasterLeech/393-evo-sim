import time

from Environment import Environment

class Simulation:
    def __init__(self, width, height, *params):
        self.create(width, height)
    
    def create(self, width, height):
        #Initialize new simulation
        self.env = Environment(width, height)
        self.age = 0
        self.gen = 0
    
    def load_json(self, filename):
        #Load state from JSON
        None

    def save_json(self, filename):
        #Save state to JSON
        None
        
    def auto_save(self, filename):
        #Save state to JSON with automatically generated file path
        saveName = "AUTO-SAVE-" + time.asctime().replace(':', '-').replace(' ', '-') + ".json"
        savePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", saveName))
        self.save_json(savePath)
        
    def step(self):
        #Calculate all organism behaviors and act on them
        state = self.env.get_state()
        for org in state["organisms"]:
            org.think(self.env)
        for org in state["organisms"]:
            org.act(self.env)
        self.age += 1
    
    def step_gen(self):
        #Create new generation of organisms
        self.age = 0
        self.gen += 1
