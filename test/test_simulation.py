import json
import unittest
import os
import time
from Simulation import Simulation
from Organism import Organism


class SimulationTest(unittest.TestCase):
    def setUp(self):
        self.width = 10
        self.height = 10
        self.pop = 3
        self.food = 0.75
        self.survival = 10
        self.age_max = 5
        self.sim = Simulation(self.width, self.height, self.food, self.pop, self.survival, self.age_max)
        self.survival_function = self.sim.survival_function
        self.survival_function_name = self.sim.survival_function_name

    def test_init(self):
        self.assertEqual(self.pop, len(self.sim.env.organisms))
        new_sim = Simulation(5, 5, self.food, 25, self.survival, self.age_max)
        new_sim.step_gen()

    def test_load_json(self):
        filename = "test_load_json.json"
        filepath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", filename))
        print(filepath)
        flag = self.sim.load_json(filepath)
        self.assertEqual(True, flag, 'File was not loaded!')
        organisms = self.sim.env.get_organisms()
        actual_location = organisms[0].get_location()
        self.assertEqual((4, 1), actual_location, 'Not the same location!')

    def test_load_bad_json(self):
        empty_orgs = os.path.normpath(
            os.path.join(os.path.abspath(__file__), "..", "..", "assets", 'test_load_empty_orgs.json'))
        empty_objs = os.path.normpath(
            os.path.join(os.path.abspath(__file__), "..", "..", "assets", 'test_load_empty_objs.json'))
        empty_args = os.path.normpath(
            os.path.join(os.path.abspath(__file__), "..", "..", "assets", 'test_load_empty_args.json'))
        self.assertEqual(False, self.sim.load_json(empty_orgs))
        self.assertEqual(False, self.sim.load_json(empty_objs))
        self.assertEqual(False, self.sim.load_json(empty_args))

    def test_save_json(self):
        filename = "test_save_json.json"
        filepath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", filename))
        exp_orgs = 3
        exp_max_age = 5
        self.sim.save_json(filepath)
        saved_file = open(filepath, "r")
        saved_state = json.loads(saved_file.read())
        saved_orgs = len(saved_state["env"]["organisms"])
        saved_max_age = saved_state["age_max"]
        msg = 'State was not saved properly!'
        self.assertEqual(exp_orgs, saved_orgs, msg)
        self.assertEqual(exp_max_age, saved_max_age, msg)
        saved_file.close()

    def test_auto_save(self):
        # DOES NOT WORK
        self.sim.auto_save('filename')
        current_time = time.strftime('%a-%b-%e-%H-%M-%S-%Y', time.localtime()).replace(' ', '-')
        exp_file_name = f"AUTO-SAVE-{current_time}.json"
        exp_file_path = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", exp_file_name))
        file_created = os.path.isfile(exp_file_path)
        self.assertTrue(file_created, "JSON file was not created!")

    def test_set_survival_function(self):
        # Check none survival function
        self.assertEqual(self.survival, self.survival_function_name)
        self.assertEqual(Simulation.SURVIVAL["None"], self.survival_function)

        # Check setting actual survival function
        sim_test = Simulation(self.width, self.height, self.food, self.pop, "North quarter", self.age_max)
        self.assertEqual(Simulation.SURVIVAL["North quarter"], sim_test.survival_function)

    def test_fill_food(self):
        self.sim.food_density = 100  # 100% chance for food
        self.sim.env.organisms = []
        self.sim.fill_food()
        msg = 'Different number of food objects in Env!'
        self.assertEqual(100, len(self.sim.env.get_objects()), msg)

    def test_step(self):
        self.sim.step()
        msg = 'Age is not the same as expected age!'
        self.assertEqual(1, self.sim.age, msg)
        self.sim.step()
        self.sim.step()
        self.sim.step()
        self.sim.step()
        self.assertEqual(0, self.sim.age, msg)
        self.assertEqual(1, self.sim.gen, msg)

    def test_step_gen(self):
        self.sim.set_survival_function("North quarter")
        org = Organism({"x": 0, "y": 0})
        self.sim.env.organisms.append(org)
        self.sim.step_gen()
        age_msg = 'Age is not the same as expected age!'
        gen_msg = 'Gen is not the same as expected gen!'
        org_msg = 'Org was not removed!'
        self.assertEqual(0, self.sim.age, age_msg)
        self.assertEqual(1, self.sim.gen, gen_msg)
        self.assertEqual(True, self.sim.env.space_open(0, 0), org_msg)

    def test_step_gen_no_survivors(self):
        self.sim.env.organisms = []
        self.sim.step_gen()
        msg = 'Different numbers of organisms!'
        self.assertEqual(self.pop, len(self.sim.env.get_organisms()), msg)


if __name__ == '__main__':
    unittest.main()
