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
        hctsa=sprintf('./%s/HCTSA_%s.mat', dire, l);
        load(hctsa);
        
        % Folder check
        folderName = sprintf('./%s/csv_files_%s/', dire, l); 
    
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
        clearvars -except direction leng dire;
    end
end
clear direction
