#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     August 2024                                       #
#                                                               #
#   Summary:  Implementation of other deterministic models      #
#                                                               #
#################################################################

import numpy as np
from discrete_time_series_generator import TimeSeriesGenerator

class LLOG(TimeSeriesGenerator):
    """
    Linear model with deterministic noise source:
    x_n=0.5*x_n-1+epsilon_n
    epsilon_n is a realization of the chaotic logistic model:
    epsilon_n= 4*epsilon_n-1*(1-epsilon_n-1)
    
    (Diks, 1995)
    """
    def __init__(self, name="LLOG", n=1, length=100, a=0.5):
        super().__init__(name, n, length)
        self.a=a

    def generate_forward(self):
        x0=np.random.rand()
        epsilon0=np.random.rand()
        x=[x0]
        epsilon=[epsilon0]

        # Generation of deterministic noise
        for k in range(1, self.length):
            epsilon_new= 4.*epsilon[k-1]*(1.-epsilon[k-1])
            epsilon.append(epsilon_new)

        # Generation of time series
        for k in range(1, self.length):
            x_new= self.a*x[k-1]+epsilon[k]
            x.append(x_new)

        return np.array(x)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3) 
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples
    
class MOD(TimeSeriesGenerator):
    """
    x_n=ax_n-1 mod1
    (Diks, 1995)
    """
    def __init__(self, name="MOD", n=1, length=100, a=1):
        super().__init__(name, n, length)
        self.a=a
    
    def generate_forward(self):
        x=np.random.rand()

        x_vals=[]
        for k in range(self.length):
            x_vals.append(x)
            x=(self.a * x) % 1 

        return np.array(x_vals)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3)  
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples
    
class MODA(MOD):
    def __init__(self, name="MODA", n=1, length=100, a=np.sqrt(2)):
        super().__init__(name, n, length, a=a)
        
class MODB(MOD):
    def __init__(self, name="MODB", n=1, length=100, a=np.sqrt(20)):
        super().__init__(name, n, length, a=a)

class MODC(MOD):
    def __init__(self, name="MODC", n=1, length=100, a=np.sqrt(200)):
        super().__init__(name, n, length, a=a)

