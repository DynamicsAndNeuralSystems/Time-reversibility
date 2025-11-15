% -------------------------------------------------------------------------

% Author:       Teresa Dalle Nogare
% Affiliation:  The University of Sydney
% Date:      August 2025

% Summary: Export csv of raw HCTSA matrix and related content.

% -------------------------------------------------------------------------

direction={'frwd', 'bkwd'};
leng={'10', '20', '50', '100', '200', '500', '1000', '2000'};

for i=1:length(direction)
    dire=direction{i};
    disp(['Direction is ', dire])
    for j=1:length(leng)
        % Load HCTSA.mat
        l=leng{j};
        base_path = fullfile(sprintf('../../../../data-tr/robustness-analysis/hctsa/%s', dire));
        hctsa=sprintf('HCTSA_%s.mat', l);
        hctsa_path = fullfile(base_path, hctsa);
        load(hctsa_path);
        
        % Folder check
        folderName = sprintf('../../../../data-tr/robustness-analysis/hctsa/%s/csv_files_%s/', dire, l); 
        csv_path = fullfile(base_path, folderName);

        % Check if the folder exists
        if ~exist(csv_path, 'dir')
            % Create the folder if it does not exist
            mkdir(csv_path);
            disp(['Folder "', csv_path, '" created successfully.']);
        else
            disp(['Folder "', csv_path, '" already exists.']);
        end
        
        % Write csv files
        disp('Printing HCTSA content in csv file')
        writetable(MasterOperations, [csv_path 'mops.csv'])
        writetable(Operations, [csv_path 'ops.csv'])
        writetable(TimeSeries, [csv_path 'TimeSeries.csv'])
        writematrix(TS_CalcTime, [csv_path 'TS_CalcTime.csv'])
        writematrix(TS_DataMat, [csv_path 'TS_DataMat.csv'])
        writematrix(TS_Quality, [csv_path 'TS_Quality.csv'])
    
        disp('Ended printing')
        disp('Now clearing past variables')
        clearvars -except direction leng dire;
    end
end
clear direction
