## python script to build a dataframe with models and operation names starting from TS_DataMat_diff.csv

import numpy as np
import pandas as pd
import os
from pathlib import Path


# folder where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REPO_DIR = Path(BASE_DIR).parents[2]

DATA_DIR = REPO_DIR / 'data-tr' / 'main-analysis' / 'hctsa' / 'hctsa-cnt'
print(DATA_DIR)
path_data= str(DATA_DIR)

SAVE_DIR = REPO_DIR / 'data-tr' / 'main-analysis' / 'data-analysis'
print(SAVE_DIR)
path_save= str(SAVE_DIR)

 

# Write down models (same order as the one in INP_file_generation.py)
models = ['BRW_cont','OU', 'Oscillator', 
              'LORENZ_SUM', 'ROSSLER_SUM', 
              'MACKEYGLASS17', 'VDP', 
              'LORENZ_STOCH_SUM',
                'VDP_STOCH']


model_keywords={ 'BRW_cont': ['reversible'], 'OU': ['reversible'], 'Oscillator': ['reversible'],
                 'LORENZ_SUM': ['irreversible'], 'ROSSLER_SUM': ['irreversible'],
                 'MACKEYGLASS17': ['irreversible'], 'VDP': ['irreversible'],
                 'LORENZ_STOCH_SUM': ['irreversible'],
                 'VDP_STOCH': ['irreversible']
        }


# Load the csv files
df_ops = pd.read_csv(path_data+'/hctsa_tot/csv_files/ops_filter.csv')
op_Names = df_ops['Name'].tolist()

# Create the dataframe
num_ts=100
models_repeated = np.repeat(models, num_ts)

df_hctsa = pd.read_csv(path_data+'/hctsa_diff/TS_DataMat_diff.csv', header=None)
df_hctsa.columns = op_Names
df_hctsa['Model'] = models_repeated
df_hctsa = df_hctsa.set_index('Model')

# save the dataframe (change path)
os.makedirs(path_save, exist_ok=True)
df_hctsa.to_csv(path_save+'/df_TS_DataMat_diff_cnt.csv')




