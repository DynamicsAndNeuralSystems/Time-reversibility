# Select the models and operations from the original hctsa df_TS_DataMat_diff used for the analysis, previous to the roubstness
# as the time series have length of 5000 steps

import numpy as np
import pandas as pd
import os


cwd = os.getcwd()

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

# operations (24)
ops = ['AC_nl_001_abs', 'AC_nl_01_abs',
       'AC_nl_001',
       'AC_nl_013',
       'CO_glscf_1_2_1',
       'CO_glscf_1_10_2',
       'CO_StickAngles_y_mean_p',
       'CO_StickAngles_y_skewness_n',
       'CO_Embed2_Basic_1_parabdown05_n1',
       'PH_Walker_biasprop_01_05_w_mean',
       'PH_Walker_prop_05_sw_meanabsdiff',
       'FC_LocalSimple_mean3_gofr2',
       'FC_LocalSimple_mean4_meanabserr',
       'MF_armax_1_1_05_1_normksstat',
       'MF_steps_ahead_ar_2_6_mabserr_1',
       'EX_MovingThreshold_01_01_medianq',
       'NL_MS_nlpe_fnn_mi_normksstat',
       'SB_BinaryStats_diff_diff21stretch1',
       'SB_BinaryStats_diff_diff21stretch0',
       'SB_BinaryStats_diff_meanstretch1',
       'SB_BinaryStats_diff_meanstretch0',
       'SB_MotifTwo_diff_uu',
       'SB_MotifTwo_diff_dd',
       'SB_MotifTwo_diff_u']

dir_data = cwd + '/../../Data_HCTSA/dsct_ACFDS/analysis_removed_CO_TranslateShape/Data_analysis/'

df = pd.read_csv(dir_data + 'df_TS_DataMat_diff.csv')
df.set_index('Model', inplace=True)

# Extract rows models
df = df[df.index.isin(models)]

# Select columns in ops
df = df.loc[:, ops]

print(df.shape)  # (900, 24)

# Save
df.to_csv(cwd + '/Data_analysis/df_TS_DataMat_diff_5000.csv')