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
    def __init__(self, neuron_type:NeuronType):
        self.neuron_type = neuron_type
        self.bias = random.uniform(BIAS_LOWER_LIMIT,BIAS_UPPER_LIMIT)
        self.activation = 0.0

class Connetion:
    def __init__(self, innovation_no, input_id, output_id):
        self.innovation_no = innovation_no
        if(random.random < CONNECTION_VALID_RATE):
            self.is_valid = True
        else:
            self.is_valid = False
        self.initial_weight = random.uniform(WEIGHT_LOWER_LIMIT,WEIGHT_UPPER_LIMIT)
        self.weight = initial_weight
        self.input_id = input_id
        self.output_id = output_id

class NeuralNetwork:
    def __init__(self,):
        self.neurons = []
        for n in range(INPUT_NUM):
            self.neurons.append(Neuron(NeuronType.INPUT))
        for n in range(OUTPUT_NUM):
            self.neurons.append(Neuron(NeuronType.OUTPUT))
        for n in range(MODULATION_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.MODULATION))
        for n in range(NORMAL_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.NORMAL))
        self.connections = []

    def get_output():
        pass


class HebbianNetwork:
    pass

class ExHebbianNetwork:
    pass

if __name__ == '__main__':
    n = NeuralNetwork()
    print(n.neurons)
