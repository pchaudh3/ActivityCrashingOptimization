import logging
from project_network_generator import create_connected_graph 
from generate_correlation_matrix import generate_correlation_matrix
from generate_beta_distribution_for_activities import get_beta_distribution
from generate_scenarios import generate_scenarios

def generate_infrastructure(no_of_nodes,no_of_layers,dic,no_of_scenarios,out_location,project_file_name,scenarios_file_name):

    logger = logging.getLogger("NetworkGenerator.generate_infrastructure")  
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)    
    logger.addHandler(logging.StreamHandler())    

    #Generating the network
    create_connected_graph(no_of_nodes,no_of_layers,out_location,project_file_name,logger)

    #Generating the correlation Matrix
    P=generate_correlation_matrix(no_of_nodes,logger)   

    distribution_dic,most_likely_duration,pessimistic_duration=get_beta_distribution(dic,logger)

    #Generate Scenarios
    S=generate_scenarios(no_of_nodes,no_of_scenarios,P,distribution_dic,out_location,scenarios_file_name,logger)
    print("Scenarios:")
    print(S)

    return most_likely_duration,pessimistic_duration
     