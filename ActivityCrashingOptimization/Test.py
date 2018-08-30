
import networkx as nx
import matplotlib.pyplot as plt
#from keras.layers import Dense
from keras.models import Sequential
from networkx import *
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

#Trying Keras
#model = sequential()
#model.add(dense(1, input_dim=1))
#model.add(dense(3))


#svg(model_to_dot(model).create(prog='dot', format='svg'))


###Create a empty directed Graph
#G=nx.DiGraph()
#G.add_node(1)
#nx.draw(G)
#plt.show()

###Checking type of Graph
#print(type(G))

###Creating a multi dimrected graph:Multi means one node can be connected to multiples nodes
#D=nx.MultiDiGraph()

#k=nx.ladder_graph(5,create_using=None)
#nx.draw(k)
#plt.show()


####degree sequence graph
#sequence = nx.random_powerlaw_tree_sequence(10, tries=500)
#G = nx.configuration_model(sequence)
#G = nx.Graph(G)
#print("length",len(G))
#G.remove_edges_from(nx.selfloop_edges(G))
#nx.draw(G)
#plt.show()

#Testing manual
D=nx.gnp_random_graph(12,0.2,1,True)
nx.draw(D)
plt.show()
#D.add_edge(1,2)
#D.add_edge(1,3)
#D.add_edge(2,4)
#D.add_edge(3,5)
#D.add_edge(4,6)
#D.add_edge(5,6)
#pos =graphviz_layout(D, prog='dot')
#nx.draw(D, pos, with_labels=False, arrows=True)

plt.show()


####Testing 





