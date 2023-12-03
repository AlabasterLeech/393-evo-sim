import unittest
from src.Environment import Environment
from src.Organism import Organism
from src.Object import Object


class EnvironmentTest(unittest.TestCase):
    def setUp(self):
        self.env = Environment(10, 10)
        self.north = Organism({"x": 0, "y": 0, "dir": Organism._NORTH})
        self.east = Organism({"x": 2, "y": 2, "dir": Organism._EAST})
        self.south = Organism({"x": 9, "y": 9, "dir": Organism._SOUTH})
        self.west = Organism({"x": 0, "y": 6, "dir": Organism._WEST})

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
        message = 'Child gen not from either Parent genome!'
        for gene in gen3:
            self.assertTrue(gene in gen1 or gene in gen2, message)

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

    def test_check(self):
        wester = [Organism({"x": 2, "y": 2, "dir": Organism._WEST})]
        self.env.organisms = wester
        exp_valid_actions = [0, 1, 2, 3]
        act_valid_actions = self.env.check([0, 1, 2, 3, 4, 5], wester[0])
        msg = 'Actual and expected actions not the same!'
        self.assertEqual(exp_valid_actions, act_valid_actions, msg)

    def test_check_move_forward(self):
        organisms = [self.north, self.east, self.south, self.west]
        self.env.organisms = organisms
        true_msg = "Organism could not move in this direction!"
        false_msg = "Organism could move in this direction!"
        self.assertEqual(True, self.env.check_move_forward(self.north), true_msg)
        self.assertEqual(True, self.env.check_move_forward(self.east), true_msg)
        self.assertEqual(True, self.env.check_move_forward(self.south), true_msg)
        self.assertEqual(False, self.env.check_move_forward(self.west), false_msg)

    def test_check_move_backward(self):
        organisms = [self.north, self.east, self.south, self.west]
        self.env.organisms = organisms
        true_msg = "Organism could not move in this direction!"
        false_msg = "Organism could move in this direction!"
        self.assertEqual(False, self.env.check_move_backward(self.north), false_msg)
        self.assertEqual(True, self.env.check_move_backward(self.east), true_msg)
        self.assertEqual(False, self.env.check_move_backward(self.south), false_msg)
        self.assertEqual(True, self.env.check_move_backward(self.west), true_msg)
        norther = Organism({"x": 4, "y": 4, "dir": Organism._NORTH})
        souther = Organism({"x": 0, "y": 8, "dir": Organism._SOUTH})
        self.assertEqual(True, self.env.check_move_backward(norther), true_msg)
        self.assertEqual(True, self.env.check_move_backward(souther), true_msg)

    def test_check_consume(self):
        organisms = [self.north]
        food = [Object(0, 1, 'food', 0.75)]
        self.env.organisms = organisms
        self.env.objects = food
        true_msg = "Organism could not consume in this direction!"
        false_msg = "Organism could consume in this direction!"
        self.assertEqual(True, self.env.check_consume(self.north), true_msg)
        self.assertEqual(False, self.env.check_consume(self.east), false_msg)
        self.assertEqual(False, self.env.check_consume(self.south), false_msg)
        self.assertEqual(False, self.env.check_consume(self.west), false_msg)

    def test_check_consume_true(self):
        south = Organism({"x": 5, "y": 5, "dir": Organism._SOUTH})
        east = Organism({"x": 5, "y": 5, "dir": Organism._EAST})
        west = Organism({"x": 5, "y": 5, "dir": Organism._WEST})
        sfood = Object(5, 4, 'food', 0.75)
        efood = Object(6, 5, 'food', 0.75)
        wfood = Object(4, 5, 'food', 0.75)
        organs = [south, east, west]
        foods = [sfood, efood, wfood]
        self.env.organisms = organs
        self.env.objects = foods
        true_msg = "Organism could not consume in this direction!"
        self.assertEqual(True, self.env.check_consume(south), true_msg)
        self.assertEqual(True, self.env.check_consume(east), true_msg)
        self.assertEqual(True, self.env.check_consume(west), true_msg)

    def test_check_kill(self):
        norther = Organism({"x": 0, "y": 1, "dir": Organism._NORTH})
        organisms = [self.north, norther]
        self.env.organisms = organisms
        true_msg = "Organism could not kill in this direction!"
        false_msg = "Organism could kill in this direction!"
        self.assertEqual(True, self.env.check_kill(self.north), true_msg)
        self.assertEqual(False, self.env.check_kill(self.east), false_msg)
        self.assertEqual(False, self.env.check_kill(self.south), false_msg)
        self.assertEqual(False, self.env.check_kill(self.west), false_msg)

    def test_check_kill_true(self):
        south = Organism({"x": 5, "y": 5, "dir": Organism._SOUTH})
        east = Organism({"x": 5, "y": 5, "dir": Organism._EAST})
        west = Organism({"x": 5, "y": 5, "dir": Organism._WEST})
        souther = Organism({"x": 5, "y": 4, "dir": Organism._SOUTH})
        easter = Organism({"x": 6, "y": 5, "dir": Organism._EAST})
        wester = Organism({"x": 4, "y": 5, "dir": Organism._WEST})
        organs = [south, east, west, souther, easter, wester]
        self.env.organisms = organs
        true_msg = "Organism could not kill in this direction!"
        self.assertEqual(True, self.env.check_kill(south), true_msg)
        self.assertEqual(True, self.env.check_kill(east), true_msg)
        self.assertEqual(True, self.env.check_kill(west), true_msg)


if __name__ == '__main__':
    unittest.main()
