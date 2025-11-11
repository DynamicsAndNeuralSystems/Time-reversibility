% -------------------------------------------------------------------------

% Author:       Teresa Dalle Nogare
% Affiliation:  The University of Sydney
% Date:         June 2025

% Summary: Compute HCTSA on input dataset

% -------------------------------------------------------------------------
%% INITIALIZE HCTSA
% -------------------------------------------------------------------------
run('/Users/tdal0054/hctsa/startup.m')

% -------------------------------------------------------------------------
%% INITIALISE DATASET
% -------------------------------------------------------------------------
data='./INP_ts_files/INP_ts_20_dsct_frwd.txt';
log_file='./log_hctsa.txt';

% 1x2 cell with mops and ops file names
cell_mops_ops={'INP_mops_good_small.txt', 'INP_ops_good_small.txt'};

diary(log_file)
% -------------------------------------------------------------------------
%%  READ INPUT FILE AND INITIALZE HCTSA
% -------------------------------------------------------------------------
% Read input file and initialize HCTSA.mat
TS_Init(data, cell_mops_ops,false)

% Looping over a hctsa analysis and saving every 5 time series(already initialized)
sample_runscript_matlab(true, 5, 'HCTSA.mat')

diary off