#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     September 2024                                    #
#                                                               #
#   Summary:  Implementation of Henon maps and combinations     #
#             of Henon maps with reversed ones                  #
#                                                               #
#################################################################

import numpy as np
from discrete_time_series_generator import TimeSeriesGenerator
import pandas as pd

class HEN(TimeSeriesGenerator):
    """
    Henon map. It is deterministic but different realizations are generated depending on the initial conditions
    """
    def __init__(self, name="HEN", n=1, length=100, a=1.4, b=0.3, allow_diverge=False): # define instances
        super().__init__(name, n=n, length=length)  # instances inherited from parental class
        self.a=a    # instances of the class
        self.b=b
        self.allow_diverge = allow_diverge
    
    def generate_forward(self):
        x,y = self.generate_trajectory()
        
        # If data diverge, recursively generate until there is no overflow
        while (pd.isnull(x).any() or pd.isnull(y).any()) and not self.allow_diverge:
            traj=self.generate_trajectory()
            x=traj[0]
            y=traj[1]
        return x

    def generate_trajectory(self):
        x0=np.random.rand()
        y0=np.random.rand()
        
        x=[x0]
        y=[y0]
        try:
            for k in range(1, self.length):
                x_new= 1. - self.a * x[k-1]**2 + y[k-1]
                y_new= self.b* x[k-1]
                x.append(x_new)
                y.append(y_new)
        except OverflowError as e:
            for k in range(self.length - len(x)):
                x.append(np.nan)
                y.append(np.nan)
        
        return np.array(x), np.array(y)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:] 

        return self.samples
    
class HEN_SUM(HEN):
    """
    Combination of two realizations of Henon map, both forward in time 

    (Diks, 1995)
    """
    def __init__(self, name="HEN_SUM", n=1, length=100, a=1.4, b=0.3, allow_diverge=False):
        super().__init__(name, n=n, length=length)
        self.a=a
        self.b=b
        self.allow_diverge=allow_diverge

    def generate_forward(self):
        x1=super().generate_forward()
        x2=super().generate_forward()

        return x1+x2


class HENR_diverse(HEN):
    """
    Combination of a realization of Henon map and the reversed of another realization of Henon map
    with different initial conditions 

    (Diks, 1995)
    """
    def __init__(self, name="HENR_diverse", n=1, length=100, a=1.4, b=0.3, allow_diverge=False):
        super().__init__(name, n=n, length=length)
        self.a=a
        self.b=b
        self.allow_diverge=allow_diverge

    def generate_forward(self):
        x1=super().generate_forward()
        x2=super().generate_forward()
        # Reverse time series
        x2_r=x2[::-1]

        return x1+x2_r

class HENR_same(HEN):
    """
    Combination of a realization of Henon map and its reversed 
    with different initial conditions 
    """
    def __init__(self, name="HENR_same", n=1, length=100, a=1.4, b=0.3, allow_diverge=False):
        super().__init__(name, n=n, length=length)
        self.a=a
        self.b=b
        self.allow_diverge=allow_diverge

    def generate_forward(self):
        x1=super().generate_forward()
        # Reverse time series
        x1_r=x1[::-1]

        return x1+x1_r
    