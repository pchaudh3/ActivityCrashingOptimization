
import create_final_optimization_problem
import NetworkGenerator
import branch_bound_impl
import random
import pickle 
from NetworkGenerator import GenerateInfrastructure
import penalty_function_helper


def optimize():

    #To change this location update below
    out_location="C:/Users/Priyanka/Desktop/Optimization Project/RUN1/"
    #name for project network pickle file
    project_file_name="ProjectNetwork"

    #name for scenario pickle file
    scenarios_file_name="Scenarios"

    #Input no of nodes in network(excluding start and stop)
    no_of_nodes=10

    #Input no of layers in network(excluding start and stop layer)
    no_of_layers=3   

    #number of scenarios needed
    no_of_scenarios=15

    #Generating probabilities for beta Distributions
    dic={}
    for i in range(1,no_of_nodes+1):        
        value=[]
        value.append(random.uniform(0, 1))
        value.append(random.uniform(0, 1))
        value.append(random.uniform(0, 1))
        dic[i]=value
        
    GenerateInfrastructure.generate_infrastructure(no_of_nodes,no_of_layers,dic,no_of_scenarios,out_location,project_file_name,scenarios_file_name)
    
    project_network_file = open(out_location+project_file_name+".pkl", 'rb')
    project_network = pickle.load(project_network_file)
    project_network_file.close()

    scenario_file = open(out_location+scenarios_file_name+".pkl", 'rb')
    scenarios = pickle.load(scenario_file)
    scenario_file.close()

    crashtime=[0,0,40,30,50,0,0,0,60,10,0,0]
    crashcost=[0,0,20,60,30,0,0,0,60,40,0,0]    

    t_init,t_final=penalty_function_helper.get_t_init_final(project_network,out_location)
    
    branch_bound_impl.branch_bound_algorithm(project_network,scenarios,crashtime,crashcost,t_init,t_final,out_location)
    
#calling itself
optimize()