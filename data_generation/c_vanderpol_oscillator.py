import numpy as np
from continuous_time_series_generator import ContinuousTimeSeriesGenerator
from statsmodels.tsa.stattools import acf
from BF_PointOfCrossing import BF_PointOfCrossing
from scipy.integrate import solve_ivp

class VanDerPol(ContinuousTimeSeriesGenerator):
    """
    Van der Pol Oscillator:
    d^2x/dt^2 - mu * (1 - x^2) * dx/dt + x = 0

    That can be recasted as the combined
    dx/dt = y
    dy/dt = mu * (1 - x^2) * y - x
    mu is the (nonlinearity?) parameter
    
    """

    def __init__(self, name = "VDP", n=1, length=1000, dt = 1e-2, mu=1.0):
        super().__init__(name, n=n, length=length)
        self.mu = mu
        self.dt = dt 


    def generate_forward(self):
        T = self.length
        dt = self.dt

        mu = self.mu

        def vanderpol(t, y):
            x, y = y
            dxdt = y
            dydt = mu * (1 - x**2) * y - x
            return [dxdt, dydt]
        

        # Initial conditions
        x0 = np.random.uniform(-2, 2)
        y0 = np.random.uniform(-2,2)
        initial_state = [x0, y0]

        t_span = (0, T)

        states = solve_ivp(vanderpol, 
                           t_span = t_span, 
                           y0 = initial_state,
                           max_step = dt)
                           #method='RK45')
        
        return states.y[0,:-2]#, states.y[1,:-2]
    

    def discard_transient_forward(self):
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
        cut = 5e3
        for i in range(self.n):
            if len(self.samples[i]) > int(cut):
                self.samples[i] = self.samples[i][:int(cut)]
            else:
                self.samples[i] = self.samples[i]
        return self.samples

class Oscillator(ContinuousTimeSeriesGenerator):
    """
    Simple classical oscillator
    d^2x/dt^2 + x = 0
    
    """

    def __init__(self, name = "Oscillator", n=1, length=1000, dt = 1e-2, mu=0):
        super().__init__(name, n=n, length=length)
        self.mu = mu
        self.dt = dt 


    def generate_forward(self):
        T = self.length
        dt = self.dt

        mu = self.mu

        def vanderpol(t, y):
            x, y = y
            dxdt = y
            dydt = mu * (1 - x**2) * y - x
            return [dxdt, dydt]
        

        # Initial conditions
        x0 = np.random.uniform(-2, 2)
        y0 = np.random.uniform(-2,2)
        initial_state = [x0, y0]

        t_span = (0, T)

        states = solve_ivp(vanderpol, 
                           t_span = t_span, 
                           y0 = initial_state,
                           max_step = dt)
                           #method='RK45')
        
        return states.y[0,:-2]#, states.y[1,:-2]
    

    def discard_transient_forward(self):
        
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
    


