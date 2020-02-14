import copy
import random
import math
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from operator import attrgetter

try:
    from . modneat_settings import *
    from . neuron import *
    from . nn import *
    from . evolution import *
except:
    from modneat_settings import *
    from neuron import *
    from nn import *
    from evolution import *

class Agents(list):
    def __init__(
            self,
            agent_type_string,
            agent_num,
            is_automatic_change = True,

            input_num = INPUT_NUM,
            output_num = OUTPUT_NUM,

            normal_num_upper_limit = NORMAL_NUM_UPPER_LIMIT,
            normal_num_lower_limit = NORMAL_NUM_LOWER_LIMIT,

            modulation_num_upper_limit = MODULATION_NUM_UPPER_LIMIT,
            modulation_num_lower_limit = MODULATION_NUM_LOWER_LIMIT,

            neuron_num_upper_limit = NEURON_NUM_UPPER_LIMIT,

            connection_num_upper_limit = CONNECTION_NUM_UPPER_LIMIT,
            connection_num_lower_limit = CONNECTION_NUM_LOWER_LIMIT,

            weight_upper_limit = WEIGHT_UPPER_LIMIT,
            weight_lower_limit = WEIGHT_LOWER_LIMIT,

            bias_upper_limit = BIAS_UPPER_LIMIT,
            bias_lower_limit = BIAS_LOWER_LIMIT,

            evolution_param_upper_limit = EVOLUTION_PARAM_UPPER_LIMIT,
            evolution_param_lower_limit = EVOLUTION_PARAM_LOWER_LIMIT,

            epsiron_lower_limit = EPSIRON_LOWER_LIMIT,
            epsiron_upper_limit = EPSIRON_UPPER_LIMIT

        ):
        super().__init__()
        self.agent_num = agent_num
        for i in range(self.agent_num):
            #self.append(NeuralNetwork(self.global_max_connection_id))
            self.append(eval(agent_type_string)(self.global_max_connection_id, is_automatic_change,input_num, output_num, normal_num_upper_limit,normal_num_lower_limit, modulation_num_upper_limit, modulation_num_lower_limit))

    @property
    def global_max_connection_id(self):
        """
        self中の各オブジェクトが持つ local_max_connection_id のうち最大のものを返す
        """
        if len(self) == 0:
            return -1
        elif len(self) > 0:
            return max(self, key=lambda x:x.local_max_connection_id).local_max_connection_id

    @property
    def max_fitness(self):
        fitness_list = [ self[i].fitness for i in range(len(self)) ]
        return max(fitness_list)

    @property
    def min_fitness(self):
        fitness_list = [ self[i].fitness for i in range(len(self)) ]
        return min(fitness_list)

    @property
    def average_fitness(self):
        fitness_list = [ self[i].fitness for i in range(len(self)) ]
        return ( sum(fitness_list) / len(fitness_list) )

    def evolution(self, elite_num = 0, mutate_prob=0.01, sigma=0.1):
        self.sort(key=attrgetter('fitness'), reverse = True)

        fitness_list = [ self[i].fitness for i in range(len(self)) ]

        min_fitness = min(fitness_list)
        max_fitness = max(fitness_list)
        range_fitness = max_fitness - min_fitness +0.001

        fitness_list = [(fitness_list[i] - min_fitness)/range_fitness +0.001 for i in range(len(fitness_list))]

        #next_agents = Agents(copy.deepcopy(self[0:elite_num]))
        next_agents = copy.deepcopy(self)
        next_agents.clear()
        for i in range(elite_num):
            self[i].reset()
            next_agents.append(self[i])

        # evolution
        for i in range(self.agent_num - elite_num):
            larger = lambda a,b: a if a>b else b
            parent_A = random.choices(self, weights=fitness_list)[0]
            parent_B = random.choices(self, weights=fitness_list)[0]
            new_agent = crossover(parent_A, parent_A.fitness, parent_B, parent_B.fitness)
            new_agent = mutate_add_connection(new_agent,larger(self.global_max_connection_id,next_agents.global_max_connection_id)) if random.random() < mutate_prob else new_agent
            new_agent = mutate_disable_connection(new_agent) if random.random() < mutate_prob else new_agent
            new_agent = mutate_add_neuron(new_agent, larger(self.global_max_connection_id, next_agents.global_max_connection_id)) if random.random() < mutate_prob else new_agent
            new_agent = give_dispersion(new_agent, rate=mutate_prob, sigma=sigma)
            next_agents.append(new_agent)

        #引数で返すようにしないとなぜか内容が更新されない
        return next_agents

    def save_agents(self,name='undefined.pickle'):
        f = open(name,'wb')
        pickle.dump(self,f)
        f.close

def read_agents(name):
    f = open(name,'rb')
    return(pickle.load(f))

if __name__=='__main__':
    a = Agents('ExHebbianNetwork',10)
    for i in range(10):
        a[0].show_network()
        a=a.evolution(elite_num=0,mutate_prob=0.01,sigma=0.1)
