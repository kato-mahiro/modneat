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
$ git clone https://github.com/katomasahiro10/modneat
```

# configuration  
To configure parameters of modneat, please edit this file: `./modneat/modneat_settings`  

# usage (concept)  
```python

# import package
from modneat import modneat_agents

# create agents. give type and number of agents as argments.
agents = modneat_agents.Agents('NeuralNetwork',100)
agents = modneat_agents.Agents('HebbianNetwork',100)
agents = modneat_agents.Agents('ExHebbianNetwork',100)

# agents is list of agent.
# In this case, a[0]~a[99] are each individual.
# Each individual has methods as follows.
a[0].get_output([0,1])
a[0].get_output_with_update([0,1])
a[0].show_network('save_file_path')

# set fitness of each individual
a[0].fitness = 0.1

# Evolution using each fitness value.
agents = agents.evolution(elite_num = 4, mutate_prob = 0.05, sigma = 0.1)

# Agents class has these properties
agents.max_fitness
agents.min_fitness
agents.average_fitness
```
