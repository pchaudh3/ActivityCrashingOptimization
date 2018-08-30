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
import math


def create_final_optimization_problem(project_network,scenario,crashtime,crashcost,subproblem,t_init,t_final,outlocation,logger):

    no_of_nodes=len(project_network.nodes)

    #finding intervals for the penalty
    d=(t_final - t_init)/20.0

    #intervals
    t=[]
    for j in range(20):
        t.append(t_init + (j*d))

    # Setting up the Master problem
    master = gp.Model("FinalOptimizationProblem")
    master.params.OutputFlag = 0 # Supress logging
    master.params.Thread = 0 # Single thread execution of solver

    #variables
    variables=subproblem.get("variables")
    
    xi={}
    #variables for weather crashing activity is set or not
    for i in range(len(variables)):
        xi[i] = master.addVar(vtype=gp.GRB.BINARY, name="x"+str(i))
    
    
    #variables for calculating start time of project activities
    si={}
    for i in range(no_of_nodes):
        si[i]=master.addVar(vtype=gp.GRB.INTEGER, name="s"+str(i))

    #variable for penalty function
    z={}
    z['z']=master.addVar(vtype=gp.GRB.CONTINUOUS,name="z")
    
    #variable which will be used to calculate penalty function
    w={}
    w['w']=master.addVar(vtype=gp.GRB.CONTINUOUS,name="w")
    
    # Update model to integrate new variables  
    master.update()

    #Debug
    print(master.getVars())

    #Add constraints
    constraints=subproblem.get("constraints")

    #constraints for crashing activity that are set in sub-problem while partitioning
    xi_constr={}
    for i,j in constraints.items():
        xi_constr[i]=master.addConstr(xi[i]==j,name="c"+str(i))

    #constraints to calculate start time of project activities based on which crashing activities
    #have been set in the subproblem
    si_constr={}
    for node in project_network.nodes:
        successors=project_network.successors(node)
        for successor in successors: 
            logger.debug("Adding constraint for:%s",successor)           
            master.addConstr(si[int(successor)]>=si[int(node)]+scenario[int(node)]-xi[int(node)]*((crashtime[int(node)]*scenario[int(node)])/100), name="start time for node"+str(successor))

    #Adding the non-negativity constraints
    master.addConstr(z['z']>0)
    
    #constraints for penalty calculation    
    for j in range(20):
        f1=(1.5**(t[j]-t_init))-1
        f2=math.log((1.5**(t[j]-t_init)), 2)
        master.addConstr(z['z']>=f1 + f2*(w['w']-t[j]))

    #Debug
    master.write(outlocation+"model.lp")
    
    #Optimization function    
    master.setObjective(z['z']+gp.quicksum(xi[i]*crashcost[i] for i in range(no_of_nodes)),gp.GRB.MINIMIZE)

    return master


    