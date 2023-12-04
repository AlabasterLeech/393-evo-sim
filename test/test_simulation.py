import unittest
from src.Simulation import Simulation


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.sim = Simulation(10, 10)

    def test_load_json(self):
        self.assertEqual(True, True)

    def test_save_json(self):
        self.assertEqual(True, True)

    def test_step(self):
        self.sim.step()
        msg = 'Age is not the same as expected age!'
        self.assertEqual(1, self.sim.age, msg)

    def test_step_gen(self):
        self.sim.step_gen()
        age_msg = 'Age is not the same as expected age!'
        gen_msg = 'Gen is not the same as expected gen!'
        self.assertEqual(0, self.sim.age, age_msg)
        self.assertEqual(1, self.sim.gen, gen_msg)


if __name__ == '__main__':
    unittest.main()
