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
            self.append(eval(agent_type_string)(self.global_max_connection_id, is_automatic_change,input_num, output_num, normal_num_upper_limit,normal_num_lower_limit, modulation_num_upper_limit, modulation_num_lower_limit, neuron_num_upper_limit,connection_num_upper_limit,connection_num_lower_limit))

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

    @property
    def max_species_id(self):
        species_id_list = [ self[i].species_id for i in range(len(self)) ]
        return max(species_id_list)

    @property
    def species_set(self):
        species_id_list = [ self[i].species_id for i in range(len(self)) ]
        return( set(species_id_list) )

    def get_species_individuals(self, species_id):
        species_individuals = []
        for i in self:
            if(i.species_id == species_id):
                species_individuals.append(copy.deepcopy(i))

        return species_individuals


    """
    def assign_species_id(self, ):
        #assign species id for agents which id is -1
        if(self.max_species_id == -1):
            self[0].species_id = 1

        while( -1.in(species_set) ):
            for species_set:
    """

    def get_distance(self, agent_A, agent_B, c1=1.0, c2=1.0, c3=1.0):
        "各エージェントのconnectionsにidの重複がないことを前提として実装"
        A = copy.deepcopy(agent_A)
        A.connections.sort(key=attrgetter('connection_id'))
        B = copy.deepcopy(agent_B)
        B.connections.sort(key=attrgetter('connection_id'))

        a_id_list=[]
        b_id_list=[]
        for i in range(len(A.connections)):
            a_id_list.append(A.connections[i].connection_id)
        for i in range(len(B.connections)):
            b_id_list.append(B.connections[i].connection_id)

        union = set(a_id_list) & set(b_id_list)
        excess = (len(a_id_list)-len(union)) + (len(b_id_list)-len(union))

        # calculate disjoint and weight_differences

        # ToDo: weight -> initial_weight
        disjoint = 0
        weight_differences = 0
        a_connection_list=[]
        b_connection_list=[]
        for i in range(len(A.connections)):
            if (A.connections[i].connection_id in union):
                a_connection_list.append(A.connections[i])

        for i in range(len(B.connections)):
            if (B.connections[i].connection_id in union):
                b_connection_list.append(B.connections[i])

        for i in range(len(a_connection_list)):
            if(a_connection_list[i].is_valid != b_connection_list[i].is_valid):
                disjoint += 1
            weight_differences += abs(a_connection_list[i].weight - b_connection_list[i].weight)

        if(len(a_connection_list)!=0):
            weight_differences /= len(a_connection_list)

        larger = lambda a,b: a if a>b else b
        larger_connection_num = larger(len(agent_A.connections), len(agent_B.connections))

        distance = c1 * excess / larger_connection_num + c2 * disjoint / larger_connection_num + c3 * weight_differences

        print('union:', union)
        print('excess:', excess)
        print('disjoint:', disjoint)
        print('weight_differences:', weight_differences)
        print('distance:', distance)

        return distance

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

    def evolution_mgg(self, task, elite_num = 0, mutate_prob=0.01, sigma=0.1): # task(): function, which take an agent as argument and return fitness
        self.sort(key=attrgetter('fitness'), reverse = True)

        next_agents = copy.deepcopy(self)
        next_agents.clear()
        for i in range(elite_num):
            elite_agent = copy.deepcopy(self[i])
            elite_agent.reset()
            next_agents.append(elite_agent)

        # evolution
        if(self.agent_num - elite_num%2 == 1):
            raise Exception('Error: (evolution_mgg) agent_num - elite_num must be even number')
        for i in range( (self.agent_num - elite_num) // 2):
            four_agents = []
            larger = lambda a,b: a if a>b else b

            parent = random.choice(self)
            parent_A = copy.deepcopy(parent)
            four_agents.append(parent_A)

            parent = random.choice(self)
            parent_B = copy.deepcopy(parent)
            four_agents.append(parent_B)

            new_agent_a = crossover(parent_A, parent_A.fitness, parent_B, parent_B.fitness)
            new_agent_a = mutate_add_connection(new_agent_a,larger(self.global_max_connection_id,next_agents.global_max_connection_id)) if random.random() < mutate_prob else new_agent_a
            new_agent_a = mutate_disable_connection(new_agent_a) if random.random() < mutate_prob else new_agent_a
            new_agent_a = mutate_add_neuron(new_agent_a, larger(self.global_max_connection_id, next_agents.global_max_connection_id)) if random.random() < mutate_prob else new_agent_a
            new_agent_a = give_dispersion(new_agent_a, rate=mutate_prob, sigma=sigma)
            new_agent_a.fitness = task(new_agent_a)
            four_agents.append(new_agent_a)

            new_agent_b = crossover(parent_A, parent_A.fitness, parent_B, parent_B.fitness)
            new_agent_b = mutate_add_connection(new_agent_b,larger(self.global_max_connection_id,next_agents.global_max_connection_id)) if random.random() < mutate_prob else new_agent_b
            new_agent_b = mutate_disable_connection(new_agent_b) if random.random() < mutate_prob else new_agent_b
            new_agent_b = mutate_add_neuron(new_agent_b, larger(self.global_max_connection_id, next_agents.global_max_connection_id)) if random.random() < mutate_prob else new_agent_b
            new_agent_b = give_dispersion(new_agent_b, rate=mutate_prob, sigma=sigma)
            new_agent_b.fitness = task(new_agent_b)
            four_agents.append(new_agent_b)

            four_agents.sort(key=attrgetter('fitness'), reverse = True)
            best_offspring = four_agents[0]

            fitness_list = [ four_agents[i].fitness for i in range(4) ]
            min_fitness = min(fitness_list)
            max_fitness = max(fitness_list)
            range_fitness = max_fitness - min_fitness +0.001
            fitness_list = [(fitness_list[i] - min_fitness)/range_fitness +0.001 for i in range(len(fitness_list))]
            roulette_offspring = random.choices(four_agents, weights=fitness_list)[0]

            next_agents.append(best_offspring)
            next_agents.append(roulette_offspring)

        for i in range(len(next_agents)):
            next_agents[i].reset()

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
