"""
# -*- coding: utf-8 -*-
Created on July 2 2018

@author: Priyanka Chaudhary
"""

import numpy as np
import random 
import scipy
import pickle


def generate_scenarios(num_activities,num_scenarios,correlation_matrix,activity_beta_distribution_list,out_location,out_name,logger):
    mean=np.zeros( num_activities )
    B1 = np.random.multivariate_normal(mean, correlation_matrix, num_scenarios)
    B2 = scipy.stats.norm.cdf(B1)
    S=np.array(())
    k_list=[]
    if(num_activities==len(activity_beta_distribution_list)):
        for i in range(num_activities):
            k=np.array(activity_beta_distribution_list[i+1].ppf(B2[:,i])).astype(int)
            k_list.append(k)
    else:
        logger.exception("Something wrong in GenerateScenarios")

    #duration for start node
    S=np.zeros(num_scenarios)

    #duration for end node
    k_list.append(np.zeros(num_scenarios))

    for k in k_list:
        S = np.column_stack((S,k))
        
    #Save generated scenarios in a file
    file_name = out_location + out_name + '.pkl'
    output_file = open(file_name, 'wb+')
    pickle.dump(S, output_file)     
    output_file.close()

    return S
        