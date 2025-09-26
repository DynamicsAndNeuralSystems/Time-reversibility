# Python script to generate dataframes of time series

import pandas as pd
import numpy as np
import os   
import tqdm
import glob

# Length of time series
length=2000 # length of time series
# Current folder
cwd = os.getcwd()
ts_dir=cwd+'/Data_2000_dsct/'

# Number of time series
num_ts=100

# Models of time series in alphabetical order
models_dsct = ['AR1_GNO', 'ARNOLD', 'AR1_UNO', 'ARMA11_UNO', 'AR3_Gamma',
               'BROWN',  
               'CHIRIKOV',
               'GNO', 
               'HEN', 'HEN_SUM', 'HENR_diverse', 'HENR_same',
               'LLOG', 'LOGISTIC4', 'LOGISTIC38284',
               'MODA',
               'N_AR2', 
               'PINK', 
               'QUADRATIC', 'QUADRATIC_RSUM',
               'SETAR1_GNO', 'SETAR2_GNO', 'SINE_STOCH', 'STAR_GNO',
               'UNO', 'VIOLET']


# Create forward and backward dataframes with time series

df_ts_frwd=pd.DataFrame()
df_ts_bkwd=pd.DataFrame()

for model in tqdm.tqdm(models_dsct):
    print(model)
    ts_files = glob.glob(ts_dir+f'{model}/{model}_*.txt')
    ts_files_bkwd = glob.glob(ts_dir+f'{model}/{model}_reverse_*.txt')
    ts_files_frwd = [ts_file for ts_file in ts_files if 'reverse' not in ts_file]

    # Sort
    ts_files_frwd.sort()
    ts_files_bkwd.sort()

    # Read and concatenate
    for file in ts_files_frwd:
        ts_file=pd.read_csv(file, header=None).T
        df_ts_frwd = pd.concat([df_ts_frwd,ts_file] , axis=0)

    for file in ts_files_bkwd:
        ts_file=pd.read_csv(file, header=None).T
        df_ts_bkwd = pd.concat([df_ts_bkwd, ts_file], axis=0)
    print(len(df_ts_bkwd.columns))
        
# Set model as index
df_ts_frwd['model'] = [model for model in models_dsct for _ in range(num_ts)]
df_ts_bkwd['model'] = [model for model in models_dsct for _ in range(num_ts)]

df_ts_frwd.set_index(['model'], inplace=True)
df_ts_bkwd.set_index(['model'], inplace=True)

# Save dataframes
df_ts_frwd.to_csv(ts_dir+f'../df_time_series/df_ts_{length}_dsct_frwd.csv')
df_ts_bkwd.to_csv(ts_dir+f'../df_time_series/df_ts_{length}_dsct_bkwd.csv')