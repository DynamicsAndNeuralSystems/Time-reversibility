% -------------------------------------------------------------------------

% Author:       Teresa Dalle Nogare
% Affiliation:  The University of Sydney
% Date:      February 2025

% Summary: Export csv of raw HCTSA matrix and related content.

% -------------------------------------------------------------------------
clear all


direction={'frwd', 'bkwd'};
data_types={'dsct', 'cnt'}; % discrete time and continuous time

for k=1:length(data_types)
    data_type=data_types{k};
    
    for i=1:length(direction)
        dir=direction{i};
        disp(['Direction: ', dir, ' Type: ', data_type]);
        % Load HCTSA.mat
        base_path = fullfile('../../../../data-tr/main-analysis/hctsa');
        folder_name = sprintf('hctsa-%s', data_type);
        file_name = sprintf('HCTSA_%s.mat', dir);
        hctsa_path = fullfile(base_path, folder_name, file_name);

        load(hctsa_path);
        
        % Folder check
        base_path = fullfile('../../../../data-tr/main-analysis/hctsa');
        folder_name1 = sprintf('hctsa-%s', data_type);
        folder_name2 = sprintf('csv_files_%s', dir); 
        csv_path = fullfile(base_path, folder_name1, folder_name2);
    
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
        writetable(MasterOperations, [csv_path '/mops.csv'])
        writetable(Operations, [csv_path '/ops.csv'])
        writetable(TimeSeries, [csv_path '/TimeSeries.csv'])
        writematrix(TS_CalcTime, [csv_path '/TS_CalcTime.csv'])
        writematrix(TS_DataMat, [csv_path '/TS_DataMat.csv'])
        writematrix(TS_Quality, [csv_path '/TS_Quality.csv'])
    
        disp('Ended printing')
    
    end
       
end

