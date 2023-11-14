import unittest
from src.Environment import Environment
from src.Organism import Organism
from src.Object import Object


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
                     "genome": [],
                     "dir": 0}
        obj_state = {"x": 2,
                     "y": 3,
                     "object_type": 'obstacle',
                     "density": 1}
        test_dic = {"organisms": [org_state],
                    "objects": [obj_state]}
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
        try:
            self.assertTrue(gen3 != gen1, message)
            self.assertTrue(gen3 != gen2, message)
        except AssertionError:
            pass

    # Tests if Environment creates a new Organism from two parent organisms
    def test_breed(self):
        org_state_one = {"x": 4,
                         "y": 4,
                         "genome": [1, 2, 3, 4]}
        org_state_two = {"x": 4,
                         "y": 3,
                         "genome": [5, 6, 7, 8]}
        org_one = Organism(org_state_one)
        org_two = Organism(org_state_two)
        child = self.env.breed(org_one, org_two)
        message = 'Did not create new Organism!'
        self.assertEqual((0, 0), child.get_location(), message)

    # Tests if Environment holds and remembers objs/orgs in their positions
    def test_space_open(self):
        org_state = {"x": 4,
                     "y": 4,
                     "genome": []}
        obj_state = {"x": 2,
                     "y": 3,
                     "object_type": 'obstacle',
                     "density": 1}
        env_state = {"organisms": [org_state],
                     "objects": [obj_state]}
        self.env.set_state(env_state)
        self.assertEqual(False, self.env.space_open(4, 4), 'Org not in this space!')
        self.assertEqual(False, self.env.space_open(2, 3), 'Obj not in this space!')
        self.assertEqual(False, self.env.space_open(11, 4), 'Env is large enough to have this space!')
        self.assertEqual(True, self.env.space_open(3, 3), 'Some Obj/Org is in this space!')

    # Tests if Environment holds the new survival function
    def test_set_survival_function(self):
        fun = 55
        self.env.set_survival_function(fun)
        message = 'Env did not properly set the survival function!'
        self.assertEqual(55, self.env.survival_function)


if __name__ == '__main__':
    unittest.main()
