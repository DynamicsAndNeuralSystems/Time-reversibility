#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     January 2025                                      #
#                                                               #
#   Summary:  Simulations                                       #
#                                                               #
#################################################################

from d_noises import *
from d_arma import *
from d_henon import *
from d_deterministic_models import *
from d_logistic import *
from d_conservative_maps import *
from d_quadratic import *
from d_stochastic_sine_map import *
from bounded_random_walk import *

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

if data_gno==True:
    gno=GNO(n=n, length=length)
    gno.generate()
    gno.discard_transient()
    ts,rts=gno.save()

if data_uno==True:
    uno=UNO(n=n, length=length)
    uno.generate()
    uno.discard_transient()
    ts,rts=uno.save()

if data_ar1_gno==True:
    ar1=AR1_GNO(n=n, length=length)
    ar1.generate()
    ar1.discard_transient()
    ts,rts=ar1.save()

if data_ar1_uno==True:
    ar1_uno=AR1_UNO(n=n, length=length)
    ar1_uno.generate()
    ar1_uno.discard_transient()
    ts,rts=ar1_uno.save()

if data_star_gno==True:
    star=STAR_GNO(n=n, length=length)
    star.generate()
    star.discard_transient()
    ts,rts=star.save()

if data_arma11_uno==True:
    arma11_uno=ARMA11_UNO(n=n, length=length)
    arma11_uno.generate()
    arma11_uno.discard_transient()
    ts,rts=arma11_uno.save()

if data_nar2==True:
    narma=NonLinearAR2(n=n, length=length)
    narma.generate()
    narma.discard_transient()
    ts,rts=narma.save()

if data_ar3==True:
    ngrp=AR3_Gamma(n=n, length=length)   
    ngrp.generate()
    ngrp.discard_transient()
    ts,rts=ngrp.save()

if data_setar1==True:
    setar=SETAR1_GNO(n=n, length=length)
    setar.generate()
    setar.discard_transient()
    ts,rts=setar.save()

if data_setar2==True:
    setar=SETAR2_GNO(n=n, length=length)
    setar.generate()
    setar.discard_transient()
    ts,rts=setar.save()

if data_arnold==True:
    arnold=ArnoldCat(n=n, length=length)
    arnold.generate()
    arnold.discard_transient()
    ts,rts=arnold.save()

if data_chirikov==True:
    chirikov=ChirikovMap(n=n, length=length)
    chirikov.generate()
    chirikov.discard_transient()
    ts,rts=chirikov.save()

if data_hen==True:
    hen=HEN(n=n, length=length)
    hen.generate()
    hen.discard_transient() 
    ts,rts=hen.save()

if data_logistic4==True:
    logistic=Logistic4(n=n, length=length)
    logistic.generate()
    logistic.discard_transient()
    ts,rts=logistic.save()

if data_logistic38284==True:
    logistic=Logistic38284(n=n, length=length)
    logistic.generate()
    logistic.discard_transient()
    ts,rts=logistic.save()

if data_quadratic==True:
    quadratic=Quadratic(n=n, length=length)
    quadratic.generate()
    quadratic.discard_transient()
    ts,rts=quadratic.save()

if data_hen_sum==True:
    henf=HEN_SUM(n=n, length=length)
    henf.generate()
    henf.discard_transient()
    ts,rts=henf.save()

if data_henr_diverse==True:
    henr=HENR_diverse(n=n, length=length)
    henr.generate()
    henr.discard_transient()
    ts,rts=henr.save()

if data_henr_same==True:
    henr=HENR_same(n=n, length=length)
    henr.generate()
    henr.discard_transient()
    ts,rts=henr.save()

if data_quadratic_rsum==True:
    quadratic_sum=QuadraticRSum(n=n, length=length)
    quadratic_sum.generate()
    quadratic_sum.discard_transient()
    ts,rts=quadratic_sum.save()

if data_llog==True:
    llog=LLOG(n=n, length=length)
    llog.generate()
    llog.discard_transient()
    ts,rts=llog.save()

if data_moda==True:
    moda=MODA(n=n,length=length)
    moda.generate()
    moda.discard_transient()
    ts,rts=moda.save()

if data_sine==True:
    sine=StochasticSineMap(n=n, length=length)
    sine.generate()
    sine.discard_transient()
    ts,rts=sine.save()



