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

lenght_ts=5000

# Extract path of data, sort data by index, separate forward from backward time series and associate keywords each time series
def extract_index(filename):
    match = re.search(r'(\d{3})', filename)
    return int(match.group()) if match else float('inf')

cwd = os.getcwd()
filepaths=[]
filepaths_frwd=[]
filepaths_bkwd=[]
for model_name in models:
    model_dir = os.path.join(cwd, 'data-tr/time-series/data-cnt', model_name)
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




# Write an input file with both forward and reversed time series INP_ts.txt
cwd=os.getcwd()
input_dir=cwd+'/INP_ts_files_ACFDS'
if not os.path.exists(input_dir):
    os.mkdir(input_dir)
with open(os.path.join(input_dir,f"INP_ts_{lenght_ts}_ACFDS.txt"), 'w') as f:
    for l in filepaths:
        f.write(l + "\n")

# Write an input file with forward time series INP_ts_frwd.txt
with open(os.path.join(input_dir,f"INP_ts_{lenght_ts}_ACFDS_frwd.txt"), 'w') as f:
    for l in filepaths_frwd:
        f.write(l + "\n")

# Write an input file with reversed time series INP_ts_bkwd.txt
with open(os.path.join(input_dir,f"INP_ts_{lenght_ts}_ACFDS_bkwd.txt"), 'w') as f:
    for l in filepaths_bkwd:
        f.write(l + "\n")