# modneat

This package will be python package which can make easier to implement second-order-learning with neuromodulation.  
We use NEAT algorithm for evolution of neural network.  


このpythonパッケージは，修飾ニューロンを用いた二次学習の進化の実装に役立つパッケージになる予定です．  
ニューラルネットワークの進化にはNEATアルゴリズムを用います． 

# environment  
- Python3  
- networkx  
- pygraphviz  

# install  
on the your project folder...
```
$ git clone https://github.com/katomasahiro10/modneat/modneat
```

# configuration  
To configure parameters of modneat, please edit this file: `/modneat/modneat_settings`  

# usage (concept)  
```python

# import package
from modneat import agents

# create agents. give type and number of agents as argments.
agents = agents.Agents('NeuralNetwork',100)
agents = agents.Agents('HebbianNetwork',100)
agents = agents.Agents('ExHebbianNetwork',100)

# agents is list of agent.
# In this case, agents[0]~agents[99] are each individual.
# Each individual has methods as follows.
agents[0].get_output([0,1]) # doesn't update their weight
agents[0].get_output_with_update([0,1]) # update their weight using Hebb's rule and modulation neurons
agents[0].show_network('save_file_path') 

# set fitness of each individual
agents[0].fitness = 0.1

# In addition, each individual has these instance variables
agents[0].epsiron  # learning rate
agents[0].A, agents[0].B, agents[0].C, agents[0].D  # evolutionaly variables(only in 'ExHebbianNetwork' agent)

# Evolution following fitness value of each individual.
agents = agents.evolution(elite_num = 4, mutate_prob = 0.05, sigma = 0.1)

# Agents class has these properties
agents.max_fitness
agents.min_fitness
agents.average_fitness
```  

`/xor.py` shows more concrete example of using this package.
