# mod-neat

This package will be python package which can make easier to implement second-order-learning with neuromodulation.  
We use NEAT algorithm for evolution of neural network.  


このpythonパッケージは，修飾ニューロンを用いた二次学習の進化の実装に役立つパッケージになる予定です．  
ニューラルネットワークの進化にはNEATアルゴリズムを用います． 

# usage (concept)  
```python
import modpy  
agent = modpy.agent( #create agent
  input_num = 10, 
  output_num = 10, 
  neuron_num = 10,
  normal_num = 10,
  modulatory_num = 10,
  neuron_num_upper_limit = 100
  neuron_num_lower_limit = 20
  normal_num_upper_limit = 100
  modulatory_num_upper_limit = 0
  eta = 0.1
  )
#using agent
output = agent.get_output([0,1,0,1,..0]) 

#evolution
new_agent = agentA.create_offspring(agentB)

```
みたいな？
