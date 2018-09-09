import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import random

#get_beta_distribution(activity_set,optimistic_value,optimistic_mlikely_diff,pessimestic_mlikely_diff,logger)
def get_beta_distribution(activity_dic,logger):
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
        logger.debug("Node:%s",arch)
        logger.debug("Probability Used for generating distribution:%s,%s,%s",optimistic_value,optimistic_mlikely_diff,pessimestic_mlikely_diff)
        #Choosing optimistic,optimistic_mlikely_diff,pessimestic_mlikely_diff from geometric distributions
        o_value = np.random.geometric(p=optimistic_value)
        o_ml_diff=np.random.geometric(p=optimistic_mlikely_diff)
        p_ml_diff=np.random.geometric(p=pessimestic_mlikely_diff)
        logger.debug("Activity:%s:optimistic_value:%s,o_ml_diff:%s,p_ml_diff:%s",key,o_value,o_ml_diff,p_ml_diff)
        #Calculating most likely and pessimistic time for activity based on above sampled values 
        i=random.randint(1,10)       
        ml_value=o_value+i*o_ml_diff
        most_likely_duration.append(ml_value) 
        i=random.randint(1,10)   
        p_value=ml_value+i*p_ml_diff
        pessimistic_duration.append(p_value)

        logger.debug("Activity:%s:optimistic_value:%s,most_likely_value:%s,pessimistic_value:%s",key,o_value,ml_value,p_value)

        a=o_value
        m=ml_value
        b=p_value

        #Calculating alpha and beta from PERT[o_value,ml_value,p_value] calculated above
        #alpha=(2*(b+4*m-5*a)/3*(b-a))*(1+4*((m-a)*(b-m)/(b-a)**2))        
        #bet=(2*(5*b-4*m-a)/3*(b-a))*(1+4*((m-a)*(b-m)/(b-a)**2))

        alpha=1 +  4*(m-a)/(b-a)
        bet=1 + 4*(b-m)/(b-a)

        logger.debug("alpha:%s,beta:%s",alpha,bet)
        
        #Calculate pert beta distribution using alpha and bet
        D_ij = beta(alpha, bet,loc=a, scale=b-a)
        logger.debug("Mean:%s",D_ij.mean())
        logger.debug("Var:%s",D_ij.var())
        

        distribution_dic[arch]=D_ij

    #for end activity
    most_likely_duration.append(0)
    #for end activity
    pessimistic_duration.append(0)


    return distribution_dic,most_likely_duration,pessimistic_duration


