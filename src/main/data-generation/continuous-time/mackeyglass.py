import numpy as np
from continuous_time_series_generator import ContinuousTimeSeriesGenerator
from statsmodels.tsa.stattools import acf
from BF_PointOfCrossing import BF_PointOfCrossing


class MackeyGlass17(ContinuousTimeSeriesGenerator):
    """
    Mackey-Glass introduced in (Mackey and Glass, 1977) 
    dx/dt = beta0*x(t-tau)/(1+x(t-tau)^m) - gamma*x(t)

    Solution with Runge-Kutta method
    """
    def __init__(self, name="MACKEYGLASS17", n=1, length=1000, beta0=0.2, gamma=0.1, tau=17, m=10, dt=1):
        super().__init__(name, n=n, length=length)
        self.beta0=beta0
        self.gamma=gamma
        self.tau=tau
        self.m=m
        self.dt=dt
    
    def generate_forward(self):
        beta0=self.beta0
        gamma=self.gamma
        tau=self.tau
        m=self.m
        dt=self.dt

        def mackey_glass(t, x, x_tau):
            """
            Mackey Glass equation
            """
            dxdt= beta0 * x_tau/(1.+x_tau**m) - gamma*x
            return dxdt
        
        def RK4(f, t, x, x_tau, dt):
            k1 = f(t, x, x_tau)
            k2 = f(t+dt/2, x+dt*k1/2, x_tau)
            k3 = f(t+dt/2, x+dt*k2/2, x_tau)
            k4 = f(t+dt, x+dt*k3, x_tau)
            return x + dt/6. * (k1 + 2*k2 + 2*k3 + k4)
        
        T=self.length  # length in time of time series
        dt=self.dt # integration time step
        N=int(T/dt) # number of samples

        k=int(tau/dt)  # number of samples for past
        x=np.zeros(N)

        x0=np.random.uniform(0., 1.5)  # initial condition (or 1.2)
        x[0]=x0

        for i in range(N-1):
            if i < k:
                x_tau = 0.
            elif i==k:
                x_tau = x0
            else:
                x_tau = x[i-k]
            
            x[i+1] = RK4(mackey_glass, i*dt, x[i], x_tau, dt)

        return x
    
    def discard_transient_forward(self):
        T = self.length
        dt = self.dt 
        N = int(T/dt)
        N_star = int(5000)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]

        return self.samples
    
    def downsample_forward(self):
        "Downsampling factor is the first lag where the ACF is below 1/e"
        acf_ds = True
        downsampling_factor = np.zeros(self.n)
        for i in range(self.n): 
            if acf_ds == True:
                acf_values = acf(self.samples[i], nlags=len(self.samples[i])-1)
                lag = BF_PointOfCrossing(acf_values, 1/np.e, False)[0] # first lag here ACF is below 1/e
                #lag = BF_PointOfCrossing(acf_values, 0, False)[0] 
                factor = int(lag)
                # store in vertical array
                downsampling_factor[i] = factor
            else: 
                
                factor = 1 #100
                
                downsampling_factor[i] = factor

            self.samples[i] = self.samples[i][0::factor]
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
    

    