% -------------------------------------------------------------------------

% Author:       Teresa Dalle Nogare
% Affiliation:  The University of Sydney
% Date:      August 2025

% Summary: Combine frwd and bkwd HCTSA matrices and filter bad performing
% features
% -------------------------------------------------------------------------
%% INITIALIZE HCTSA
% -------------------------------------------------------------------------
run('/Users/tdal0054/hctsa/startup.m');

% -------------------------------------------------------------------------
%% CREATE THE COMBINED HCTSA RAW MATRIX (frwd, bkwd) 
% -------------------------------------------------------------------------

leng={'10', '20', '50', '100', '200', '500', '1000', '2000'};

first_run = 0;

if first_run == 1
base_path = fullfile('../../../../data-tr/robustness-analysis/hctsa/');

folder_frwd = 'hctsa-frwd'; 
folder_bkwd = 'hctsa-bkwd';
folder_tot = fullfile(base_path, 'hctsa-tot'); 
% Check if the folder exists
if ~exist(folder_tot, 'dir')
    % Create the folder if it does not exist
    mkdir(folder_tot);
    disp(['Folder "', folder_tot, '" created successfully.']);
else
    disp(['Folder "', folder_tot, '" already exists.']);
end

    for i=1:length(leng)
        l = leng{i};
        folder_len = fullfile(folder_tot, sprintf('%s', l));

        if ~exist(folder_len, 'dir')
            % Create the folder if it does not exist
            mkdir(folder_len);
            disp(['Folder "', folder_len, '" created successfully.']);
        else
            disp(['Folder "', folder_len, '" already exists.']);
        end
        
        % Combine matrices
        path_frwd = fullfile(base_path, folder_frwd, sprintf('HCTSA_%s.mat', l));
        path_bkwd = fullfile(base_path, folder_bkwd, sprintf('HCTSA_%s.mat', l));
        file_tot = fullfile(folder_len, sprintf('HCTSA_%s.mat', l));

        
        
        TS_Combine(path_frwd, path_bkwd, false, false, file_tot);
        
        hctsa = file_tot;
        load(hctsa);

        % Generate filtered HCTSA matrix
        TS_Normalize('none', [0.7,1], hctsa);
    end

elseif first_run == 0

    for i=1:length(leng)
        l=leng{i};
        base_path = fullfile('../../../../data-tr/robustness-analysis/hctsa/');

        folder_tot = fullfile(base_path, 'hctsa-tot'); 
        hctsa = fullfile(folder_tot, sprintf('%s/HCTSA_%s_N.mat', l, l));
        load(hctsa);

        % Export full data structures
        csv_folder = fullfile(folder_tot, sprintf('%s/csv_files', l)); 
    
    
        % Check if the folder exists
        if ~exist(csv_folder, 'dir')
            % Create the folder if it does not exist
            mkdir(csv_folder);
            disp(['Folder "', csv_folder, '" created successfully.']);
        else
            disp(['Folder "', csv_folder, '" already exists.']);
        end

        disp('Saving files ...');
     
        writetable(MasterOperations, fullfile(csv_folder, 'mops_filter.csv'))
        writetable(Operations, fullfile(csv_folder, 'ops_filter.csv'))
        writetable(TimeSeries, fullfile(csv_folder, 'TimeSeries_filter.csv'))
        writematrix(TS_DataMat, fullfile(csv_folder, 'TS_DataMat_filter.csv'))

        disp('File saved! Now compute the difference HCTSA matrix');

        % Compute difference between forward and backward filtered HCTSA
        % matrices and save TS_DataMat
        idx0_frwd = 1;
        idxend_frwd= 900; % change based on the number of time series considered
        idx0_bkwd = 901;
        idxend_bkwd = 1800; % change based on the number of time series considered
    
        TS_DataMat_frwd=TS_DataMat(idx0_frwd:idxend_frwd,:);
        TS_DataMat_bkwd=TS_DataMat(idx0_bkwd:idxend_bkwd,:);
    
        TS_DataMat_diff=TS_DataMat_frwd-TS_DataMat_bkwd;

        % Export total difference matrix

        % Export full data structures
        folderName = fullfile(base_path, 'hctsa-diff/');
    
        % Check if the folder exists
        if ~exist(folderName, 'dir')
            % Create the folder if it does not exist
            mkdir(folderName);
            disp(['Folder "', folderName, '" created successfully.']);
        else
            disp(['Folder "', folderName, '" already exists.']);
        end

        disp('Saving file ...');
        writematrix(TS_DataMat_diff, fullfile(folderName, sprintf('TS_DataMat_diff_%s.csv', l)));
    
        disp('All done ;)')
    end

end

 