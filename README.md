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
at your project folder...
```
$ git clone https://github.com/katomasahiro10/modneat
```

# usage (concept)  
```python
"""
import package
"""
import modneat

"""
Create agent and use it
"""
agent = modneat.nn.NeuralNetwork()    # create agent which doesn't learn
agent = modneat.nn.HebbianNetwork()   # which learn by Hebb's rule
agent = modneat.nn.ExHebbianNetwork() # which learn by Expanded Hebb's rule

output = agent.get_output( [1,0,1,0] ) # get output and update weight
agent.show_network()                   # visualize neural network

"""
Evolution of agents
"""
next_agent = modneat.evolution.crossover( agent_a, 0.1, agent_b, 0.2) # get next_generation using neat algorithm. 2nd and 4th argment represents each fitness.
# about mutation
agent = modneat.evolution.mutate_add_connection(agent)
agent = modneat.evolution.mutate_disable_connection(agent)
agent = modneat.evolution.mutate_add_neuron(agent)

```
