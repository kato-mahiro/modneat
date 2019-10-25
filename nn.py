import random
import math
import networkx as nx
import matplotlib.pyplot as plt

try:
    from . modneat_const import *
    from . neuron import *
except:
    from modneat_const import *
    from neuron import *

class NeuralNetwork:
    def __init__(self,global_max_connection_id = 0):
        # initialize neurons
        self.neurons = []
        for n in range(INPUT_NUM):
            self.neurons.append(Neuron(NeuronType.INPUT))
        for n in range(OUTPUT_NUM):
            self.neurons.append(Neuron(NeuronType.OUTPUT))
        for n in range(NORMAL_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.NORMAL))
        for n in range(MODULATION_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.MODULATION))

        # initialize connections
        self.connections = []
        connection_id = global_max_connection_id +1
        for n in range(CONNECTION_NUM_LOWER_LIMIT):
            input_id = random.randint(0, len(self.neurons) -1)
            output_id = random.randint(INPUT_NUM, len(self.neurons) -1)
            self.connections.append(Connetion(connection_id, input_id, output_id ))
            connection_id += 1

        self.epsiron = random.uniform(EPSIRON_LOWER_LIMIT, EPSIRON_UPPER_LIMIT)

        self.fitness = 0.0

    @property
    def output_vector(self):
        output_vector = []
        for n in range(INPUT_NUM, INPUT_NUM + OUTPUT_NUM):
            output_vector.append(self.neurons[n].activation)
        return output_vector

    @property
    def local_max_connection_id(self):
        maxid = 0
        for i in range(len(self.connections)):
            if(self.connections[i].connection_id > maxid):
                maxid = self.connections[i].connection_id
        return maxid

    @property
    def num_of_normal_neuron(self):
        num = 0
        for i in range( INPUT_NUM + OUTPUT_NUM, len(self.neurons)):
            if(self.neurons[i].neuron_type == NeuronType.NORMAL):
                num += 1
        return num
    
    @property
    def num_of_modulation_neuron(self):
        num = 0
        for i in range( INPUT_NUM + OUTPUT_NUM, len(self.neurons)):
            if(self.neurons[i].neuron_type == NeuronType.MODULATION):
                num += 1
        return num

    @property
    def num_of_active_connection(self):
        num = 0
        for i in range( len(self.connections) ):
            if(self.connections[i].is_valid == True):
                num += 1
        return num

    def revert_to_initial_condition(self):
        for i in range(len(self.connections)):
            self.connections[i].weight = self.connections[i].initial_weight
        for i in range(len(self.neurons)):
            if(self.neurons[i].neuron_type != NeuronType.MODULATION):
                self.neurons[i].activation = 0.0
            else:
                self.neurons[i].modulation = 0.0
        self.fitness = 0.0

    def get_output(self,input_vector):
        if(len(input_vector) != INPUT_NUM):
            raise Exception('ERROR:num of input_vector is invalid')

        # Set input_vector
        for n in range(INPUT_NUM):
            self.neurons[n].activation = input_vector[n]

        for n in range( len(self.neurons)-1, INPUT_NUM-1, -1):
            activated_sum = 0
            modulated_sum = 0
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid and self.connections[c].output_id == n):
                    activated_sum += self.neurons[self.connections[c].input_id].activation * self.connections[c].weight
                    modulated_sum += self.neurons[self.connections[c].input_id].modulation * self.connections[c].weight

            if(self.neurons[n].neuron_type != NeuronType.MODULATION):
                self.neurons[n].activation = math.tanh(activated_sum + self.neurons[n].bias)
            else:
                self.neurons[n].modulation = math.tanh(activated_sum + self.neurons[n].bias)

            # if Hebbian or ExHebbian, update weight using modulated_sum
        return self.output_vector

    def show_network(self, path=None):

        G=nx.MultiDiGraph()

        for n in range(len(self.neurons)):
            if(self.neurons[n].neuron_type == NeuronType.INPUT):
                pos_string= str(n*2)+ ",10!"
                #label_string = str(n) + "\n" + str( round(self.neurons[n].bias,2))
                label_string = str(n)
                G.add_node(n, color='yellow',size=1.5, pos = pos_string,label=label_string, font_size = 8)
            elif(self.neurons[n].neuron_type == NeuronType.OUTPUT):
                pos_string= str((n - INPUT_NUM) *2)+ ",0!"
                label_string = str(n) + "\n" + str( round(self.neurons[n].bias,2))
                G.add_node(n, color='red',size=1.5, pos = pos_string, label=label_string, fot_size = 8)
            elif(self.neurons[n].neuron_type == NeuronType.MODULATION):
                label_string = str(n) + "\n" + str( round(self.neurons[n].bias,2))
                G.add_node(n, color='blue',size=1.5,label=label_string, fot_size = 8, shape='d')
            elif(self.neurons[n].neuron_type == NeuronType.NORMAL):
                label_string = str(n) + "\n" + str( round(self.neurons[n].bias,2))
                G.add_node(n, color='black',size=1.5,label=label_string, fot_size = 8)

        for c in range(len(self.connections)):
            if(self.connections[c].is_valid == True):
                i = self.connections[c].input_id
                o = self.connections[c].output_id
                #w = round(self.connections[c].weight,2)
                w = self.connections[c].connection_id
                G.add_edge(i,o,label=w)

        pos = nx.spring_layout(G,k=0.1)
        nx.draw_networkx(G, pos, with_labels=True, alpha=0.5, size=(10,100))
        nx.nx_agraph.view_pygraphviz(G,prog='fdp',path=path)
        
class HebbianNetwork(NeuralNetwork):
    def get_output(self,input_vector):
        if(len(input_vector) != INPUT_NUM):
            raise Exception('ERROR:num of input_vector is invalid')

        # Set input_vector
        for n in range(INPUT_NUM):
            self.neurons[n].activation = input_vector[n]

        for n in range( len(self.neurons)-1, INPUT_NUM-1, -1):
            activated_sum = 0
            modulated_sum = 0
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid and self.connections[c].output_id == n):
                    activated_sum += self.neurons[self.connections[c].input_id].activation * self.connections[c].weight
                    modulated_sum += self.neurons[self.connections[c].input_id].modulation * self.connections[c].weight

            if(self.neurons[n].neuron_type != NeuronType.MODULATION):
                self.neurons[n].activation = math.tanh(activated_sum + self.neurons[n].bias)
            else:
                self.neurons[n].modulation = math.tanh(activated_sum + self.neurons[n].bias)

            # if Hebbian or ExHebbian, update weight using modulated_sum
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid and self.connections[c].output_id == n):
                    if(modulated_sum == 0):
                        self.connections[c].weight += \
                            self.epsiron * self.neurons[n].activation * self.neurons[ self.connections[c].input_id ].activation
                    elif(modulated_sum != 0):
                        self.connections[c].weight += \
                            modulated_sum * (self.epsiron * self.neurons[n].activation * self.neurons[ self.connections[c].input_id ].activation)
                    self.connections[c].weight = WEIGHT_UPPER_LIMIT if (self.connections[c].weight > WEIGHT_UPPER_LIMIT) else self.connections[c].weight
                    self.connections[c].weight = WEIGHT_LOWER_LIMIT if (self.connections[c].weight < WEIGHT_LOWER_LIMIT) else self.connections[c].weight

        return self.output_vector

class ExHebbianNetwork(NeuralNetwork):
    def __init__(self,global_max_connection_id = 0):
        super().__init__(global_max_connection_id)
        self.A= random.uniform(EVOLUTION_PARAM_LOWER_LIMIT, EVOLUTION_PARAM_UPPER_LIMIT)
        self.B= random.uniform(EVOLUTION_PARAM_LOWER_LIMIT, EVOLUTION_PARAM_UPPER_LIMIT)
        self.C= random.uniform(EVOLUTION_PARAM_LOWER_LIMIT, EVOLUTION_PARAM_UPPER_LIMIT)
        self.D= random.uniform(EVOLUTION_PARAM_LOWER_LIMIT, EVOLUTION_PARAM_UPPER_LIMIT)

    def get_output(self,input_vector):
        if(len(input_vector) != INPUT_NUM):
            raise Exception('ERROR:num of input_vector is invalid')

        # Set input_vector
        for n in range(INPUT_NUM):
            self.neurons[n].activation = input_vector[n]

        for n in range( len(self.neurons)-1, INPUT_NUM-1, -1):
            activated_sum = 0
            modulated_sum = 0
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid and self.connections[c].output_id == n):
                    activated_sum += self.neurons[self.connections[c].input_id].activation * self.connections[c].weight
                    modulated_sum += self.neurons[self.connections[c].input_id].modulation * self.connections[c].weight

            if(self.neurons[n].neuron_type != NeuronType.MODULATION):
                self.neurons[n].activation = math.tanh(activated_sum + self.neurons[n].bias)
            else:
                self.neurons[n].modulation = math.tanh(activated_sum + self.neurons[n].bias)

            # if Hebbian or ExHebbian, update weight using modulated_sum
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid and self.connections[c].output_id == n):
                    if(modulated_sum == 0):
                        self.connections[c].weight += \
                            self.epsiron * \
                            (
                                self.neurons[n].activation * self.neurons[ self.connections[c].input_id ].activation * self.A + \
                                self.neurons[n].activation * self.B + \
                                self.neurons[ self.connections[c].input_id ].activation * self.C + \
                                self.D
                            )
                    elif(modulated_sum != 0):
                        self.connections[c].weight += \
                            modulated_sum * self.epsiron * \
                            (
                                self.neurons[n].activation * self.neurons[ self.connections[c].input_id ].activation * self.A + \
                                self.neurons[n].activation * self.B + \
                                self.neurons[ self.connections[c].input_id ].activation * self.C + \
                                self.D
                            )
                    self.connections[c].weight = WEIGHT_UPPER_LIMIT if (self.connections[c].weight > WEIGHT_UPPER_LIMIT) else self.connections[c].weight
                    self.connections[c].weight = WEIGHT_LOWER_LIMIT if (self.connections[c].weight < WEIGHT_LOWER_LIMIT) else self.connections[c].weight

        return self.output_vector
if __name__ == '__main__':
    n = HebbianNetwork()
    n.show_network()
    n.get_output([1,1])
    n.show_network()
