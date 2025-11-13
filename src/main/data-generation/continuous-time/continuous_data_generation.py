#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     March 2025                                        #
#                                                               #
#   Summary:  Simulations                                       #
#                                                               #
#################################################################

from ornstein_uhlenbeck import *
from dissipative_flows import *
from mackeyglass import *
from stochastic_dissipative_flows import *
from bounded_random_walk import *
from vanderpol_oscillator import *
from stochastic_vanderpol import *
import os

status = False
data_vdp = True
data_oscillator = status
data_lorenz = status
data_rossler = status
data_stochLorenz = status 
data_stochasticVDP = status 
data_ou = status 
data_brw_cont = status
data_MackeyGlass17 = status 

length = int(1e4) # length of time series (dt=1e-2)
n = 100 #number of repetitions

cwd = os.getcwd()


dir_data = os.path.join(cwd, 'data-tr/')
# check if folder exists
if not os.path.exists(dir_data):
    os.mkdir(dir_data)

# create time-series data folder
dir_time_series = os.path.join(dir_data, 'time-series')
if not os.path.exists(dir_time_series):
    os.mkdir(dir_time_series)

# create discrete data folder
dir_data_cnt = os.path.join(dir_time_series, 'data-cnt')
if not os.path.exists(dir_data_cnt):
    os.mkdir(dir_data_cnt)


save_to = dir_data_cnt  # folder to save data (specify actual length without transient)

os.makedirs( save_to, exist_ok=True)

if data_vdp==True:
    vdp=VanDerPol(n=n, length=length)
    print("Simulating ", vdp.name)
    vdp.generate()
    vdp.discard_transient()
    vdp.downsample()
    vdp.cut_trajectory()
    ts, rts =vdp.save(save_to=save_to)


if data_oscillator==True:
    oscillator=Oscillator(n=n, length=length)
    print("Simulating ", oscillator.name)
    oscillator.generate()
    oscillator.discard_transient()
    oscillator.downsample()
    oscillator.cut_trajectory()
    ts, rts =oscillator.save(save_to=save_to)
    

if data_lorenz==True:
    lorenz=Lorenz(n=n, length=length)
    print("Simulating ", lorenz.name)
    lorenz.generate()
    lorenz.discard_transient()
    lorenz.downsample()
    lorenz.cut_trajectory()
    ts_x, ts_y, ts_z, ts_sum, rts_x, rts_y, rts_z, rts_sum=lorenz.save(save_to=save_to)

if data_rossler==True:
    rossler=Rossler(n=n, length=length)
    print("Simulating ", rossler.name)
    rossler.generate()
    rossler.discard_transient()
    rossler.downsample()
    rossler.cut_trajectory()
    ts_x, ts_y, ts_z, ts_sum, rts_x, rts_y, rts_z, rts_sum=rossler.save(save_to=save_to)
 

if data_stochLorenz==True:
    lorenz=LorenzStochastic(n=n, length=length)
    print("Simulating ", lorenz.name)
    lorenz.generate()
    lorenz.discard_transient()
    lorenz.downsample()
    lorenz.cut_trajectory()
    ts_x, ts_y, ts_z, ts_sum, rts_x, rts_y, rts_z, rts_sum=lorenz.save(save_to=save_to)

if data_stochasticVDP==True:
    stoch_vdp=VanDerPolStochastic(n=n, length=length)
    print("Simulating ", stoch_vdp.name)
    stoch_vdp.generate()
    stoch_vdp.discard_transient()
    stoch_vdp.downsample()
    stoch_vdp.cut_trajectory()
    ts, rts =stoch_vdp.save(save_to=save_to)

if data_ou==True:
    ou_em=OrnsteinUhlenbeck(n=n, length=length)
    print("Simulating ", ou_em.name)
    ou_em.generate()    
    ou_em.discard_transient()
    ou_em.downsample()
    ou_em.cut_trajectory()
    ts, rts =ou_em.save(save_to=save_to)

length = int(100001)
if data_MackeyGlass17==True:
    mg=MackeyGlass17(n=n, length=length)
    print("Simulating ", mg.name)
    mg.generate()
    mg.discard_transient()
    mg.downsample()
    mg.cut_trajectory()
    ts,rts=mg.save(save_to=save_to)   

length = int(1100)
if data_brw_cont==True:
    brw=BoundedRandomWalkContinuous(n=n, length=length)
    print("Simulating ", brw.name)
    brw.generate()
    brw.discard_transient()
    brw.downsample()
    brw.cut_trajectory()
    ts,rts=brw.save(save_to=save_to)