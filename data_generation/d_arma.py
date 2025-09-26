#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     January 2025                                      #
#                                                               #
#   Summary:  Implementation of ARMA processes                  #
#                                                               #
#################################################################

import numpy as np
from discrete_time_series_generator import TimeSeriesGenerator
from statsmodels.tsa.arima_process import arma_generate_sample

class ARMA(TimeSeriesGenerator):
    """ 
    ARMA model
    scale: std dev of noise
    """
    def __init__(self, name="ARMA", n=1, length=100, ar=None, ma=None, scale=1, distrvs=None):
        super().__init__(name, n=n, length=length)
        # Set of parameters for AR(p) and MA(q) processes
        if ar is None:  # additional instance attributes compared to parental class
            self.ar=np.array([])
        else:
            self.ar=np.array(ar)
        if ma is None:
            self.ma=np.array([])
        else:
            self.ma=np.array(ma)
        
        # By convention set to 1 the first parameter in the AR and MA processes and change the sign to the AR coefficients 
        # (because of how it is implemented the filter function used in the arima generation process)
        self.ar=np.r_[1., -self.ar]
        self.ma=np.r_[1., self.ma]

        self.scale=scale
        self.distrvs=distrvs

    def generate_forward(self):
        return arma_generate_sample(self.ar, self.ma, self.length, scale=self.scale, distrvs=self.distrvs)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3) #int(10/100 * N)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples
        

class AR1_GNO(ARMA):
    """
    AR1 model:
    x_n = 0.5x_n-1 + epsilon_n
    epsilon_n = N(0,1)

    (Diks, 1995)
    """
    def __init__(self, name="AR1_GNO", n=1, length=100, a=0.5):
        super().__init__(name, n=n, length=length, ar=[a], ma=None)


def uniform_noise(size):
    return np.random.uniform(low=-0.5, high=0.5, size=size)

class AR1_UNO(ARMA):
    """
    AR1 model:
    x_n = 0.5x_n-1 + epsilon_n
    epsilon_n = Uniform(-0.5,0.5)
    """
    def __init__(self, name="AR1_UNO", n=1, length=100, a=0.5):
        super().__init__(name, n=n, length=length, ar=[a], ma=None)
    
    def generate_forward(self):
        return arma_generate_sample(self.ar, self.ma, self.length, scale=self.scale, distrvs=uniform_noise)


class ARMA11_UNO(ARMA):
    """
    ARMA(1,1) model:
    x_n-0.6x_n-1=epsilon_n+0.4epsilon_n-1
    epsilon_n = Uniform(-0.5,0.5)
    """
    def __init__(self, name="ARMA11_UNO", n=1, length=100, a=0.6, m=0.4):
        super().__init__(name, n=n, length=length, ar=[a], ma=[m])
    
    def generate_forward(self):
        return arma_generate_sample(self.ar, self.ma, self.length, scale=self.scale, distrvs=uniform_noise)   

class STAR_GNO(AR1_GNO):
    """
    Static transformation
    y_n= 0.6y_n-1 + epsilon_n
    x_n=tanh^2(y_n) 
    of a first order Gaussian random process y_n
    epsilon_n = N(0,1)

    (Diks, 1995)
    """
    def __init__(self, name="STAR_GNO", n=1, length=100, a=0.6):
        super().__init__(name, n=n, length=length, a=a)

    def generate_forward(self):
        x=super().generate_forward()
        return np.tanh(x)**2


class SETAR1_GNO(TimeSeriesGenerator):
    """
    Self-exiting threshold autoregressive model with Gaussian noise 
    x[n] = -0.9 x[n-1] + epsilon[n] if x[n-1] >= 1
    x[n] = -0.4 x[n-1] + epsilon[n] if x[n-1] < 1
    epsilon[n] = N(0,1)

    (Rothman, 1990)
    """
    def __init__(self, name="SETAR1_GNO", n=1, length=100, phi=-0.9, psi=-0.4):
        super().__init__(name, n=n, length=length)
        self.phi=phi
        self.psi=psi

    def generate_forward(self):
        x=np.zeros(self.length)
        x[0]=np.random.normal(0,1)
        for i in range(1, self.length):
            if x[i-1]>=1:
                x[i]=self.phi*x[i-1]+np.random.normal(0,1)
            else:
                x[i]=self.psi*x[i-1]+np.random.normal(0,1)
        return x
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3) #int(10/100 * N)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  # discard initial 10% of the time series

        return self.samples
    

class SETAR2_GNO(TimeSeriesGenerator):
    """
    Self-exiting threshold autoregressive model with Gaussian noise
    x[n]=0.62 + 1.25x[n-1]-0.43x[n-2] + 0.0381epsilon[n] if x[n-2] <= 3.25
    x[n]=2.25 + 1.52x[n-1]-1.24x[n-2] + 0.0626epsilon[n] if x[n-2] > 3.25

    (Martinez, 2018)
    """
    def __init__(self, name="SETAR2_GNO", n=1, length=100, phi=[0.62, 1.25, -0.43, 0.0381], psi=[2.25, 1.52, -1.24, 0.0626], x_star=3.25):
        super().__init__(name, n=n, length=length)
        self.phi=np.array(phi)
        self.psi=np.array(psi)
        self.x_star=x_star

    def generate_forward(self):
        x=np.zeros(self.length)
        x[0]=np.random.normal(0,1)
        x[1]=np.random.normal(0,1)
        for i in range(2, self.length):
            if x[i-2]<=self.x_star:
                x[i]=self.phi[0]+self.phi[1]*x[i-1]+self.phi[2]*x[i-2]+self.phi[3]*np.random.normal(0,1)
            else:
                x[i]=self.psi[0]+self.psi[1]*x[i-1]+self.psi[2]*x[i-2]+self.psi[3]*np.random.normal(0,1)
        return x
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3) #int(10/100 * N)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]

        return self.samples
    
def bimodal_gaussian(mu, sigma):
        return 0.5 * np.random.normal(mu, sigma) + 0.5 * np.random.normal(-mu, sigma)


class NonLinearAR2(TimeSeriesGenerator):
    """
    Nonlinear ARMA with Laplace noise
    x[n] = 0.5 x[n-1]-0.3x[n-2] + 0.1 y[n-2] + 0.1 x[n-2]^2 + 0.4 y[n-1]^2 + 0.0025 eta[n], eta[n] laplacian noise
    y[n] = sin(4pi n) + sin(6pi n) + 0.0025 eta2[n], eta2[n] bimodal gaussian noise

    (Martinez, 2018)
    """
    def __init__(self, name="N_AR2", n=1, length=100, phi=[0.5, -0.3, 0.1, 0.1, 0.4, 0.0025], mu_l=0, b_l=1, mu_b=0.63, sigma=1):
        super().__init__(name, n=n, length=length)
        self.phi=np.array(phi)
        self.mu_l=mu_l
        self.b_l=b_l
        self.mu_b=mu_b
        self.sigma=sigma

    def generate_forward(self):
        x= np.zeros(self.length)
        y= np.zeros(self.length)

        for i in range(2, self.length):
            x[i]=self.phi[0]*x[i-1]+self.phi[1]*x[i-2]+self.phi[2]*y[i-2]+self.phi[3]*x[i-2]**2+self.phi[4]*y[i-1]**2+self.phi[5]*0.5*np.random.laplace(self.mu_l, self.b_l)
            y[i]=np.sin(4*np.pi*i)+np.sin(6*np.pi*i)+self.phi[5]*bimodal_gaussian(self.mu_b, self.sigma)

        return x
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]

        return self.samples
    


class AR3_Gamma(TimeSeriesGenerator):
    """
    Linear non-Gaussian time series
    AR3: x_n= 0.3x_n-3 - 0.2x_n-2 + 0.10x_n-1 + epsilon_n
    Gamma epsilon_n with shape=2 and scale=2
    
    """
    def __init__(self, name="AR3_Gamma", n=1, length=100, a=0.3, b=0.2, c=0.1):
        super().__init__(name, n, length)
        self.a=a
        self.b=b
        self.c=c
    
    def generate_forward(self):
        epsilon=np.random.gamma(shape=1, scale=0.3, size=self.length)
        #epsilon=np.random.normal(loc=0, scale=1, size=self.length)
        x0=np.random.rand()
        x1=np.random.rand()
        x2=np.random.rand()
        x=[x0, x1, x2]
        for k in range(3, self.length):
            x_new=self.a*x[k-3]-self.b*x[k-2]+self.c*x[k-1]+epsilon[k]
            x.append(x_new)

        return np.array(x)
    
    def discard_transient_forward(self):
        N = self.length
        N_star = int(5e3)
        for i in range(self.n):
            self.samples[i] = self.samples[i][N_star:]  
        return self.samples