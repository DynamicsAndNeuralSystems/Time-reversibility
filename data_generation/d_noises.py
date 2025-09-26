#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     August 2024                                       #
#                                                               #
#   Summary:  Implementation of different noise sources         #
#                                                               #
#################################################################

import numpy as np
from discrete_time_series_generator import TimeSeriesGenerator

## Coloured noise: Run in MATLAB to generate the time series

class GNO(TimeSeriesGenerator): # subclass of TimeSeriesGenerator
    """
    i.i.d. Gaussian noise
    """
    def __init__(self, name="GNO", n=1, length=100):
        super().__init__(name, n=n, length=length) # call initializer of parent class
    def generate_forward(self):
        return np.random.normal(loc=0, scale=1, size=self.length) 
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3) #int(10/100 * N)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples

class UNO(TimeSeriesGenerator): # subclass of TimeSeriesGenerator
    """
    i.i.d. uniform noise
    """
    def __init__(self, name="UNO", n=1, length=100):
        super().__init__(name, n=n, length=length) # call initializer of parent class
    def generate_forward(self):
        return np.random.uniform(low=-0.5, high=0.5, size=self.length)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3) #int(10/100 * N)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples
    


