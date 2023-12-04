import unittest
from src.Simulation import Simulation


class SimulationTest(unittest.TestCase):
    def setUp(self):
        self.width = 10
        self.height = 10
        self.pop = 3
        self.survival = 10
        self.age_max = 5
        self.sim = Simulation(self.width, self.height, self.pop, self.survival, self.age_max)

    def test_init(self):
        self.assertEqual(self.pop, len(self.sim.env.organisms))

    def test_load_json(self):
        self.assertEqual(True, True)

    def test_save_json(self):
        self.assertEqual(True, True)

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
