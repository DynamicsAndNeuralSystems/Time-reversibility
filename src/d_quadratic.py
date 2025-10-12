#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     September 2024                                    #
#                                                               #
#   Summary:  Implementation of quadratic map                   #
#                                                               #
#################################################################

import numpy as np
from discrete_time_series_generator import TimeSeriesGenerator

class Quadratic(TimeSeriesGenerator):
    """
    Quadratic map
    x[n+1]=1-ax[n]^2

    (Kennel, 2004)
    """
    def __init__(self, name="QUADRATIC", n=1, length=100, a=1.8):
        super().__init__(name, n=n, length=length)
        self.a = a

    def generate_forward(self):
        x = self.generate_trajectory()
        return x
    
    def generate_trajectory(self):
        x0=np.random.rand() 
        x=[x0]
        for k in range(1, self.length):
            x_new= 1 - self.a * x[k-1]**2
            x.append(x_new)
        return np.array(x)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]

        return self.samples

class QuadraticRSum(TimeSeriesGenerator):
    """
    Sum of two quadratic maps
    x[n+1]=1-ax[n]^2
    (Kennel, 2004)
    """
    def __init__(self, name="QUADRATIC_RSUM", n=1, length=100, a=1.8, alpha=1):
        super().__init__(name, n=n, length=length)
        self.a = a
        self.alpha = alpha

    def generate_forward(self):
        x = self.generate_trajectory()
        y = self.generate_trajectory()

        y_r = y[::-1]

        x = x + self.alpha* y_r
        return x
    
    def generate_trajectory(self):
        x0=np.random.rand() 
        x=[x0]
        for k in range(1, self.length):
            x_new= 1 - self.a * x[k-1]**2
            x.append(x_new)
        return np.array(x)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]

        return self.samples
    