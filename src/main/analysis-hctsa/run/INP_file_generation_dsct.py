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
    model_dir = os.path.join(cwd, 'data-tr/time-series/data-dsct', model_name)
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
input_dir=cwd+'/src/main/analysis-hctsa/run/INP_ts_files'
if not os.path.exists(input_dir):
    os.mkdir(input_dir)


# Write an input file with forward time series INP_ts_frwd.txt
with open(os.path.join(input_dir,f"INP_ts_dsct_frwd.txt"), 'w') as f:
    for l in filepaths_frwd:
        f.write(l + "\n")

# Write an input file with reversed time series INP_ts_bkwd.txt
with open(os.path.join(input_dir,f"INP_ts_dsct_bkwd.txt"), 'w') as f:
    for l in filepaths_bkwd:
        f.write(l + "\n")