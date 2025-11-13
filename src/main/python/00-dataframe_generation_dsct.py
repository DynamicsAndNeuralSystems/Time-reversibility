## python script to build a dataframe with models and operation names starting from TS_DataMat_diff.csv

import numpy as np
import pandas as pd
import os


cwd = os.getcwd()

# Write down models (same order as the one in INP_file_generation.py)
models=['GNO', 'UNO', 'PINK', 'BROWN', 'VIOLET', # noises (R)
        'AR1_GNO', 'STAR_GNO', #    ARMA (R)
        'ARNOLD', 'CHIRIKOV', # Conservative chaotic maps (R)
        'HENR_diverse', 'HENR_same', 'QUADRATIC_RSUM', # Sum of frwd and bckwd realisations of chaotic maps (R)
        'AR1_UNO', 'ARMA11_UNO', 'AR3_Gamma', 'N_AR2', 'SETAR1_GNO', 'SETAR2_GNO',
        'HEN', 'HEN_SUM', 'LOGISTIC4', 'LOGISTIC38284', 'QUADRATIC', # Chaotic maps (I)
        'MODA', 'LLOG', # Other deterministic (I)
        'SINE_STOCH' # Other stochastic (I)
        ]

model_keywords={'GNO': ['reversible'], 'UNO': ['reversible'], 'PINK': ['reversible'], 'BROWN': ['reversible'], 'VIOLET': ['reversible'],
                'AR1_GNO': ['reversible'], 'STAR_GNO': ['reversible'],
                'ARNOLD': ['reversible'], 'CHIRIKOV': ['reversible'],
                'HENR_diverse': ['reversible'], 'HENR_same': ['reversible'], 'QUADRATIC_RSUM': ['reversible'],
                'AR1_UNO': ['irreversible'], 'ARMA11_UNO': ['irreversible'], 'AR3_Gamma': ['irreversible'], 'N_AR2': ['irreversible'], 'SETAR1_GNO': ['irreversible'], 'SETAR2_GNO': ['irreversible'], 
                'HEN': ['irreversible'], 'HEN_SUM': ['irreversible'], 'LOGISTIC4': ['irreversible'], 'LOGISTIC38284': ['irreversible'],'QUADRATIC': ['irreversible'],
                'MODA': ['irreversible'], 'LLOG': ['irreversible'],
                'SINE_STOCH': ['irreversible']}


# Load the csv files
df_ops = pd.read_csv(cwd+'/../../../data-tr/main-analysis/hctsa/hctsa-dsct/hctsa_tot/csv_files/ops_filter.csv')
op_Names = df_ops['Name'].tolist()

# Create the dataframe
num_ts=100
models_repeated = np.repeat(models, num_ts)

df_hctsa = pd.read_csv(cwd+'/../../../data-tr/main-analysis/hctsa/hctsa-dsct/hctsa_diff/TS_DataMat_diff.csv', header=None)
df_hctsa.columns = op_Names
df_hctsa['Model'] = models_repeated
df_hctsa = df_hctsa.set_index('Model')

# save the dataframe
os.makedirs(cwd+'/./data-analysis/', exist_ok=True)
df_hctsa.to_csv(cwd+'/./data-analysis/df_TS_DataMat_diff_dsct.csv')




