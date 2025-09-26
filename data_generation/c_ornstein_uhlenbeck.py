#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     January 2025                                      #
#                                                               #
#   Summary:  Implementation of correlated  processes           #
#                                                               #
#################################################################

import numpy as np
from continuous_time_series_generator import ContinuousTimeSeriesGenerator
from statsmodels.tsa.stattools import acf
from BF_PointOfCrossing import BF_PointOfCrossing
import sdeint as sde


class OrnsteinUhlenbeck(ContinuousTimeSeriesGenerator):
    """
    Ornstein-Uhlenbeck process

    dx = -theta x + sigma*dw

    simulated using sdeint.itoEuler
    """
    def __init__(self, name="OU", n=1, length=100, dt=1e-2, theta=0.8, mu=0.0, sigma=0.3):
        super().__init__(name, n=n, length=length)
        self.dt=dt
        self.theta=theta
        self.mu=mu
        self.sigma=sigma

    def generate_forward(self):
        T=self.length  # length in time of time series
        dt=self.dt   # sampling time
    
        theta=self.theta
        mu=self.mu
        sigma=self.sigma

        # Deterministic part
        def f(x, t):
            return theta * (mu - x)

        # Stochastic part
        def g(x, t):
            return sigma
        
        # Initial condition
        x0 = 0
        t_span = np.linspace(0, T, int(T/dt))

        xs = sde.itoEuler(f, g, x0, t_span)

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
            #lag = BF_PointOfCrossing(acf_values, 0, False)[0] # first lag where ACF is below 1/e
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
        cut = 5e3
        for i in range(self.n):
            if len(self.samples[i]) > int(cut):
                self.samples[i] = self.samples[i][:int(cut)]
            else:
                self.samples[i] = self.samples[i]
        return self.samples
