import random
import math

from const import *
from neuron import *

class NeuralNetwork:
    def __init__(self,):
        # initialize neurons
        self.neurons = []
        for n in range(INPUT_NUM):
            self.neurons.append(Neuron(NeuronType.INPUT))
        for n in range(OUTPUT_NUM):
            self.neurons.append(Neuron(NeuronType.OUTPUT))
        for n in range(MODULATION_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.MODULATION))
        for n in range(NORMAL_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.NORMAL))

        # initialize connections
        self.connections = []
        connection_id = 0
        for n in range(CONNECTION_NUM_LOWER_LIMIT):
            input_id = random.randint(0, len(self.neurons) -1)
            output_id = random.randint(INPUT_NUM, len(self.neurons) -1)
            self.connections.append(Connetion(connection_id, input_id, output_id ))
            connection_id += 1

    def get_output(self,input_vector):
        if(len(input_vector) != INPUT_NUM):
            raise Exception('ERROR:num of input_vector is invalid')

        # Set input_vector
        for n in range(INPUT_NUM):
            self.neurons[n].activation = input_vector[n]

        for n in range(INPUT_NUM, len(self.neurons)):
            activation_sum = 0
            modulation_sum = 0
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid):
                    if(self.connections[c].output_id == n):
                        activation_sum += self.neurons[self.connections[c].input_id].activation * self.connections[c].weight
                        modulation_sum += self.neurons[self.connections[c].input_id].modulation * self.connections[c].weight

class HebbianNetwork:
    pass

class ExHebbianNetwork:
    pass

if __name__ == '__main__':
    n = NeuralNetwork()
    for i in range(len(n.neurons)):
        print(n.neurons[i].activation)
        print(n.neurons[i].modulation)
    n.get_output([1,1])
