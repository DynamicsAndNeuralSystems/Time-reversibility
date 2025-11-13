% -------------------------------------------------------------------------

% Author:       Teresa Dalle Nogare
% Affiliation:  The University of Sydney
% Date:      February 2025

% Summary: Export csv of raw HCTSA matrix and related content.

% -------------------------------------------------------------------------

direction={'frwd', 'bkwd'};

dir_data = '../../../data-tr/main-analysis/hctsa'
for i=1:length(direction)
    dir=direction{i};
    disp(['Direction is ', dir])

    % Load HCTSA.mat
    hctsa=sprintf('HCTSA.mat', dir);
    load(hctsa);
    
    % Folder check
    folderName = sprintf('./hctsa_%s/csv_files/', dir); 

    % Check if the folder exists
    if ~exist(folderName, 'dir')
        % Create the folder if it does not exist
        mkdir(folderName);
        disp(['Folder "', folderName, '" created successfully.']);
    else
        disp(['Folder "', folderName, '" already exists.']);
    end
    
    % Write csv files
    disp('Printing HCTSA content in csv file')
    writetable(MasterOperations, [folderName 'mops.csv'])
    writetable(Operations, [folderName 'ops.csv'])
    writetable(TimeSeries, [folderName 'TimeSeries.csv'])
    writematrix(TS_CalcTime, [folderName 'TS_CalcTime.csv'])
    writematrix(TS_DataMat, [folderName 'TS_DataMat.csv'])
    writematrix(TS_Quality, [folderName 'TS_Quality.csv'])

    disp('Ended printing')
    disp('Now clearing past variables')
    clearvars -except direction;

end
clear direction
