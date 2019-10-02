# modneat

This package will be python package which can make easier to implement second-order-learning with neuromodulation.  
We use NEAT algorithm for evolution of neural network.  


このpythonパッケージは，修飾ニューロンを用いた二次学習の進化の実装に役立つパッケージになる予定です．  
ニューラルネットワークの進化にはNEATアルゴリズムを用います． 

# environment  
Python3
networkx
pygraphviz

# usage (concept)  
```python

"""
Create agent and use it
"""
import mod-neat
agent = mod-neat.nn.NeuralNetwork()    # create agent
output = agent.get_output( [1,0,1,0] ) # get output and update weight
agent.show_network()                   # visualize neural network

"""
Evolution of agents
"""
next_agent = mod-neat.evolution.neat( agent_a, 0.1, agent_b, 0.2) # get next_generation using neat algorithm
```
みたいな？
