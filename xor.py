#usage sample

import agents

inputs = [[0,0],[1,0],[0,1],[1,1]]
outputs = [0,1,1,0]

agents = agents.Agents('NeuralNetwork',10)

for g in range(4000):
    average_fitness=0
    for n in range(10):
        error = 0.0
        error += (agents[n].get_output_without_update(inputs[0])[0] - outputs[0]) ** 2
        error += (agents[n].get_output_without_update(inputs[1])[0] - outputs[1]) ** 2
        error += (agents[n].get_output_without_update(inputs[2])[0] - outputs[2]) ** 2
        error += (agents[n].get_output_without_update(inputs[3])[0] - outputs[3]) ** 2
        agents[n].fitness = error *-1
        average_fitness += agents[n].fitness
        #print(agents[n].fitness)
    if(g%10 == 0):
        print(average_fitness/10)
    agents = agents.evolution(elite_num = 2, mutate_prob = 0.01, sigma = 0.1)

print(agents[0].get_output_without_update(inputs[0]))
print(agents[0].get_output_without_update(inputs[1]))
print(agents[0].get_output_without_update(inputs[2]))
print(agents[0].get_output_without_update(inputs[3]))
