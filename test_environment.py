import unittest
from Environment import Environment
from Organism import Organism


class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.env = Environment(10, 10)

    # Tests if get_state returns the correct dictionary
    def test_get_state(self):
        test_dic = {"organisms": [],
                    "objects": []}
        message = 'Environment returned a different state!'
        self.assertEqual(test_dic, self.env.get_state(), message)

    # Tests if set_state correctly sets the values of its lists
    def test_set_state(self):
        org_state = {"x": 4,
                     "y": 4,
                     "genome": []}
        test_dic = {"organisms": [org_state],
                    "objects": []}
        self.env.set_state(test_dic)
        message = 'Environment did not set the input state properly!'
        self.assertEqual(test_dic, self.env.get_state(), message)

    # Tests if crossover returns a new genome made from its input genomes
    # This also tests for the breed method, since breed calls crossover and returns the new Organism
    def test_crossover(self):
        gen1 = [1, 2, 3, 4]
        gen2 = [5, 6, 7, 8]
        gen3 = self.env.crossover(gen1, gen2)
        message = 'Child genome the same as Parent genome!'
        self.assertTrue(gen3 != gen1, message)
        self.assertTrue(gen3 != gen2, message)

    # Tests if Environment holds and remembers objs/orgs in their positions
    def test_space_open(self):
        org_state = {"x": 4,
                     "y": 4,
                     "genome": []}
        env_state = {"organisms": org_state,
                     "objects": []}
        self.env.set_state(env_state)
        print(self.env.get_state())
        print(self.env.organisms[0].get_location() == (4,4))
        self.assertEqual(False, self.env.space_open(4, 4), 'Obj/Org not in this space!')
        self.assertEqual(False, self.env.space_open(11, 4), 'Env is large enough to have this space!')
        self.assertEqual(True, self.env.space_open(3, 3), 'Some Obj/Org is in this space!')


if __name__ == '__main__':
    unittest.main()
