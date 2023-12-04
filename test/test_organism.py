import unittest
from src.Organism import Organism
from src.Environment import Environment
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
        self.test_neuron.bias = 3
        self.env = Environment(10, 10)
        self.env.organisms = [self.org]

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

    def test_think(self):
        genome = [b'\x01\x10\x05', b'\x01\x10\x06', b'\x01\x10\x07', b'\x01\x10\x08', b'\x01\x10\x01',
                  b'\x02\x20\x05', b'\x02\x20\x06', b'\x02\x20\x07', b'\x02\x20\x08', b'\x02\x20\x02',
                  b'\x03\x30\x05', b'\x03\x30\x06', b'\x03\x30\x07', b'\x03\x30\x08', b'\x03\x30\x03',
                  b'\x04\x40\x05', b'\x04\x40\x06', b'\x04\x40\x07', b'\x04\x40\x08', b'\x04\x40\x04',
                  b'\x05\x15\x05', b'\x06\x25\x06', b'\x07\x35\x07', b'\x08\x45\x08']
        self.org.set_genome(genome)
        self.org.build_network()
        self.org.think(self.env)
        msg = 'Output was not modified and did not exceed output threshold!'
        # self.assertTrue(self.org.network[8].get_output_thresh(), msg)

    def test_act(self):
        neurons = {254: self.neuron2,         # Backwards
                   255: self.neuron1}         # Forwards
        back_org = Organism({"x": 4, "y": 3})
        self.env.organisms.append(back_org)
        self.org.network = neurons
        self.org.act(self.env)
        exp_pos = (4, 5)
        msg = "Organism performed a different (set of) actions!"
        self.assertEqual(exp_pos, self.org.get_location(), msg)

    def test_mutate(self):
        chance = 2147483647
        genome = [b'\x01\x01\x01']
        self.org.set_genome(genome)
        self.org.mutate(chance)
        new_genome = self.org.get_genome()
        msg = 'Random byte in gene did not change!'
        self.assertTrue(new_genome != genome[0], msg)

    def test_build_network(self):
        weight = int.from_bytes(b'\x02', byteorder="little", signed=True) / 64.
        # Test for skipping
        self.org.set_genome([b'\x03\x02\x01'])
        self.org.build_network()
        skip_net_msg = 'Did not skip the neurons!'
        self.assertEqual({}, self.org.network, skip_net_msg)

        # Test for empty network
        self.org.set_genome([b'\x01\x02\x03'])
        self.org.build_network()
        empty_net_msg = 'Not the correct weight value!'
        self.assertEqual(weight, self.org.network[3].inputs[0][1], empty_net_msg)

        # Test for same src ID for two genes
        self.org.set_genome([b'\x01\x02\x03', b'\x01\x02\x04'])
        self.org.build_network()
        same_id_output_msg = 'Neuron does not have the correct number of output Neurons!'
        same_id_input_msg = 'Neuron does not have the correct number of input Neurons!'
        self.assertEqual(2, len(self.org.network[1].outputs), same_id_output_msg)
        self.assertEqual(2, len(self.org.network[3].inputs), same_id_input_msg)

        # Test for same src and dst ID
        self.org.set_genome([b'\x01\x02\x01'])
        self.org.build_network()
        same_ids_msg = 'Neuron bias was not set to weight!'
        self.assertEqual(weight, self.org.network[1].bias, same_ids_msg)

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

    '''
    Neuron Tests
    '''

    def test_activation(self):
        signal = 5
        activated = self.test_neuron.activation(signal)
        sigmoid = 1 / (1 + math.exp(-2 * signal))
        tanh = math.tanh(2 * sigmoid - 1)
        msg = 'Different activation values!'
        self.assertEqual(tanh, activated, msg)

    def test_calc_output(self):
        self.test_neuron.inputs = [(self.neuron1, 1), (self.neuron2, 2)]
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

    def test_get_output_thresh(self):
        message = 'Incorrect comparison in get_output_thresh!'
        low_out = 0.5
        self.test_neuron.output = low_out
        self.assertFalse(self.test_neuron.get_output_thresh())
        high_out = 1.0
        self.test_neuron.output = high_out
        self.assertTrue(self.test_neuron.get_output_thresh())

    def test_add_input(self):
        msg = 'Default input not empty!'
        self.assertTrue(self.test_neuron.inputs == [], msg)
        self.test_neuron.add_input(self.neuron1, 1)
        msg_after = 'Wrong input neuron or weight!'
        self.assertTrue((self.neuron1, 1) in self.test_neuron.inputs, msg_after)
        msg_other = 'Did not properly connect neurons or wrong weight!'
        self.assertTrue(self.test_neuron in self.neuron1.outputs, msg_other)


if __name__ == '__main__':
    unittest.main()
