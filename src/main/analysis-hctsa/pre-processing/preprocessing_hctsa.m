% -------------------------------------------------------------------------

% Author:       Teresa Dalle Nogare
% Affiliation:  The University of Sydney
% Date:      February 2025

% Summary: Combine frwd and bkwd HCTSA matrices and filter bad performing
% features
% -------------------------------------------------------------------------
%% INITIALIZE HCTSA
% -------------------------------------------------------------------------
run('/Users/tdal0054/hctsa/startup.m');

% -------------------------------------------------------------------------
%% CREATE THE COMBINED HCTSA RAW MATRIX (frwd, bkwd) 
% -------------------------------------------------------------------------

first_run = 0

if first_run == 1
    folderName = './hctsa_tot'; % Specify the folder name

    % Check if the folder exists
    if ~exist(folderName, 'dir')
        % Create the folder if it does not exist
        mkdir(folderName);
        disp(['Folder "', folderName, '" created successfully.']);
    else
        disp(['Folder "', folderName, '" already exists.']);
    end

    % Combine matrices
    TS_Combine('./hctsa_frwd/HCTSA.mat', './hctsa_bkwd/HCTSA.mat', false, false, './hctsa_tot/HCTSA.mat');

    hctsa = './hctsa_tot/HCTSA.mat';
    load(hctsa);

    % Generate filtered HCTSA matrix
    TS_Normalize('none', [0.7,1], hctsa);

elseif first_run == 0
    % Load filtered matrix
    hctsa = './hctsa_tot/HCTSA_N.mat';
    load(hctsa);

    % Export full data structures
    folderName = './hctsa_tot/csv_files'; % Specify the folder name
    
    % Check if the folder exists
    if ~exist(folderName, 'dir')
        % Create the folder if it does not exist
        mkdir(folderName);
        disp(['Folder "', folderName, '" created successfully.']);
    else
        disp(['Folder "', folderName, '" already exists.']);
    end

    disp('Saving files ...');
     
    writetable(MasterOperations, './hctsa_tot/csv_files/mops_filter.csv')
    writetable(Operations, './hctsa_tot/csv_files/ops_filter.csv')
    writetable(TimeSeries, './hctsa_tot/csv_files/TimeSeries_filter.csv')
    writematrix(TS_DataMat, './hctsa_tot/csv_files/TS_DataMat_filter.csv')

    disp('File saved! Now compute the difference HCTSA matrix');

    % Compute difference between forward and backward filtered HCTSA
    % matrices and save TS_DataMat
    idx0_frwd = 1;
    idxend_frwd= 2600;
    idx0_bkwd = 2601;
    idxend_bkwd = 5200;
    
    TS_DataMat_frwd=TS_DataMat(idx0_frwd:idxend_frwd,:);
    TS_DataMat_bkwd=TS_DataMat(idx0_bkwd:idxend_bkwd,:);
    
    TS_DataMat_diff=TS_DataMat_frwd-TS_DataMat_bkwd;

    % Export total difference matrix

    % Export full data structures
    folderName = './hctsa_diff'; % Specify the folder name
    
    % Check if the folder exists
    if ~exist(folderName, 'dir')
        % Create the folder if it does not exist
        mkdir(folderName);
        disp(['Folder "', folderName, '" created successfully.']);
    else
        disp(['Folder "', folderName, '" already exists.']);
    end

    disp('Saving file ...');
    writematrix(TS_DataMat_diff, './hctsa_diff/TS_DataMat_diff.csv');
    
    disp('All done ;)')

end

 