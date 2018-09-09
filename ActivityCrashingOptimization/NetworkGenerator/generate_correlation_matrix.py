
from nearest_correlation import nearcorr
import numpy as np
import random

def generate_correlation_matrix(num_activities,logger):    
    P=np.zeros( (num_activities,num_activities) )
    for k in range(num_activities):
        for i in range(num_activities):
            if(k==i):
                P[k][i] = 1
            elif(k<i):
                P[k][i] = random.uniform(-1, 1)
            else:
                P[k][i] = P[i][k]
    
    logger.debug("Random Correlation Matrix:")
    print(P)
    
    A=nearcorr(P)
    logger.debug("Positive Definite Correlation Matrix:")    
    print(A)
    
    print(np.linalg.eigvals(A))
    print(np.all(np.linalg.eigvals(A) >= 0))

    return A




            
        
    