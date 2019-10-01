import copy
from nn import *

def crossover(agent_A, fitness_A, agent_B, fitness_B):
    A = copy.deepcopy(agent_A)
    B = copy.deepcopy(agent_B)

    offspring = copy.deepcopy(A)
    offspring.neurons = []
    offspring.connections = []

    for a in range(len(A.connections)):
        for b in range(len(B.connections)):
            if A.connections[a] != None and B.connections[b] != None and A.connections[a].connection_id == B.connections[b].connection_id:
                offspring.connections.append(copy.deepcopy( random.choice([ A.connections[a],B.connections[b] ]) ) )
                A.connections[a] = None
                B.connections[b] = None
                print("一致した")
                break
    
    A.connections = [x for x in A.connections if x != None]
    B.connections = [x for x in B.connections if x != None]
    print(len(A.connections),len(B.connections),len(offspring.connections))
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

    # evolution_param
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

def mutate_add_connection(a):
    agent = copy.deepcopy(a)
    input_id = random.randint(0, len(agent.neurons) -1)
    output_id = random.randint(INPUT_NUM, len(agent.neurons) -1)
    connection_id = agent.max_connection_id + 1
    agent.connections.append(Connetion(connection_id, input_id, output_id ))
    return agent

def mutate_disable_connection(a):
    pass

def mutate_add_neuron(a):
    """
    1.なんか適当なコネクションを選んで無効化
    2.適当なニューロンを作って追加
    3. 2をつなぐためのコネクションを2つ作って追加
    いじょうです
    """
    agent = copy.deepcopy(a)
    target_no = random.randint(0, len(agent.connections))
    target_input = agent.connections[target_no].input_id
    target_output = agent.connections[target_no].output_id
    print("ti:",target_input,"to:",target_output)

    normal_allowance = NORMAL_NUM_UPPER_LIMIT - agent.num_of_normal_neuron
    modulation_allowance = MODULATION_NUM_UPPER_LIMIT - agent.num_of_modulation_neuron
    if (normal_allowance == 0 and modulation_allowance == 0):
        print("ニューロン追加しませーん")
        return agent

    t = random.choices(['n','m'],[normal_allowance,modulation_allowance])[0]
    print("ニューロン追加しまーす")
    if t=='n':
        print(agent.num_of_normal_neuron,agent.num_of_modulation_neuron)
        agent.neurons.append(Neuron(NeuronType.NORMAL))
        print("ノーマル追加")
        print(agent.num_of_normal_neuron,agent.num_of_modulation_neuron)
    elif t=='m':
        print(agent.num_of_normal_neuron,agent.num_of_modulation_neuron)
        agent.neurons.append(Neuron(NeuronType.MODULATION))
        print("mod追加")
        print(agent.num_of_normal_neuron,agent.num_of_modulation_neuron)

    agent.connections[target_no].is_valid = False
    print(len(agent.neurons),"個のニューロンがある")
    agent.connections.append(Connetion( agent.max_connection_id+1, target_input, len(agent.neurons) -1) )
    agent.connections.append(Connetion( agent.max_connection_id+1, len(agent.neurons) -1,target_output) )
    return agent


if __name__=='__main__':
    b=ExHebbianNetwork()
    b.show_network()
    #b=mutate_add_connection(b)
    #b=mutate_add_connection(b)
    b=mutate_add_neuron(b)
    b.show_network()
    b=mutate_add_neuron(b)
    b.show_network()
    #o1=crossover(a,0,b,0)
    #o2=crossover(a,0,b,0)
    #o3=crossover(o1,0,o2,0)
    #o1.show_network()
    #o2.show_network()
    #o3.show_network()
