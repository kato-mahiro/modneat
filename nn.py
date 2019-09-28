import random
import math
from enum import Enum
from const import *

class NeuronType(Enum):
    INPUT = 1
    OUTPUT = 2
    NORMAL = 3
    MODULATION = 4
    
class Neuron:
    def __init__(self, neuron_type:NeuronType, neuron_id):
        self.neuron_id = neuron_id
        self.neuron_type = neuron_type
        self.bias = random.uniform(BIAS_LOWER_LIMIT,BIAS_UPPER_LIMIT)
        self.activation = 0.0

class Connetion:
    def __init__(self, connection_id, input_id, output_id):
        self.connection_id = connection_id
        self.is_valid = True
        self.weight = random.uniform(WEIGHT_LOWER_LIMIT,WEIGHT_UPPER_LIMIT)
        self.initial_weight = self.weight
        self.input_id = input_id
        self.output_id = output_id

class NeuralNetwork:
    def __init__(self,):
        # initialize neurons
        self.neurons = []
        neuron_id = 0
        for n in range(INPUT_NUM):
            self.neurons.append(Neuron(NeuronType.INPUT,neuron_id))
            neuron_id += 1
        for n in range(OUTPUT_NUM):
            self.neurons.append(Neuron(NeuronType.OUTPUT,neuron_id))
            neuron_id += 1
        for n in range(MODULATION_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.MODULATION,neuron_id))
            neuron_id += 1
        for n in range(NORMAL_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.NORMAL,neuron_id))
            neuron_id += 1

        # initialize connections
        self.connections = []
        connection_id = 0
        for n in range(CONNECTION_NUM_LOWER_LIMIT):
            input_id = random.randint(0, self.neuron_num -1)
            output_id = random.randint(INPUT_NUM, self.neuron_num -1)
            self.connections.append(Connetion(connection_id, input_id, output_id ))
            connection_id += 1

    @property
    def neuron_num(self):
        return len(self.neurons)

    def get_output():
        pass

class HebbianNetwork:
    pass

class ExHebbianNetwork:
    pass

if __name__ == '__main__':
    n = NeuralNetwork()
    print(n.neurons)
