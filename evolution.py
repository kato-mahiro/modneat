import copy
import random

try:
    from . const import *
    from . nn import *
except:
    from const import *
    from nn import *

def crossover(agent_A, fitness_A, agent_B, fitness_B):
    A = copy.deepcopy(agent_A)
    B = copy.deepcopy(agent_B)
    A.revert_to_initial_condition()
    B.revert_to_initial_condition()

    offspring = copy.deepcopy(A)
    offspring.neurons = []
    offspring.connections = []

    for a in range(len(A.connections)):
        for b in range(len(B.connections)):
            if A.connections[a] != None and B.connections[b] != None and A.connections[a].connection_id == B.connections[b].connection_id:
                offspring.connections.append(copy.deepcopy( random.choice([ A.connections[a],B.connections[b] ]) ) )
                A.connections[a] = None
                B.connections[b] = None
                break
    
    A.connections = [x for x in A.connections if x != None]
    B.connections = [x for x in B.connections if x != None]
    if(fitness_A > fitness_B):
        remaining_connections = A.connections
    elif(fitness_B > fitness_A):
        remaining_connections = B.connections
    elif(fitness_A == fitness_B):
        remaining_connections = A.connections + B.connections
        remaining_connections = [x for x in remaining_connections if random.randint(0,1)]
    offspring.connections += remaining_connections

    # create neurons of offspring
    longer = A if (len(A.neurons) > len(B.neurons) ) else B
    shorter = B if (len(A.neurons) > len(B.neurons) ) else A
    A_B_neurons = list(zip(A.neurons,B.neurons))
    for i in range(len(A_B_neurons)):
        offspring.neurons.append( random.choice(A_B_neurons[i] ) )
    for i in range(len(shorter.neurons), len(longer.neurons)):
        offspring.neurons.append( longer.neurons[i])

    #その他のパラメータ (epsiron,A,B,C,Dの交叉)
    if(fitness_A > fitness_B):
        offspring.epsiron = A.epsiron
    elif(fitness_B > fitness_A):
        offspring.epsiron = B.epsiron
    elif(fitness_A == fitness_B):
        offspring.epsiron = random.choice([A.epsiron, B.epsi])

    if A.__class__.__name__ == 'ExHebbianNetwork':
        if(fitness_A > fitness_B):
            offspring.A = A.A
            offspring.B = A.B
            offspring.C = A.C
            offspring.D = A.D
        elif(fitness_B > fitness_A):
            offspring.A = B.A
            offspring.B = B.B
            offspring.C = B.C
            offspring.D = B.D
        elif(fitness_A == fitness_B):
            offspring.A = random.choice([A.A,B.A])
            offspring.B = random.choice([A.B,B.B])
            offspring.C = random.choice([A.C,B.C])
            offspring.D = random.choice([A.D,B.D])

    return offspring

def mutate_add_connection(a, global_max_connection_id ):
    agent = copy.deepcopy(a)
    agent.revert_to_initial_condition()
    if(agent.num_of_active_connection >= CONNECTION_NUM_UPPER_LIMIT):
        return agent
    else:
        input_id = random.randint(0, len(agent.neurons) -1)
        output_id = random.randint(INPUT_NUM, len(agent.neurons) -1)
        connection_id = global_max_connection_id +1
        agent.connections.append(Connetion(connection_id, input_id, output_id ))
        print("新しいidのニューロンが追加されました")
        print("idは",connection_id)
        return agent

def mutate_disable_connection(a):
    """
    なんか適当なコネクションを選んでとりあえず無効化する
    """
    agent = copy.deepcopy(a)
    agent.revert_to_initial_condition()
    if(agent.num_of_active_connection <= CONNECTION_NUM_LOWER_LIMIT):
        return agent
    else:
        while(True):
            n = random.randint(0, len(agent.connections)-1 )
            if agent.connections[n].is_valid == True:
                agent.connections[n].is_valid = False
                return agent


def mutate_add_neuron(a, global_max_connection_id):
    """
    1.なんか適当なコネクションを選んで無効化
    2.適当なニューロンを作って追加
    3. 2をつなぐためのコネクションを2つ作って追加
    いじょうです
    """
    agent = copy.deepcopy(a)
    agent.revert_to_initial_condition()

    if(agent.num_of_active_connection >= CONNECTION_NUM_UPPER_LIMIT):
        return agent
    if(agent.num_of_normal_neuron + agent.num_of_modulation_neuron >= NEURON_NUM_UPPER_LIMIT):
        return agent

    target_no = random.randint(0, len(agent.connections) -1)
    target_input = agent.connections[target_no].input_id
    target_output = agent.connections[target_no].output_id

    normal_allowance = NORMAL_NUM_UPPER_LIMIT - agent.num_of_normal_neuron
    modulation_allowance = MODULATION_NUM_UPPER_LIMIT - agent.num_of_modulation_neuron
    normal_allowance = 0 if normal_allowance < 0 else normal_allowance
    modulation_allowance = 0 if modulation_allowance < 0 else modulation_allowance
    if (normal_allowance == 0 and modulation_allowance == 0):
        return agent

    t = random.choices(['n','m'],[normal_allowance,modulation_allowance])[0]
    if t=='n':
        agent.neurons.append(Neuron(NeuronType.NORMAL))
    elif t=='m':
        agent.neurons.append(Neuron(NeuronType.MODULATION))

    agent.connections[target_no].is_valid = False
    agent.connections.append(Connetion( global_max_connection_id +1, target_input, len(agent.neurons) -1) )
    agent.connections.append(Connetion( global_max_connection_id +2, len(agent.neurons) -1,target_output) )
    print("新しいidのニューロンが追加されました")
    print("idは",global_max_connection_id+1,"と",global_max_connection_id+2)
    return agent
    
def give_dispersion(a, sigma = 0.1, rate = 0.1):

    agent = copy.deepcopy(a)
    agent.revert_to_initial_condition()

    for i in range(len(agent.neurons)):
        if random.random() < rate:
            agent.neurons[i].bias += random.normalvariate(0, sigma)
            if agent.neurons[i].bias < BIAS_LOWER_LIMIT:
                agent.neurons[i].bias = BIAS_LOWER_LIMIT
            elif agent.neurons[i].bias > BIAS_UPPER_LIMIT:
                agent.neurons[i].bias = BIAS_UPPER_LIMIT

    for i in range(len(agent.connections)):
        if random.random() < rate:
            agent.connections[i].weight += random.normalvariate(0, sigma)
            if agent.connections[i].weight < WEIGHT_LOWER_LIMIT:
                agent.connections[i].weight = WEIGHT_LOWER_LIMIT
            elif agent.connections[i].weight > WEIGHT_UPPER_LIMIT:
                agent.connections[i].weight = WEIGHT_UPPER_LIMIT

    return agent

if __name__=='__main__':
    b=ExHebbianNetwork()
    b.show_network()
    #b=mutate_add_connection(b)
    #b=mutate_add_connection(b)
    b=mutate_add_connection(b)
    b.show_network()
    b=mutate_add_connection(b)
    b.show_network()
    b=mutate_disable_connection(b)
    b.show_network()
    b=mutate_disable_connection(b)
    b.show_network()
    b=mutate_disable_connection(b)
    b.show_network()

    #o1=crossover(a,0,b,0)
    #o2=crossover(a,0,b,0)
    #o3=crossover(o1,0,o2,0)
    #o1.show_network()
    #o2.show_network()
    #o3.show_network()
