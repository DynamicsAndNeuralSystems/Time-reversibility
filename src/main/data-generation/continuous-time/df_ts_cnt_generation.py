# Python script to generate dataframes of time series

import pandas as pd
import numpy as np
import os   
import tqdm
import glob

# Length of time series
length=5000 # length of time series
# Current folder
cwd = os.getcwd()
ts_dir=cwd+f'/Data_{length}_ACFDS/'

# Number of time series
num_ts=100

# Models of time series in alphabetical order
models_cnt = ['BRW_cont', 'LORENZ_SUM', 'ROSSLER_SUM', 
              'LORENZ_STOCH_SUM', 'MACKEYGLASS17',
              'Oscillator', 'OU',
              'VDP', 'VDP_STOCH']


# Create forward and backward dataframes with time series

df_ts_frwd=pd.DataFrame()
df_ts_bkwd=pd.DataFrame()

for model in tqdm.tqdm(models_cnt):
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
df_ts_frwd['model'] = [model for model in models_cnt for _ in range(num_ts)]
df_ts_bkwd['model'] = [model for model in models_cnt for _ in range(num_ts)]

df_ts_frwd.set_index(['model'], inplace=True)
df_ts_bkwd.set_index(['model'], inplace=True)

# Save dataframes
df_ts_frwd.to_csv(ts_dir+f'../df_time_series/df_ts_{length}_ACFDS_frwd.csv')
df_ts_bkwd.to_csv(ts_dir+f'../df_time_series/df_ts_{length}_ACFDS_bkwd.csv')