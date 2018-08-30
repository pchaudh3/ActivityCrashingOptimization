
"""
# -*- coding: utf-8 -*-
Created on August 2 2018

@author: Priyanka Chaudhary
"""
import gurobipy as gp
import time
import numpy as np
import networkx as nx
import pickle
import time
import logging 
import copy
from create_final_optimization_problem import create_final_optimization_problem 

def branch_bound_algorithm(project_network,scenarios,crashtime,crashcost,t_init,t_final,outlocation):

    logger = logging.getLogger("branch_bound_impl.branch_bound_algorithm")  
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)    
    logger.addHandler(logging.FileHandler(filename=outlocation+"brachboundlog", delay=False))
        
    nodes=project_network.nodes
    no_of_nodes=len(nodes)

    #This list will contain all the leaf sub-problems of the partitioned tree.
    partition_list=[]
    
    #we dont need it since final bound estimation depends on a seperate logic :Discuss with prof
    #global_objective_function_value
    
   
    #Step 1:Initialization
    subproblem={}

    #Add variables
    variable_list=[]
    for node in nodes:
        variable_list.append("x"+str(node))

    subproblem['variables']=variable_list
    subproblem['constraints']={}
    subproblem['recordset']=True

    subproblem['lowerbound']=estimate_bounds(project_network,scenarios,crashtime,crashcost,subproblem,t_init,t_final,outlocation,logger)
    subproblem['no_of_scenerios_worked_on']=len(scenarios)
    ##global_lower_bound=subproblem['lowerbound']   
       
    partition_list.append(subproblem)

    #Step2:Partitioning
    k=1
    while True:#Todo: Add stopping criteria    
        for subproblem in partition_list:
            if(subproblem.get('recordset',False)==True and subproblem.get('singleton',False)==False):
                #Get constraints List for subproblem
	            #create two subproblems with below added constraints
                constraints_dic=subproblem.get('constraints')
                variable_list=subproblem.get('variables')
                index_of_last_constraint = len(constraints_dic)-1
                if(index_of_last_constraint<no_of_nodes):
                    subproblem1=copy.deepcopy(subproblem)
                    subproblem1['recordset']=False
                    subproblem2=copy.deepcopy(subproblem)
                    subproblem2['recordset']=False
                    subproblem1.get('constraints',{})[index_of_last_constraint+1]=0
                    subproblem2.get('constraints',{})[index_of_last_constraint+1]=1               
                    partition_list.remove(subproblem )
                    partition_list.extend([subproblem1, subproblem2])                	
                else:
                    subproblem['singleton']=True
        
                min_obj_function_value_per_subproblem=[]
                for subproblem in partition_list:
                    min_obj_function_value_per_subproblem.append(estimate_bounds(project_network,scenarios,crashtime,crashcost,subproblem,t_init,t_final,outlocation,logger))
            
                #Setting the record set
                index=min_obj_function_value_per_subproblem.index(min(min_obj_function_value_per_subproblem))
                subproblem= partition_list[index]
                subproblem['recordset']=True

    ###################################################################################################
    # Final Bound Estimation
    # This function Estimate Bounds on Each Partition in Partition Set after Partitioning Set is over. 
    # It will call optimizer on all partition for each scenario and store the minimum function value for
    # each scenario.Then it will take average of minimum function value across all scenarios and that 
    # will be our optimal objective function value.
    ####################################################################################################

    # List that will contain minimum function value for each scenario
    min_function_value_each_scenerio=[]
    for scenario in scenarios:
        #List that will contain min function value(returned by optimizer) for each partition
        function_value_per_scenerio_per_partition=[]
        for subproblem in partition_list:  
            function_value_per_scenerio_per_partition.append(estimate_bounds(project_network,scenarios,crashtime,crashcost,subproblem,t_init,t_final,outlocation,logger))
        min_function_value_per_scenerio.append(min(function_value_per_scenerio_per_partition))
    optimal_value=sum(min_function_value_per_scenerio)/length(min_function_value_per_scenerio)


def estimate_bounds(project_network,scenarios,crashtime,crashcost,subproblem,t_init,t_final,outlocation,logger):
        obj_function_value_each_scenerio=[]
        for scenario in scenarios:
               logger.info("Begin working on scenario:Start")
               ##Create optimization problem for input Sub-problem
               logger.info("Creating the model:Start")
               model=create_final_optimization_problem(project_network,scenario,crashtime,crashcost,subproblem,t_init,t_final,outlocation,logger) 
               logger.info("Creating the model:End")
               logger.info("Running the model:Start")
               model.optimize()
               logger.info("Running the model:End")
               min_obj_func_value=model.getAttr('ObjVal')
               model.write(outlocation+"solution.sol")
               obj_function_value_each_scenerio.append(min_obj_func_value)
               logger.info("Begin working on scenario:End")
        min_obj_function_value= sum(obj_function_value_each_scenerio)/len(scenarios)

        return min_obj_function_value





                



