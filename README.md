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

# create agents
agents = modneat_agents.Agents('NeuralNetwork',100)
agents = modneat_agents.Agents('HebbianNetwork',100)
agents = modneat_agents.Agents('ExHebbianNetwork',100)
```
