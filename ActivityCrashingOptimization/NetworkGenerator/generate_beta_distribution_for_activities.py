import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt

#get_beta_distribution(activity_set,optimistic_value,optimistic_mlikely_diff,pessimestic_mlikely_diff,logger)
def get_beta_distribution(activity_dic,logger):
    distribution_dic={}
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

        #Calculating most likely and pessimistic time for activity based on above sampled values        
        ml_value=o_value+o_ml_diff
        p_value=ml_value+p_ml_diff

        logger.debug("optimistic_value:%s,most_likely_value:%s,pessimistic_value:%s",o_value,ml_value,p_value)

        a=o_value
        m=ml_value
        b=p_value

        #Calculating alpha and beta from PERT[o_value,ml_value,p_value] calculated above
        alpha=(2*(b+4*m-5*a)/3*(b-a))*(1+4*((m-a)*(b-m)/(b-a)^2))        
        bet=(2*(5*b-4*m-a)/3*(b-a))*(1+4*((m-a)*(b-m)/(b-a)^2))

        logger.debug("alpha:%s,beta:%s",alpha,bet)
        
        #Calculate pert beta distribution using alpha and bet
        D_ij = beta(alpha, bet)
        logger.debug("Beta distribution:%s",D_ij) 

        distribution_dic[arch]=D_ij

    return distribution_dic


