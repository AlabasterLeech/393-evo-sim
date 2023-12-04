import json
import unittest
import os
import time
from unittest.mock import Mock, patch
from src.Simulation import Simulation


class SimulationTest(unittest.TestCase):
    def setUp(self):
        self.width = 10
        self.height = 10
        self.pop = 3
        self.food = 0.75
        self.survival = 10
        self.age_max = 5
        self.sim = Simulation(self.width, self.height, self.pop, self.food, self.survival, self.age_max)
        self.survival_function = self.sim.survival_function
        self.survival_function_name = self.sim.survival_function_name

    def test_init(self):
        self.assertEqual(self.pop, len(self.sim.env.organisms))
        new_sim = Simulation(5, 5, 25, self.food, self.survival, self.age_max)
        new_sim.step_gen()

    def test_load_json(self):
        filename = "test_load_json.json"
        filepath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", filename))
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
        sim_test = Simulation(self.width, self.height, self.pop, self.food, "North quarter", self.age_max)
        self.assertEqual(Simulation.SURVIVAL["North quarter"], sim_test.survival_function)

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
        self.sim.step_gen()
        age_msg = 'Age is not the same as expected age!'
        gen_msg = 'Gen is not the same as expected gen!'
        self.assertEqual(0, self.sim.age, age_msg)
        self.assertEqual(1, self.sim.gen, gen_msg)


if __name__ == '__main__':
    unittest.main()
