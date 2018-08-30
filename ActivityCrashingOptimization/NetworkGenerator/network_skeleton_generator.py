"""
# -*- coding: utf-8 -*-
Created on July 2 2018

@author: Priyanka Chaudhary
"""


import numpy
import math
import logging

#Function takes in no of nodes excluding Start and End node and no of internal layers in the network
def generate_network_skeleton(number_of_nodes, number_of_layers,logger):
    #Number of nodes in each layer
    num_nodes_per_layer=math.floor(number_of_nodes/number_of_layers)
    #Number of nodes in last layer if number_of_nodes is not a multiple of number_of_layers
    num_nodes_last_layer=number_of_nodes%number_of_layers
    #Creating a list that will hold list of nodes in each layer,Eg [[1],[2,3,4],[4,5,6],[7]]
    #index in he list will denote layer number
    nodes_per_layer_list=[]
    #NodeID 
    nodeId=0 

    ###Adding node 0(Start) to list ###
    nodes_per_layer_list.append([nodeId])
    nodeId=nodeId+1

    ###Arranging nodes in layers
    for i in range(number_of_layers):
        list=[]
        for j in range(int(num_nodes_per_layer)):
            list.append(nodeId)
            nodeId=nodeId+1
        nodes_per_layer_list.append(list)

    ###Adding last layer if number_of_nodes is not a multiple of number_of_layers
    if(num_nodes_last_layer>0):
        list=[]
        for i in range(num_nodes_last_layer):       
            list.append(nodeId)
            nodeId += 1
        nodes_per_layer_list.append(list) 

    ###Adding End node layer
    nodes_per_layer_list.append([nodeId])

    ###DEBUG:printing the layered structure of graph
    logger.info("nodes_per_layer_list:%s",nodes_per_layer_list)

    ####Creating equal number of flattened partitions and creating Edges between each subsequent layer#####    
    all_edges=[]
    for i in range(len(nodes_per_layer_list)-1):
        layern=nodes_per_layer_list[i]
        layernext=nodes_per_layer_list[i+1]
        if(len(layern)==len(layernext)):            
            partitions_layer = numpy.array_split(numpy.array(layern),len(layern))
            partitions_layernext = numpy.array_split(numpy.array(layernext),len(layernext))            
        elif(len(layern)<len(layernext)):            
            partitions_layer = numpy.array_split(numpy.array(layern),len(layern))
            partitions_layernext = numpy.array_split(numpy.array(layernext),len(layern))
            partitions_layer,partitions_layernext=FlattenPartition(partitions_layer,partitions_layernext)            
        else:
            partitions_layer= numpy.array_split(numpy.array(layern),len(layernext))
            partitions_layernext = numpy.array_split(numpy.array(layernext),len(layernext))
            partitions_layer,partitions_layernext=FlattenPartition(partitions_layer,partitions_layernext)

        for i in range(len(partitions_layer)):
            partition_from_layer=partitions_layer[i]
            partition_from_layernext=partitions_layernext[i]
            all_edges=createEdges(partition_from_layer,partition_from_layernext,all_edges,logger)

    logger.info("AllEdges:%s",all_edges)        
    
    return all_edges
                

####Function that takes in two layers with equal number of partitions and flattens the corresponding 
####partitions in the two inputed layers such that the partitions have equal no of nodes corresponding to 
####partition in next layer 
def FlattenPartition(partitions_Layer1,partitions_Layer2):
    l1=len(partitions_Layer1)
    l2=len(partitions_Layer2)
    if(l1==l2):
        for i in range(l1):
            partitionfromlayer1=partitions_Layer1[i]            
            partitionfromlayer2=partitions_Layer2[i]            
            if(len(partitionfromlayer1)<len(partitionfromlayer2)):
                partitionfromlayer1=numpy.repeat(partitionfromlayer1,len(partitionfromlayer2)).ravel().tolist()
                partitions_Layer1[i]=partitionfromlayer1
            elif(len(partitionfromlayer1)>len(partitionfromlayer2)):
                partitionfromlayer2=numpy.repeat(partitionfromlayer2,len(partitionfromlayer1)).ravel().tolist()
                partitions_Layer2[i]=partitionfromlayer2             
    else:
        logger.exception("Something Wrong in FlattenPartition")

    return(partitions_Layer1,partitions_Layer2)
    
   
#Function that takes two equal partitioned layers as input and creates edges between corresponding 
#nodes of the layers
def createEdges(Layer1,Layer2,all_edges,logger):    
    if(len(Layer1)==len(Layer2)):
        for i in range(len(Layer1)):
            logger.debug("Layer1node:%s",Layer1[i])             
            logger.debug("Layer2node:%s",Layer2[i])            
            edge=(Layer1[i],Layer2[i])
            logger.debug("Edge:%s",edge)
            all_edges.append(edge)    
    else:
        logger.exception("Error in createEdge:Partition not equal")
    return all_edges








