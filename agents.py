import copy
import random
import math
import networkx as nx
import matplotlib.pyplot as plt
from operator import attrgetter

try:
    from . const import *
    from . neuron import *
    from . nn import *
    from . evolution import *
except:
    from const import *
    from neuron import *
    from nn import *
    from evolution import *

class Agents(list):
    def __init__(
            self,
            agent_type_string,
            agent_num
        ):
        super().__init__()
        self.agent_num = agent_num
        for i in range(self.agent_num):
            #self.append(NeuralNetwork(self.global_max_connection_id))
            self.append(eval(agent_type_string)(self.global_max_connection_id))
        print(type(self))

    @property
    def global_max_connection_id(self):
        """
        self中の各オブジェクトが持つ local_max_connection_id のうち最大のものを返す
        """
        if len(self) == 0:
            return 0
        elif len(self) > 0:
            return max(self, key=lambda x:x.local_max_connection_id).local_max_connection_id

    def evolution(self):
        print(type(self))
        self.sort(key=attrgetter('fitness'), reverse = True)
        print("1",type(self))
        print(self)
        fitness_list = [ self[i].fitness for i in range(len(self)) ]
        print("2",type(self))

        next_agents = copy.deepcopy(self[0:ELITE_NUM])
        print("3",type(self))

        # evolution
        for i in range(AGENT_NUM - ELITE_NUM):
            print("4",type(self))
            parent_A = random.choices(self, weights=fitness_list)[0]
            parent_B = random.choices(self, weights=fitness_list)[0]
            new_agent = crossover(parent_A, parent_A.fitness, parent_B, parent_B.fitness)
            print(type(self))
            new_agent = mutate_add_connection(new_agent, self.global_max_connection_id) if random.random() < MUTATE_PROB else new_agent
            new_agent = mutate_disable_connection(new_agent) if random.random() < MUTATE_PROB else new_agent
            new_agent = mutate_add_neuron(new_agent, self.global_max_connection_id) if random.random() < MUTATE_PROB else new_agent
            new_agent = give_dispersion(new_agent)
            next_agents.append(new_agent)
        self = next_agents
