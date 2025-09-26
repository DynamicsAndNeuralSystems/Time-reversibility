#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     March 2025                                        #
#                                                               #
#   Summary:  Simulations                                       #
#                                                               #
#################################################################

from c_ornstein_uhlenbeck import *
from c_dissipative_flows import *
from c_mackeyglass import *
from c_stochastic_dissipative_flows import *
from bounded_random_walk import *
from c_vanderpol_oscillator import *
from c_stochastic_vanderpol import *


status = True
data_vdp = True
data_oscillator = True
data_lorenz = True
data_rossler = True
data_stochLorenz = True #
data_stochasticVDP = True #
data_ou = True #
data_brw_cont =True
data_MackeyGlass17 = True #

length = int(1.2e4) # length of time series (dt=1e-2)
n = 100#number of repetitions

if data_vdp==False:
    vdp=VanDerPol(n=n, length=length)
    vdp.generate()
    vdp.discard_transient()
    vdp.downsample()
    vdp.cut_trajectory()
    ts, rts =vdp.save()


if data_oscillator==False:
    oscillator=Oscillator(n=n, length=length)
    oscillator.generate()
    oscillator.discard_transient()
    oscillator.downsample()
    oscillator.cut_trajectory()
    ts, rts =oscillator.save()
    

if data_lorenz==False:
    lorenz=Lorenz(n=n, length=length)
    lorenz.generate()
    lorenz.discard_transient()
    lorenz.downsample()
    lorenz.cut_trajectory()
    ts_x, ts_y, ts_z, ts_sum, rts_x, rts_y, rts_z, rts_sum=lorenz.save()

if data_rossler==False:
    rossler=Rossler(n=n, length=length)
    rossler.generate()
    rossler.discard_transient()
    rossler.downsample()
    rossler.cut_trajectory()
    ts_x, ts_y, ts_z, ts_sum, rts_x, rts_y, rts_z, rts_sum=rossler.save()
 

if data_stochLorenz==False:
    lorenz=LorenzStochastic(n=n, length=length)
    lorenz.generate()
    lorenz.discard_transient()
    lorenz.downsample()
    lorenz.cut_trajectory()
    ts_x, ts_y, ts_z, ts_sum, rts_x, rts_y, rts_z, rts_sum=lorenz.save()

if data_stochasticVDP==False:
    stoch_vdp=VanDerPolStochastic(n=n, length=length)
    stoch_vdp.generate()
    stoch_vdp.discard_transient()
    stoch_vdp.downsample()
    stoch_vdp.cut_trajectory()
    ts, rts =stoch_vdp.save()

if data_ou==False:
    ou_em=OrnsteinUhlenbeck(n=n, length=length)
    ou_em.generate()    
    ou_em.discard_transient()
    ou_em.downsample()
    ou_em.cut_trajectory()
    ts, rts =ou_em.save()

length = int(100001)
if data_MackeyGlass17==False:
    mg=MackeyGlass17(n=n, length=length)
    mg.generate()
    mg.discard_transient()
    mg.downsample()
    mg.cut_trajectory()
    ts,rts=mg.save()   

length = int(1100)
if data_brw_cont==False:
    brw=BoundedRandomWalkContinuous(n=n, length=length)
    brw.generate()
    brw.discard_transient()
    brw.downsample()
    brw.cut_trajectory()
    ts,rts=brw.save()