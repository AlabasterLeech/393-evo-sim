import unittest
from src.Organism import Organism
import math


class OrganismTest(unittest.TestCase):
    def setUp(self):
        org_state = {"x": 4,
                     "y": 4,
                     "dir": Organism._NORTH,
                     "genome": [1, 2, 3]}
        self.org = Organism(org_state)
        self.neuron1 = Organism.Neuron()
        self.neuron1.output = 3
        self.neuron2 = Organism.Neuron()
        self.neuron2.output = 4
        self.test_neuron = Organism.Neuron()
        inputs = [(self.neuron1, 1), (self.neuron2, 2)]
        self.test_neuron.inputs = inputs
        self.test_neuron.bias = 3

    def test_get_state(self):
        org_state = {"x": 4,
                     "y": 4,
                     "dir": Organism._NORTH,
                     "genome": [1, 2, 3]}
        msg = 'States are not equal!'
        self.assertEqual(org_state, self.org.get_state(), msg)

    def test_set_state(self):
        new_org_state = {"x": 1,
                         "y": 1,
                         "dir": Organism._NORTH,
                         "genome": [1, 1, 1]}
        self.org.set_state(new_org_state)
        d = self.org.get_state()
        msg = 'States are not equal!'
        self.assertEqual(new_org_state, self.org.get_state(), msg)

    def test_get_genome(self):
        gen = [1, 2, 3]
        msg = 'Genomes are not equal!'
        self.assertEqual(gen, self.org.get_genome(), msg)

    def test_set_genome(self):
        # Checking for genome len = 1
        one_gen = 1
        self.org.set_genome(one_gen)
        msg = 'Genomes are not equal!'
        self.assertEqual(one_gen, self.org.get_genome(), msg)
        # Checking for changing genome len
        new_gen = [9, 8]
        self.org.set_genome(new_gen)
        self.assertEqual(new_gen, self.org.get_genome(), msg)

    def test_get_location(self):
        location = (4, 4)
        msg = 'Different locations!'
        self.assertEqual(location, self.org.get_location(), msg)

    def test_activation(self):
        signal = 5
        activated = self.test_neuron.activation(signal)
        sigmoid = 1 / (1 + math.exp(-2 * signal))
        tanh = math.tanh(2 * sigmoid - 1)
        msg = 'Different activation values!'
        self.assertEqual(tanh, activated, msg)

    def test_calc_output(self):
        self.test_neuron.calc_output()
        test_output = self.test_neuron.get_output()
        calc_signal = self.neuron1.output * 1 + self.neuron2.output * 2 + self.test_neuron.bias
        calc_out = self.test_neuron.activation(calc_signal)
        msg = 'Different output values!'
        self.assertEqual(calc_out, test_output, msg)

    def test_get_output(self):
        # Check default output value
        msg = 'Different output values!'
        self.assertEqual(self.test_neuron.output, 0, msg)


if __name__ == '__main__':
    unittest.main()
