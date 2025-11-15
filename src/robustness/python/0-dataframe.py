## python script to build a dataframe with models and operation names starting from TS_DataMat_diff.csv

import numpy as np
import pandas as pd
import os
from pathlib import Path


# folder where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_base = str(BASE_DIR)

REPO_DIR = Path(BASE_DIR).parents[2]

DATA_DIR = REPO_DIR / 'data-tr' / 'robustness-analysis' / 'hctsa'
path_data= str(DATA_DIR)

SAVE_DIR = REPO_DIR / 'data-tr' / 'robustness-analysis' / 'data-analysis'
path_save = str(SAVE_DIR)

if not os.path.exists(path_save):
    os.makedirs(path_save)

# Write down models (same order as the one in INP_file_generation.py)
models = ['AR1_UNO', 'ARMA11_UNO', #ARMA
          'HEN', 'LOGISTIC4', 'QUADRATIC', # chaos
          'HEN_SUM', # sum chaos
          'MODA', 'LLOG', # other deterministic
          'SINE_STOCH'] # other stochastic

model_keywords = {'AR1_UNO': ['irreversible'], 'ARMA11_UNO': ['irreversible'],
                  'HEN': ['irreversible'], 'LOGISTIC4': ['irreversible'], 'QUADRATIC': ['irreversible'],
                  'HEN_SUM': ['irreversible'],
                  'MODA': ['irreversible'], 'LLOG': ['irreversible'],
                  'SINE_STOCH': ['irreversible']}


num_ts=100
# Load the csv files
length = [10, 20, 50, 100, 200, 500, 1000, 2000]
for i in length:
    length_ts = i
    df_ops = pd.read_csv(path_data+f'/hctsa-tot/{length_ts}/csv_files/ops_filter.csv')
    op_Names = df_ops['Name'].tolist()

    #  Create the dataframe
    models_repeated = np.repeat(models, num_ts)

    df_hctsa = pd.read_csv(path_data+f'/hctsa-diff/TS_DataMat_diff_{length_ts}.csv', header=None)
    df_hctsa.columns = op_Names
    df_hctsa['Model'] = models_repeated
    df_hctsa = df_hctsa.set_index('Model')

    # save the dataframe
    df_hctsa.to_csv(path_save+f'/df_TS_DataMat_diff_{length_ts}.csv')
