import numpy as np
from discrete_time_series_generator import *
import pandas as pd


class StochasticSineMap(TimeSeriesGenerator):
    """
    Generate a stochastic sine map time series.
    The sine map is defined by the equation:
    x_{n+1} = mu * sin(x_n) + y_n * eta_n,
    with y_n is a rv from a Bernulli process with probability p, 
    eta_n is a rv from a uniform distribution between b and -b.

    (Freitas, PHYSICAL REVIEW E 79, 035201 R 2009)
    """""
    def __init__(self, name = 'SINE_STOCH', n=1, length=100, mu=2.4, p=0.01, b=2 , allow_diverge=False):
        super().__init__(name, n=n, length=length)
        self.mu = mu
        self.p = p
        self.b = b
        self.allow_diverge = allow_diverge

    def generate_forward(self):
        x = self.generate_trajectory()

        # If data diverge, recursively generate until there is no overflow
        while pd.isnull(x).any() and not self.allow_diverge:
            x=self.generate_trajectory()
        return x
    
    def generate_trajectory(self):
        x0 = np.random.rand()
        x = [x0]
        y = np.random.binomial(1, self.p, self.length)
        eta = np.random.uniform(-self.b, self.b, self.length)
        try:
            for k in range(1, self.length):
                x_new = self.mu * np.sin(x[k-1]) + y[k] * eta[k]
                x.append(x_new)
        except OverflowError as e:
            for k in range(self.length - len(x)):
                x.append(np.nan)
     
        return np.array(x)
    
    def discard_transient_forward(self):
        N = self.length
        N_star= int(5e3) #int(10/100 * N)
        
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]

        return self.samples
    

