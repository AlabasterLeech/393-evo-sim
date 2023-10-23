import unittest
from random import Random
from Environment import Environment


class EnvironmentTest(unittest.TestCase):
    def test_upper(self):
        self.random = Random(1)
        self.env = Environment(10, 10)

    # first value is to be tested result, second value is the true result
    # Tests if get_state returns the correct dictionary
    def test_get_state(self):
        test_dic = {"organisms": [],
                    "objects": []}
        message = 'Environment returned a different state!'
        self.assertEqual(self.env.get_state(), test_dic, message)

    # Tests if set_state correctly sets the values of its lists
    def test_set_state(self):
        test_dic = {"organisms": [1, 2, 3],
                    "objects": [2, 3, 4]}
        self.env.set_state(test_dic)
        message = 'Environment did not set the input state properly!'
        self.assertEqual(self.env.get_state(), test_dic, message)

    # Tests if crossover returns a new genome made from its input genomes
    # This also tests for the breed method, since breed calls crossover and returns the new Organism
    def test_crossover(self):
        gen1 = [1, 2, 3, 4]
        gen2 = [5, 6, 7, 8]
        gen3 = self.env.crossover(gen1, gen2)
        message = 'Child genome the same as Parent genome!'
        self.assertTrue(gen3 != gen1, message)
        self.assertTrue(gen3 != gen2, message)

    # Tests if space open returns the correct bool value
    def test_space_open(self):




if __name__ == '__main__':
    unittest.main()
