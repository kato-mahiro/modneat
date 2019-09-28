import random
import math

from const import *
from neuron import *

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
            input_id = random.randint(0, len(self.neurons) -1)
            output_id = random.randint(INPUT_NUM, len(self.neurons) -1)
            self.connections.append(Connetion(connection_id, input_id, output_id ))
            connection_id += 1

    def get_output(input_vector):
        if(len(input_vector) != INPUT_NUM):
            raise Exception('ERROR:num of input_vector is invalid')
        for n in range(INPUT_NUM):
            neurons[n].activation = input_vector[n]

class HebbianNetwork:
    pass

class ExHebbianNetwork:
    pass

if __name__ == '__main__':
    n = NeuralNetwork()
    for i in range(len(n.neurons)):
        print(n.neurons[i].activation)
        print(n.neurons[i].modulation)
