#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     September 2024                                    #
#                                                               #
#   Summary:  Implementation of logistic map                    #
#                                                               #
#################################################################

import numpy as np
from discrete_time_series_generator import TimeSeriesGenerator
import pandas as pd


class Logistic(TimeSeriesGenerator):
    """
    Logistic map. It is deterministic but different realizations are generated depending on the initial conditions
    x_n = r * x_{n-1} * (1 - x_{n-1})

    (Zanin, 2021)
    """
    def __init__(self, name="LOGISTIC", n=1, length=100, r=1, allow_diverge=False): # define instances
        super().__init__(name, n=n, length=length)  # instances inherited from parental class
        self.r=r    # instances of the class
        self.allow_diverge = allow_diverge
    
    def generate_forward(self):
        x = self.generate_trajectory()
        
        # If data diverge, recursively generate until there is no overflow
        while pd.isnull(x).any() and not self.allow_diverge:
            x=self.generate_trajectory()
        return x

    def generate_trajectory(self):
        x0=np.random.rand()
        x=[x0]
        try:
            for k in range(1, self.length):
                x_new= self.r * x[k-1] * (1.0-x[k-1])
                x.append(x_new)
        except OverflowError as e:
            for k in range(self.length - len(x)):
                x.append(np.nan)
        
        return np.array(x)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3) 
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples
    
class Logistic4(Logistic):
    """
    Logistic map with r=4

    (Zanin, 2021)
    """
    def __init__(self, name="LOGISTIC4", n=1, length=100):
        super().__init__(name, n=n, length=length, r=4)

class Logistic38284(Logistic):
    """
    Logistic map with r=3.8284

    (ArolaFernandez, 2023)
    """
    def __init__(self, name="LOGISTIC38284", n=1, length=100):
        super().__init__(name, n=n, length=length, r=3.8284)
'''    
class Logistic32(Logistic):
    """
    Logistic map with r=3.2
    """
    def __init__(self, name="LOGISTIC32", n=1, length=100):
        super().__init__(name, n=n, length=length, r=3.2)
'''

    
    
       