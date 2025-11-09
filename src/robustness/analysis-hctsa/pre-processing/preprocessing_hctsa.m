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

first_run = 0

if first_run == 1

    for i=1:length(leng)
        l = leng{i};
        folderName = sprintf('./hctsa_tot_%s',l); % Specify the folder name

        % Check if the folder exists
        if ~exist(folderName, 'dir')
           % Create the folder if it does not exist
          mkdir(folderName);
         disp(['Folder "', folderName, '" created successfully.']);
        else
            disp(['Folder "', folderName, '" already exists.']);
        end

        % Combine matrices
        file_frwd = sprintf('./frwd/HCTSA_%s.mat', l);
        file_bkwd = sprintf('./bkwd/HCTSA_%s.mat', l);
        file_tot = sprintf('./hctsa_tot_%s/HCTSA.mat', l);
        TS_Combine(file_frwd, file_bkwd, false, false, file_tot);
   
        
        hctsa = sprintf('./hctsa_tot_%s/HCTSA.mat', l);
        load(hctsa);

        % Generate filtered HCTSA matrix
        TS_Normalize('none', [0.7,1], hctsa);
    end

elseif first_run == 0

    for i=1:length(leng)
        l=leng{i};
        % Load filtered matrix
        hctsa = sprintf('./hctsa_tot_%s/HCTSA_N.mat', l);
        load(hctsa);

        % Export full data structures
        folderName = sprintf('./hctsa_tot_%s/csv_files/', l); % Specify the folder name
    
        % Check if the folder exists
        if ~exist(folderName, 'dir')
            % Create the folder if it does not exist
            mkdir(folderName);
            disp(['Folder "', folderName, '" created successfully.']);
        else
            disp(['Folder "', folderName, '" already exists.']);
        end

        disp('Saving files ...');
     
        writetable(MasterOperations, [folderName, 'mops_filter.csv'])
        writetable(Operations, [folderName, 'ops_filter.csv'])
        writetable(TimeSeries, [folderName, 'TimeSeries_filter.csv'])
        writematrix(TS_DataMat, [folderName, 'TS_DataMat_filter.csv'])

        disp('File saved! Now compute the difference HCTSA matrix');

        % Compute difference between forward and backward filtered HCTSA
        % matrices and save TS_DataMat
        idx0_frwd = 1;
        idxend_frwd= 900;
        idx0_bkwd = 901;
        idxend_bkwd = 1800;
    
        TS_DataMat_frwd=TS_DataMat(idx0_frwd:idxend_frwd,:);
        TS_DataMat_bkwd=TS_DataMat(idx0_bkwd:idxend_bkwd,:);
    
        TS_DataMat_diff=TS_DataMat_frwd-TS_DataMat_bkwd;

        % Export total difference matrix

        % Export full data structures
        folderName = sprintf('./hctsa_diff_%s/', l); % Specify the folder name
    
        % Check if the folder exists
        if ~exist(folderName, 'dir')
            % Create the folder if it does not exist
            mkdir(folderName);
            disp(['Folder "', folderName, '" created successfully.']);
        else
            disp(['Folder "', folderName, '" already exists.']);
        end

        disp('Saving file ...');
        writematrix(TS_DataMat_diff, [folderName, 'TS_DataMat_diff.csv']);
    
        disp('All done ;)')
    end

end

 