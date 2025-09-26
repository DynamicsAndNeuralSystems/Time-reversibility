import numpy as np
from continuous_time_series_generator import *
import pandas as pd
from statsmodels.tsa.stattools import acf
from BF_PointOfCrossing import BF_PointOfCrossing
import sdeint as sde

class BoundedRandomWalkContinuous(ContinuousTimeSeriesGenerator):
    """
    Generate a continuous time bounded random walk
    
    Nicolau
    """

    def __init__(self, name = 'BRW_cont', n=1, length=100,  dt=1e-3, k=-2, alpha1=2, alpha2=2, tau=0, sigma=4, beta=0.1, mu = 0, allow_diverge=False):
        super().__init__(name, n=n, length=length)
        self.dt = dt
        self.k = k
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.tau = tau
        self.sigma = sigma
        self.beta = beta
        self.mu = mu
        self.allow_diverge = False


    def generate_forward(self):
        x = self.generate_trajectory()

        # If data diverge, recursively generate until there is no overflow
        while pd.isnull(x).any() and not self.allow_diverge:
            x=self.generate_trajectory()
        return x
    
    def generate_trajectory(self):
        T = self.length
        dt = self.dt
        
        k = self.k
        alpha1 = self.alpha1
        alpha2 = self.alpha2
        tau = self.tau
        sigma = self.sigma
        beta = self.beta
        mu = self.mu

        # Deterministic part
        def f(x, t):
            return np.exp(k) * (np.exp(-alpha1*(x-tau)) - np.exp(alpha2*(x-tau)))
        
        # Stochastic part
        def g(x, t):
            return np.exp(sigma/2 + beta/2 * (x - mu)**2) 
        
        # Initial condition
        x0 = 0

        t_span = np.linspace(0, T, int(T/dt))
        xs = sde.itoEuler(f, g, x0, t_span)
        #print(xs)

        return xs[:,0]
    
    def discard_transient_forward(self):
        T = self.length
        dt = self.dt 
        N = int(T/dt)
        N_star = int(5000)

        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples
    
    
    def downsample_forward(self):
        "Downsampling factor is the first lag where the ACF is below 1/e"
        downsampling_factor = np.zeros(self.n)
        for i in range(self.n): 
            acf_values = acf(self.samples[i], nlags=len(self.samples[i])-1)
            lag = BF_PointOfCrossing(acf_values, 1/np.e, False)[0] # first lag where ACF is below 1/e
            #lag = BF_PointOfCrossing(acf_values, 0, False)[0]
            factor = int(lag)

            #factor = 1

            self.samples[i] = self.samples[i][0::factor]
            # store in vertical array
            downsampling_factor[i] = factor
        # store in vertical array
        downsampling_factor = downsampling_factor.reshape(self.n, 1)
        return self.samples, downsampling_factor
    
    def cut_trajectory_forward(self):
        """
        Cuts trajectory to "cut" samples
        """
        cut = int(5e3)
        for i in range(self.n):
            if len(self.samples[i]) > int(cut):
                self.samples[i] = self.samples[i][:int(cut)]
            else:
                self.samples[i] = self.samples[i]
        return self.samples
