#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     March 2025                                        #
#                                                               #
#   Summary:  Implementation of dissipative  maps               #
#                                                               #
#################################################################

import numpy as np
from continuous_time_series_generator import ThreeDimContinuousTimeSeriesGenerator
from statsmodels.tsa.stattools import acf
from BF_PointOfCrossing import BF_PointOfCrossing
import sdeint as sde

class LorenzStochastic(ThreeDimContinuousTimeSeriesGenerator):
    """
    Lorenz system

    dxdt=10(y-x) + a * eta_x
    dydt=x(28-z)-y + a * eta_y
    dzdt=xy-8/3z + a * eta_z
    where eta_x, eta_y, eta_z are independent white noise processes (Wiener)
 
    (Martinez, 2018) + dynamical noise
    """
    def __init__(self, name="LORENZ_STOCH", n=1, length=100, dt=1e-2, sigma=10, rho=28, beta=8/3, a = 1.5, allow_diverge=False):
        super().__init__(name, n=n, length=length)
        self.dt = dt
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.allow_diverge = allow_diverge
        self.a = a
    
    def generate_forward(self):

        T=self.length  # length in time of time series
        dt=self.dt   # sampling time

        sigma=self.sigma
        rho=self.rho
        beta=self.beta
        dt=self.dt
        a=self.a

        # Deterministic part
        def f( state, t):
            x, y, z = state 
            dxdt = sigma*(y-x) 
            dydt = x*(rho-z)-y
            dzdt = x*y - beta*z
        
            return np.array([dxdt, dydt, dzdt])
        
        # Stochastic part
        def g(state, t):
            return np.diag([a, a, a])
        

        x0=np.random.uniform(-8, 8.)
        y0=np.random.uniform(-8., 8.)
        z0=np.random.uniform(0, 10.)
        initial_state = [x0, y0, z0]

        #t=np.linspace(0, T, N)
        t_span = np.linspace(0, T, int(T/dt))
        states = sde.itoEuler(f, g, initial_state, t_span)

        return states[:,0], states[:,1], states[:,2]    # remove last two points 
    
    def discard_transient_forward(self):
        T = self.length
        dt = self.dt
        N = int(T/dt)
        N_star = int(5000)

        for i in range(self.n):
            self.samples_x[i] = self.samples_x[i][N_star:]
            self.samples_y[i] = self.samples_y[i][N_star:]
            self.samples_z[i] = self.samples_z[i][N_star:]
            self.samples_sum[i] = self.samples_sum[i][N_star:]

        return self.samples_x, self.samples_y, self.samples_z, self.samples_sum
    
    def downsample_forward(self):
        "Downsampling factor is the first lag where the ACF is below 1/e"
        acf_ds = True
        downsampling_factor = np.empty((self.n, 4))
        
        for i in range(self.n): 
            if acf_ds == True:
                # Compute acf for x,y,z
                acf_x = acf(self.samples_x[i], nlags=len(self.samples_x[i])-1)
                acf_y = acf(self.samples_y[i], nlags=len(self.samples_y[i])-1)
                acf_z = acf(self.samples_z[i], nlags=len(self.samples_z[i])-1)
                acf_sum = acf(self.samples_sum[i], nlags=len(self.samples_sum[i])-1)
                # Get the first lag where ACF is below 1/e
                lag_x = BF_PointOfCrossing(acf_x, 1/np.e, False)[0] # first lag where ACF is below 1/e
                lag_y = BF_PointOfCrossing(acf_y, 1/np.e, False)[0]
                lag_z = BF_PointOfCrossing(acf_z, 1/np.e, False)[0]
                lag_sum = BF_PointOfCrossing(acf_sum, 1/np.e, False)[0]
                #lag_x = BF_PointOfCrossing(acf_x, 0, False)[0] # first lag where ACF is below 1/e
                #lag_y = BF_PointOfCrossing(acf_y, 0, False)[0]
                #lag_z = BF_PointOfCrossing(acf_z, 0, False)[0]
                #lag_sum = BF_PointOfCrossing(acf_sum, 0, False)[0]
                # Factors for downsampling
                factor_x = int(lag_x)
                factor_y = int(lag_y)
                factor_z = int(lag_z)
                factor_sum = int(lag_sum)
                downsampling_factor[i] = np.array([factor_x, factor_y, factor_z, factor_sum])

            else:
                factor_x = 1
                factor_y = 1
                factor_z = 1
                factor_sum = 1

                downsampling_factor[i] = np.array([factor_x, factor_y, factor_z, factor_sum])

            # Downsample
            self.samples_x[i] = self.samples_x[i][0::factor_x]
            self.samples_y[i] = self.samples_y[i][0::factor_y]
            self.samples_z[i] = self.samples_z[i][0::factor_z]
            self.samples_sum[i] = self.samples_sum[i][0::factor_sum]


        return self.samples_x, self.samples_y, self.samples_z, self.samples_sum, downsampling_factor
    
    def cut_trajectory_forward(self):
        """
        Cuts trajectory to "cut" samples
        """
        cut = 5e3
        for i in range(self.n):
            if len(self.samples_x[i]) > int(cut):
                self.samples_x[i] = self.samples_x[i][:int(cut)]
            else:
                self.samples_x[i] = self.samples_x[i]

            if len(self.samples_y[i]) > int(cut):
                self.samples_y[i] = self.samples_y[i][:int(cut)]
            else:
                self.samples_y[i] = self.samples_y[i]

            if len(self.samples_z[i]) > int(cut):
                self.samples_z[i] = self.samples_z[i][:int(cut)]
            else:
                self.samples_z[i] = self.samples_z[i]

            if len(self.samples_sum[i]) > int(cut):
                self.samples_sum[i] = self.samples_sum[i][:int(cut)]
            else:
                self.samples_sum[i] = self.samples_sum[i]

        return self.samples_x, self.samples_y, self.samples_z, self.samples_sum
    