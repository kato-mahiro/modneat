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
    pass

if __name__=='__main__':
    b=ExHebbianNetwork()
    b.show_network()
    b=mutate_add_connection(b)
    b=mutate_add_connection(b)
    b.show_network()
    #o1=crossover(a,0,b,0)
    #o2=crossover(a,0,b,0)
    #o3=crossover(o1,0,o2,0)
    #o1.show_network()
    #o2.show_network()
    #o3.show_network()
