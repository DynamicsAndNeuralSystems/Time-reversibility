#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     January 2025                                      #
#                                                               #
#   Summary:  Simulations                                       #
#                                                               #
#################################################################

from noises import *
from arma import *
from henon import *
from deterministic_models import *
from logistic import *
from conservative_maps import *
from quadratic import *
from stochastic_sine_map import *

status = True
# coloured noise simulated in MATLAB (pink, brown, violet)
## iid noise
data_gno=status
data_uno=status

## autoregressive
data_ar1_gno=status
data_ar1_uno=status
data_star_gno=status
data_arma11_uno=status
data_nar2=status
data_ar3 = status
data_setar1=status
data_setar2=status

## deterministic chaotic maps 
data_arnold=status
data_chirikov=status
data_hen=status
data_logistic4=status
data_logistic38284=status
data_quadratic=status

## sum of chaotic maps
data_hen_sum=status
data_henr_diverse=status
data_henr_same=status
data_quadratic_rsum=status

## other deterministic
data_llog=status
data_moda=status

## other stochastic
data_sine =status

length=int(7000) #length of time series
n=100 #number of repetitions
save_to = f"Data_{length-5000}_dsct/"

if data_gno==True:
    gno=GNO(n=n, length=length)
    print("Starting: ", gno.name)
    gno.generate()
    gno.discard_transient()
    ts,rts=gno.save(save_to=save_to)

if data_uno==True:
    uno=UNO(n=n, length=length)
    print("Starting: ", uno.name)
    uno.generate()
    uno.discard_transient()
    ts,rts=uno.save(save_to=save_to)

if data_ar1_gno==True:
    ar1=AR1_GNO(n=n, length=length)
    print("Starting: ", ar1.name)
    ar1.generate()
    ar1.discard_transient()
    ts,rts=ar1.save(save_to=save_to)

if data_ar1_uno==True:
    ar1_uno=AR1_UNO(n=n, length=length)
    print("Starting: ", ar1_uno.name)
    ar1_uno.generate()
    ar1_uno.discard_transient()
    ts,rts=ar1_uno.save(save_to=save_to)

if data_star_gno==True:
    star=STAR_GNO(n=n, length=length)
    print("Starting: ", star.name)
    star.generate()
    star.discard_transient()
    ts,rts=star.save(save_to=save_to)

if data_arma11_uno==True:
    arma11_uno=ARMA11_UNO(n=n, length=length)
    print("Starting: ", arma11_uno.name)
    arma11_uno.generate()
    arma11_uno.discard_transient()
    ts,rts=arma11_uno.save(save_to=save_to)

if data_nar2==True:
    narma=NonLinearAR2(n=n, length=length)
    print("Starting: ", narma.name)
    narma.generate()
    narma.discard_transient()
    ts,rts=narma.save(save_to=save_to)

if data_ar3==True:
    ngrp=AR3_Gamma(n=n, length=length)   
    print("Starting: ", ngrp.name)
    ngrp.generate()
    ngrp.discard_transient()
    ts,rts=ngrp.save(save_to=save_to)

if data_setar1==True:
    setar=SETAR1_GNO(n=n, length=length)
    print("Starting: ", setar.name)
    setar.generate()
    setar.discard_transient()
    ts,rts=setar.save(save_to=save_to)

if data_setar2==True:
    setar=SETAR2_GNO(n=n, length=length)
    print("Starting: ", setar.name)
    setar.generate()
    setar.discard_transient()
    ts,rts=setar.save(save_to=save_to)

if data_arnold==True:
    arnold=ArnoldCat(n=n, length=length)
    print("Starting: ", arnold.name)
    arnold.generate()
    arnold.discard_transient()
    ts,rts=arnold.save(save_to=save_to)

if data_chirikov==True:
    chirikov=ChirikovMap(n=n, length=length)
    print("Starting: ", chirikov.name)
    chirikov.generate()
    chirikov.discard_transient()
    ts,rts=chirikov.save(save_to=save_to)

if data_hen==True:
    hen=HEN(n=n, length=length)
    print("Starting: ", hen.name)
    hen.generate()
    hen.discard_transient() 
    ts,rts=hen.save(save_to=save_to)

if data_logistic4==True:
    logistic=Logistic4(n=n, length=length)
    print("Starting: ", logistic.name)
    logistic.generate()
    logistic.discard_transient()
    ts,rts=logistic.save(save_to=save_to)

if data_logistic38284==True:
    logistic=Logistic38284(n=n, length=length)
    print("Starting: ", logistic.name)
    logistic.generate()
    logistic.discard_transient()
    ts,rts=logistic.save(save_to=save_to)

if data_quadratic==True:
    quadratic=Quadratic(n=n, length=length)
    print("Starting: ", quadratic.name)
    quadratic.generate()
    quadratic.discard_transient()
    ts,rts=quadratic.save(save_to=save_to)

if data_hen_sum==True:
    henf=HEN_SUM(n=n, length=length)
    print("Starting: ", henf.name)
    henf.generate()
    henf.discard_transient()
    ts,rts=henf.save(save_to=save_to)

if data_henr_diverse==True:
    henr=HENR_diverse(n=n, length=length)
    print("Starting: ", henr.name)
    henr.generate()
    henr.discard_transient()
    ts,rts=henr.save(save_to=save_to)

if data_henr_same==True:
    henr=HENR_same(n=n, length=length)
    print("Starting: ", henr.name)
    henr.generate()
    henr.discard_transient()
    ts,rts=henr.save(save_to=save_to)

if data_quadratic_rsum==True:
    quadratic_sum=QuadraticRSum(n=n, length=length)
    print("Starting: ", quadratic_sum.name)
    quadratic_sum.generate()
    quadratic_sum.discard_transient()
    ts,rts=quadratic_sum.save(save_to=save_to)

if data_llog==True:
    llog=LLOG(n=n, length=length)
    print("Starting: ", llog.name)
    llog.generate()
    llog.discard_transient()
    ts,rts=llog.save(save_to=save_to)

if data_moda==True:
    moda=MODA(n=n,length=length)
    print("Starting: ", moda.name)
    moda.generate()
    moda.discard_transient()
    ts,rts=moda.save(save_to=save_to)

if data_sine==True:
    sine=StochasticSineMap(n=n, length=length)
    print("Starting: ", sine.name)
    sine.generate()
    sine.discard_transient()
    ts,rts=sine.save(save_to=save_to)



