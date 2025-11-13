% -------------------------------------------------------------------------

% Author:       Teresa Dalle Nogare
% Affiliation:  The University of Sydney
% Date:      April 2025

% Summary: Compute HCTSA on input dataset

% -------------------------------------------------------------------------
%% INITIALIZE HCTSA
% -------------------------------------------------------------------------

% Load paths for the hctsa package:
myStartingDir = pwd;

% Load paths for the hctsa package:
path = % set path to hctsa directory
cd(path)
startup

% Move Matlab back to the working PBS directory
cd(myStartingDir);

% -------------------------------------------------------------------------
%% INITIALISE DATASET
% -------------------------------------------------------------------------
data='./INP_ts_5000_dsct_bkwd.txt';
log_file='./log_hctsa_init_bkwd.txt';

cell_mops_ops={'INP_mops.txt', 'INP_ops.txt'};

diary(log_file)
% -------------------------------------------------------------------------
%%  READ INPUT FILE AND INITIALZE HCTSA
% -------------------------------------------------------------------------
TS_Init(data, cell_mops_ops, false)

diary off
