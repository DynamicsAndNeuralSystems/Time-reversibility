#################################################################
#                                                               #
#   Author:   Teresa Dalle Nogare                               #
#   Date:     February 2025                                     #
#                                                               #
#   Summary:  Code to generate the input .txt file to give      #
#             in input to hctsa                                 #
#             It is of the type:                                #
#             [label_ts_idx.txt       keyword]                  #
#             It contains both forward and backward             #
#             time series                                       #
#                                                               #
#################################################################

import os
import re

# Define models and keywords for the input file INP_ts.txt

# We consider only a subset of irreversible models
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
length_ts_vals = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
 
# Extract path of data, sort data by index, separate forward from backward time series and associate keywords each time series
def extract_index(filename):
    match = re.search(r'(\d{3})', filename)
    return int(match.group()) if match else float('inf')

cwd = os.getcwd()
dict_filepaths={}
dict_filepaths_frwd={}
dict_filepaths_bkwd={}
for length_ts in length_ts_vals:

    filepaths=[]
    filepaths_frwd=[]
    filepaths_bkwd=[]
    for model_name in models:
        model_dir = os.path.join(cwd, f'data-tr/robustness-analysis/time-series/Data_{length_ts}_dsct', model_name)
        files = os.listdir(model_dir)   #list all files and directories in a directory
        files = sorted(files, key=lambda f: extract_index(f))   #sort by index
        files_frwd = [file for file in files if 'reverse' not in os.path.basename(file)]    #forward time series
        files_bkwd = [file for file in files if 'reverse' in os.path.basename(file)]    #backward time series
        srtd_files= files_frwd+files_bkwd
        srtd_files = [os.path.join(model_dir, file) for file in srtd_files]   #constructs the full paths for each file in the files list
        srtd_files = [fp + '    ' + ','.join(model_keywords[model_name]) for fp in srtd_files]  # add the corresponding keyword associated to the model 
        filepaths += srtd_files

        files_frwd = [os.path.join(model_dir, file) for file in files_frwd]
        files_frwd = [fp + '    ' + ','.join(model_keywords[model_name]) for fp in files_frwd]
        filepaths_frwd += files_frwd

        files_bkwd = [os.path.join(model_dir, file) for file in files_bkwd]
        files_bkwd = [fp + '    ' + ','.join(model_keywords[model_name]) for fp in files_bkwd]
        filepaths_bkwd += files_bkwd

    dict_filepaths[length_ts]=filepaths
    dict_filepaths_frwd[length_ts]=filepaths_frwd
    dict_filepaths_bkwd[length_ts]=filepaths_bkwd




input_dir=cwd+'/src/robustness/analysis-hctsa/run/INP_ts_files'
if not os.path.exists(input_dir):
    os.mkdir(input_dir)

for length_ts in length_ts_vals:
    filepaths=dict_filepaths[length_ts]
    filepaths_frwd=dict_filepaths_frwd[length_ts]
    filepaths_bkwd=dict_filepaths_bkwd[length_ts]
            
    # Write an input file with forward time series INP_ts_frwd.txt
    with open(os.path.join(input_dir,f"INP_ts_dsct_frwd_{length_ts}.txt"), 'w') as f:
        for l in filepaths_frwd:
            f.write(l + "\n")
    # Write an input file with reversed time series INP_ts_bkwd.txt
    with open(os.path.join(input_dir,f"INP_ts_dsct_bkwd_{length_ts}.txt"), 'w') as f:
        for l in filepaths_bkwd:
            f.write(l + "\n")