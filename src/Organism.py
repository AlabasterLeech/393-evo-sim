import math
import random


class Organism:
    _NORTH = 0
    _EAST = 1
    _SOUTH = 2
    _WEST = 3

    STIMULI = [
        lambda organism: [-2, 0, 2, 0][organism.dir],
        lambda organism: [0, 2, 0, -2][organism.dir],
        lambda organism: (organism.x / (organism.env.width - 1) - 0.5) * 4,
        lambda organism: (organism.y / (organism.env.height - 1) - 0.5) * 4,
        lambda organism: (random.random() - 0.5) * 4
    ]
    ACTIONS = [
        lambda organism: {
            setattr(organism, 'x', [organism.x, organism.x + 1, organism.x, organism.x - 1][organism.dir]),
            setattr(organism, 'y', [organism.y - 1, organism.y, organism.y + 1, organism.y][organism.dir])},
        lambda organism: {
            setattr(organism, 'x', [organism.x, organism.x - 1, organism.x, organism.x + 1][organism.dir]),
            setattr(organism, 'y', [organism.y + 1, organism.y, organism.y - 1, organism.y][organism.dir])},
        lambda organism: setattr(organism, 'dir', (organism.dir - 1) % 4),
        lambda organism: setattr(organism, 'dir', (organism.dir + 1) % 4),
        lambda organism: None,
        lambda organism: None
    ]
    STIMULUS_WEIGHT = 2.

    def __init__(self, state):
        # Initialize minimally functional default state
        self.x, self.y = 0, 0
        self.dir = Organism._NORTH
        self.genome = []
        self.network = {}

        # Copy initializer state into members
        self.set_state(state)

    def get_state(self):
        # Return functional current state
        return {
            "x": self.x,
            "y": self.y,
            "dir": self.dir,
            "genome": [[gene[0], gene[1], gene[2]] for gene in self.genome]
        }

    def set_state(self, state):
        # Copy initializer state into members
        for attr in state:
            setattr(self, attr, state[attr])

    def think(self, env):
        # Calculate neuron states
        self.env = env
        for i in range(256):
            if i in self.network:
                self.network[i].calc_output()

    def act(self, env):
        # Generate list of desired actions
        actions = []
        for i in range(len(Organism.ACTIONS)):
            if (0xff - i) in self.network and self.network[0xff - i].get_output_thresh():
                actions.append(i)
        actions = env.check(actions, self)
        for i in actions:
            Organism.ACTIONS[i](self)

    def consume(self, object):
        # Modify values according to object composition
        None

    def mutate(self, chance):
        # Randomly alter singular gene in genome
        if random.random() <= chance:
            target_gene = random.randrange(0, len(self.genome))
            target_byte = random.randrange(0, 3)
            new_byte = self.genome[target_gene][target_byte] ^ (1 << random.randrange(0, 8))
            self.genome[target_gene] = self.genome[target_gene][:target_byte] + bytes([new_byte]) + self.genome[target_gene][target_byte + 1:]

    def build_network(self):
        # Generate fresh neural network from stored genome
        self.network = {}
        for gene in self.genome:
            # Extract neuron IDs and weight from gene
            neuron_src = gene[0]
            neuron_dst = gene[2]
            weight = int.from_bytes([gene[1]], byteorder="little", signed=True) / 64.
            # Skip if neurons are out of order
            if neuron_dst < neuron_src:
                continue
            elif neuron_dst == neuron_src:
                if neuron_src not in self.network:
                    self.network[neuron_src] = Organism.Neuron()
                self.network[neuron_src].bias = weight
                continue
            # Create missing neurons
            if neuron_src not in self.network:
                self.network[neuron_src] = Organism.Neuron()
            if neuron_dst not in self.network:
                self.network[neuron_dst] = Organism.Neuron()
            # Create connection
            self.network[neuron_dst].add_input(self.network[neuron_src], weight)
        # Connect stimuli to first several neurons
        for i in range(len(Organism.STIMULI)):
            if i in self.network:
                self.network[i].add_input(Organism.Stimulus(Organism.STIMULI[i], self), Organism.STIMULUS_WEIGHT)

    def get_genome(self):
        # Return current genome
        return self.genome

    def set_genome(self, new_genome):
        # Replace genome
        self.genome = new_genome

    def get_location(self):
        # Return current location
        return (self.x, self.y)

    class Neuron:
        def __init__(self):
            # Initialize basic neuron
            self.output = 0
            self.bias = 0
            self.threshold = 0.6
            self.inputs = []
            self.outputs = []

        def get_output(self):
            # Return current activation output
            return self.output

        def get_output_thresh(self):
            # Return if current output meets threshold
            return self.output >= self.threshold

        def add_input(self, neuron, weight):
            # Add neuron to list of inputs with weight
            self.inputs.append((neuron, weight))
            # Add this to target's list of outputs
            neuron.add_output(self)

        def add_output(self, neuron):
            # Add neuron to list of outputs
            self.outputs.append(neuron)

        def activation(self, signal):
            # Calculate activation function
            sigmoid = 1 / (1 + math.exp(-2 * signal))
            return math.tanh(2 * sigmoid - 1)

        def calc_output(self):
            # Calculate activation output with current input
            signal = sum([neuron[0].get_output() * neuron[1] for neuron in self.inputs])
            signal += self.bias
            self.output = self.activation(signal)

    class Stimulus:
        def __init__(self, stimulus, organism):
            # Initialize a stimulus
            self.output = stimulus
            self.organism = organism

        def get_output(self):
            # Return stimulus
            if self.output:
                return self.output(self.organism)
            else:
                return 0.

        def add_output(self, _):
            # Dummy function for compatibility
            None