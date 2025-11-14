% -------------------------------------------------------------------------

% Author:       Teresa Dalle Nogare
% Affiliation:  The University of Sydney
% Date:      February 2025

% Summary: Combine frwd and bkwd HCTSA matrices and filter bad performing
% features
% -------------------------------------------------------------------------
%% INITIALIZE HCTSA
% -------------------------------------------------------------------------

%path_to_hctsa = XXX % path to hctsa folder
%run(path_to_hctsa);
run('/Users/tdal0054/hctsa/startup.m');

% -------------------------------------------------------------------------
%% CREATE THE COMBINED HCTSA RAW MATRIX (frwd, bkwd) 
% -------------------------------------------------------------------------

first_run = 0
data_types = {'dsct', 'cnt'};

if first_run == 1

    for k=1:length(data_types)
        data_type = data_types{k};
        base_path = fullfile('../../../../data-tr/main-analysis/hctsa');
        folder = sprintf('hctsa-%s', data_type);
        folderName = fullfile(base_path, folder, '/hctsa_tot'); % Specify the folder name
    
        % Check if the folder exists
        if ~exist(folderName, 'dir')
            % Create the folder if it does not exist
            mkdir(folderName);
            disp(['Folder "', folderName, '" created successfully.']);
        else
            disp(['Folder "', folderName, '" already exists.']);
        end
        
        path_frwd = fullfile(base_path, folder, './HCTSA_frwd.mat');
        path_bkwd = fullfile(base_path, folder, './HCTSA_bkwd.mat');
        fileName = fullfile(folderName, '/HCTSA.mat');

        % Combine matrices
        TS_Combine(path_frwd, path_bkwd, false, false, fileName);
    
        hctsa = fileName;
        load(hctsa);
    
        % Generate filtered HCTSA matrix
        TS_Normalize('none', [0.7,1], hctsa);

    end

elseif first_run == 0
    for k=1:length(data_types)
        % Load filtered matrix
        data_type = data_types{k};
        base_path = fullfile('../../../../data-tr/main-analysis/hctsa');
        folder = sprintf('hctsa-%s', data_type);
        folderName = fullfile(base_path, folder, '/hctsa_tot'); % Specify the folder name
        hctsa = fullfile(folderName, '/HCTSA_N.mat');

        load(hctsa);
    
        % Export full data structures
        csv_folder = fullfile(folderName,'/csv_files' ); % Specify the folder name
        
        % Check if the folder exists
        if ~exist(csv_folder, 'dir')
            % Create the folder if it does not exist
            mkdir(csv_folder);
            disp(['Folder "', csv_folder, '" created successfully.']);
        else
            disp(['Folder "', csv_folder, '" already exists.']);
        end
    
        disp('Saving files ...');
         
        writetable(MasterOperations, fullfile(csv_folder, '/mops_filter.csv'))
        writetable(Operations, fullfile(csv_folder, '/ops_filter.csv'))
        writetable(TimeSeries, fullfile(csv_folder, '/TimeSeries_filter.csv'))
        writematrix(TS_DataMat, fullfile(csv_folder, '/TS_DataMat_filter.csv'))
    
        disp('File saved! Now compute the difference HCTSA matrix');
    
        % Compute difference between forward and backward filtered HCTSA
        % matrices and save TS_DataMat
        if k==1
            idx0_frwd = 1;
            idxend_frwd= 2600; % change according to number of frwd time series
            idx0_bkwd = 2601; % change according to number of bkwd time series
            idxend_bkwd = 5200;
        
        elseif k == 2
            idx0_frwd = 1;
            idxend_frwd= 900; % change according to number of frwd time series
            idx0_bkwd = 901; % change according to number of bkwd time series
            idxend_bkwd = 1800;
        

        end
        
        TS_DataMat_frwd=TS_DataMat(idx0_frwd:idxend_frwd,:);
        TS_DataMat_bkwd=TS_DataMat(idx0_bkwd:idxend_bkwd,:);
        
        TS_DataMat_diff=TS_DataMat_frwd-TS_DataMat_bkwd;
    
        % Export total difference matrix
    
        % Export full data structures
        folderName = fullfile(base_path, folder, '/hctsa_diff'); % Specify the folder name
        
        % Check if the folder exists
        if ~exist(folderName, 'dir')
            % Create the folder if it does not exist
            mkdir(folderName);
            disp(['Folder "', folderName, '" created successfully.']);
        else
            disp(['Folder "', folderName, '" already exists.']);
        end
    
        disp('Saving file ...');
        writematrix(TS_DataMat_diff, fullfile(folderName, '/TS_DataMat_diff.csv'));
        
        disp('All done ;)')
    end

end

 