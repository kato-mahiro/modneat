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
    return offspring

def mutate(agent_A):
    pass

if __name__=='__main__':
    a=NeuralNetwork()
    a.show_network()
    b=NeuralNetwork()
    b.show_network()
    o=crossover(a,0,b,0)
    o.show_network()
