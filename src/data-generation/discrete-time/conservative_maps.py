#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     January 2025                                      #
#                                                               #
#   Summary:  Implementation of conservative maps               #
#                                                               #
#################################################################

import numpy as np
from  discrete_time_series_generator import TimeSeriesGenerator
import pandas as pd

class ArnoldCat(TimeSeriesGenerator):
    """
    Arnold's cat map

    x[n+1] = x[n] + y[n] mod 1
    y[n+1] = x[n] + 2*y[n] mod 1

    (Zanin, 2021)
    """
    def __init__(self, name="ARNOLD", n=1, length=100, allow_diverge=False):
        super().__init__(name, n=n, length=length)
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
                x_new = (x[k-1] + y[k-1]) % 1
                y_new = (x[k-1] + 2*y[k-1]) % 1
                x.append(x_new)
                y.append(y_new)
        except OverflowError as e:
            for k in range(self.length - len(x)):
                x.append(np.nan)
                y.append(np.nan)
        
        return np.array(x), np.array(y)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3) #int(10/100 * N)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples


class ChirikovMap(TimeSeriesGenerator):
    """
    Chirikov standard map

    theta[n+1] = theta[n] + p[n] + K/(2pi) * sin(2pi*theta[n]) mod 1
    p[n+1] = theta[n+1] - theta[n] mod 1

    (me)
    """
    def __init__(self, name="CHIRIKOV", n=1, length=100, k=0.971635, allow_diverge=False):
        super().__init__(name, n=n, length=length)
        self.k = k
        self.allow_diverge = allow_diverge

    def generate_forward(self):
        p, theta = self.generate_trajectory()

        # If data diverge, recursively generate until there is no overflow
        while (pd.isnull(p).any() or pd.isnull(theta).any()) and not self.allow_diverge:
            traj=self.generate_trajectory()
            p=traj[0]
            theta=traj[1]
        return p
    
    def generate_trajectory(self):
        p0=np.random.rand()
        theta0=np.random.rand()
        
        p=[p0]
        theta=[theta0]
        try:
            for i in range(1, self.length):
                theta_new = (theta[i-1] + p[i-1] + self.k/(2.0 * np.pi) * np.sin(2.0 * np.pi * theta[i-1])) % 1
                p_new = (theta_new - theta[i-1] ) % 1
                p.append(p_new)
                theta.append(theta_new)
        except OverflowError as e:
            for i in range(self.length - len(p)):
                p.append(np.nan)
                theta.append(np.nan)
        
        return np.array(p), np.array(theta)
    
    def discard_transient_forward(self):
        N = self.length
        N_star= int(5e3) #int(10/100 * N)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]

        return self.samples
    