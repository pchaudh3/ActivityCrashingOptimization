"""
# -*- coding: utf-8 -*-
Created on August 2 2018

@author: Priyanka Chaudhary
"""

import gurobipy as gp
import time
import numpy as np
import networkx as nx
import random

def get_beta_distribution(activity_dic):
    distribution_dic={}
    most_likely_duration=[]
    #for start activity
    most_likely_duration.append(0)
    pessimistic_duration=[]
    #for start activity
    pessimistic_duration.append(0)
    for key,value in activity_dic.items():
        arch=key
        optimistic_value=value[0]
        optimistic_mlikely_diff=value[1]
        pessimestic_mlikely_diff=value[2]
        print("Node:"+str(arch))
        print("Probability Used for generating distribution:",optimistic_value,optimistic_mlikely_diff,pessimestic_mlikely_diff)
        #Choosing optimistic,optimistic_mlikely_diff,pessimestic_mlikely_diff from geometric distributions
        o_value = np.random.geometric(p=optimistic_value)
        o_ml_diff=np.random.geometric(p=optimistic_mlikely_diff)
        p_ml_diff=np.random.geometric(p=pessimestic_mlikely_diff)

        #Calculating most likely and pessimistic time for activity based on above sampled values        
        ml_value=o_value+o_ml_diff
        most_likely_duration.append(ml_value)        
        p_value=ml_value+p_ml_diff
        pessimistic_duration.append(p_value)
        
    #for end activity
    most_likely_duration.append(0)
    #for end activity
    pessimistic_duration.append(0)

    
    return most_likely_duration,pessimistic_duration
   

def get_project_completion_time(project_network,scenario,outlocation):

    no_of_nodes=len(project_network.nodes)

    # Setting up the Master problem
    master = gp.Model("OptimizationProblem")
    master.params.OutputFlag = 0 # Supress logging
    master.params.Thread = 0 # Single thread execution of solver

       
    xi={}
    #variables for weather crashing activity is set or not
    for i in range(no_of_nodes):
        xi[i] = master.addVar(vtype=gp.GRB.BINARY, name="x"+str(i))
    
    
    #variables for calculating start time of project activities
    si={}
    for i in range(no_of_nodes):
        si[i]=master.addVar(vtype=gp.GRB.INTEGER, name="s"+str(i))    
    
    # Update model to integrate new variables  
    master.update()

    #constraints to calculate start time of project activities based on which crashing activities
    #have been set in the subproblem
    si_constr={}
    for node in project_network.nodes:
        successors=project_network.successors(node)
        for successor in successors: 
            print("Adding constraint for:",successor)           
            master.addConstr(si[int(successor)]>=si[int(node)]+scenario[int(node)], name="start time for node"+str(successor))

    #Debug
    master.write(outlocation+"penaltymodel.lp")
    
    #Optimization function    
    master.setObjective(si[no_of_nodes-1],gp.GRB.MINIMIZE)
    master.optimize()

    return master.getAttr('ObjVal')


def get_t_init_final(project_network,outlocation):

    no_of_nodes=len(project_network.nodes)-2
    dic={}
    for i in range(1,no_of_nodes+1):        
        value=[]
        value.append(random.uniform(0, 1))
        value.append(random.uniform(0, 1))
        value.append(random.uniform(0, 1))
        dic[i]=value
    
    most_likely,pessimistic=get_beta_distribution(dic)

    most_likely_time=get_project_completion_time(project_network,most_likely,outlocation)
    pessimistic_time=get_project_completion_time(project_network,pessimistic,outlocation)

    return most_likely_time,pessimistic_time





