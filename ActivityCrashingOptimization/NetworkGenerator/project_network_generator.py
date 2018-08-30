"""
# -*- coding: utf-8 -*-
Created on July 3 2018

@author: Priyanka Chaudhary
"""

import networkx as nx
from network_skeleton_generator import generate_network_skeleton
import matplotlib.pyplot as plt
import numpy as np
import pickle
import random
import math
import logging

def create_connected_graph(num_nodes,number_layers,out_location,out_name,logger):
       
    #get a skeleton graph with given no of nodes and layers
    edges=generate_network_skeleton(num_nodes,number_layers,logger)

    #Create a directed graph with skeleton edges
    G = nx.DiGraph()
    G.add_edges_from(edges)    

    ####Randomly add edges from lower nodes to higher nodes
    edgelist=[]
    for i in range(int(math.floor(0.50*len(edges)))):
        edge=random.sample(G.nodes(), 2)
        if edge[0]<edge[1]:
            edgelist.append((edge[0],edge[1]))    
    logger.debug("Randomly Added edges:%s",edgelist)    
    G.add_edges_from(edgelist)

    ###Check connectivity
    g = G.to_undirected()    
    logger.info("isCreated Graph Connected:%s",nx.is_connected(g))
    

    ####Plot the graph
    #plt.title('draw_networkx')
    #pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
    #nx.draw(G, pos, with_labels=True, arrows=False)
    #plt.show()

    #Save generated graph with transmission nodes and arcs to file
    file_name = out_location + out_name + '.pkl'
    output_file = open(file_name, 'wb+')
    pickle.dump(G, output_file)
    plt.close()
    output_file.close()



