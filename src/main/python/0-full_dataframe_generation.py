# Author: Teresa Dalle Nogare
# Year: 2025
# 
# Notes: Script to generate the full dataset of discrete time and ACFDS continuous processes

import numpy as np
import os
import pandas as pd


# Write processes in same order as in the INP_generation files 
# Discrete time models
models_dsct=['GNO', 'UNO', 'PINK', 'BROWN', 'VIOLET', # noises (R)
        'AR1_GNO', 'STAR_GNO', #    ARMA (R)
        'ARNOLD', 'CHIRIKOV', # Conservative chaotic maps (R)
        'HENR_diverse', 'HENR_same', 'QUADRATIC_RSUM', # Sum of frwd and bckwd realisations of chaotic maps (R)
        'AR1_UNO', 'ARMA11_UNO', 'AR3_Gamma', 'N_AR2', 'SETAR1_GNO', 'SETAR2_GNO',
        'HEN', 'HEN_SUM', 'LOGISTIC4', 'LOGISTIC38284', 'QUADRATIC', # Chaotic maps (I)
        'MODA', 'LLOG', # Other deterministic (I)
        'SINE_STOCH' # Other stochastic (I)
        ]

# Continuous time models
models_cnt = ['BRW_cont','OU', 'Oscillator', 
              'LORENZ_SUM', 'ROSSLER_SUM', 
              'MACKEYGLASS17', 'VDP', 
              'LORENZ_STOCH_SUM',
                'VDP_STOCH']

models = models_dsct + models_cnt

# Generate a single HCTSA dictionary with all processes
cwd = os.getcwd()

# Directories of the hctsa diff dataframe created for the single classes of processes
dir_data = cwd+'/data-analysis/'


# Read dsct and cnt diff datasets
df_hctsa_dsct=pd.read_csv(dir_data+'df_TS_DataMat_diff_dsct.csv')
df_hctsa_dsct.set_index(['Model'], inplace=True)

df_hctsa_cnt=pd.read_csv(dir_data+'df_TS_DataMat_diff_cnt.csv')
df_hctsa_cnt.set_index(['Model'], inplace=True)

# Extract common operations between the two datasets
common_ops = list(set(df_hctsa_dsct.columns) & set(df_hctsa_cnt.columns))

# Select only the common operations from the two datasets
df_hctsa_dsct_common = df_hctsa_dsct[common_ops]
df_hctsa_cnt_common = df_hctsa_cnt[common_ops]

df_hctsa = pd.concat([df_hctsa_dsct_common, df_hctsa_cnt_common], axis=0, ignore_index=True) # Concatenates based on column name, not order of columns
# Discard CO_TranslateShape operations (possible mistake iin implementation)
df_hctsa = df_hctsa.loc[:, ~df_hctsa.columns.str.contains('CO_TranslateShape')]
# also from common_ops
common_ops = [op for op in common_ops if 'CO_TranslateShape' not in op]

num_ts = 100
models_repeat = np.repeat(models, num_ts)
df_hctsa = df_hctsa.copy() # to avoid PerformanceWarning
df_hctsa['Model'] = models_repeat
df_hctsa = df_hctsa.set_index('Model')

# Save common operations and hctsa
df_hctsa.to_csv(dir_data+'df_TS_DataMat_diff.csv', index=True)
df_common_ops = pd.DataFrame(common_ops, columns=['Name'])
df_common_ops.to_csv(dir_data+'common_ops.csv', index=False)