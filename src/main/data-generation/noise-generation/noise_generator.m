clear, clc, close all
     
% Parameters
% Parameters
m = 1;        % number of the rows of the noise matrix (number of time series) keep 1 for 1 time series per file
n = 7000;     % number of the columns of the noise matrix (time series length - transient+dynamics to analyse)
idx0 = 5001;   % number of points to cut (transient dynamics)

path_folder = sprintf('../../../../data-tr/main-analysis/time-series/data-dsct'); % XXXX length of time series
%%% Pink noise
% Generate folder if it does not exist with the name of the process 
pathToSave = path_folder
folderName = 'PINK';

pathNewFolder = fullfile(pathToSave, folderName);

if ~exist(pathNewFolder, 'dir')
    mkdir(pathNewFolder);
    disp(['Folder "', folderName, '" has been created.']);
else
    disp(['Folder "', folderName, '" already exists.']);
end

for i=0:99
    
    filename = sprintf('%s_%03d.txt', folderName, i);
    filename_rev = sprintf('%s_reverse_%03d.txt', folderName, i);
    fullfilename = fullfile(pathNewFolder, filename);
    fullfilename_rev = fullfile(pathNewFolder, filename_rev);

    % Generate noise time series
    x = pinknoise(m, n); 

    % Cut first idx0 part of the time series
    x_cut = x(idx0:end);

    % Transform in a coumn vector to save 
    x_noise = x_cut';
    x_reverse = flip(x_noise);

    writematrix(x_noise, fullfilename);
    writematrix(x_reverse, fullfilename_rev);
    
end

%%% Brownian noise (red noise)

% Generate folder if it does not exist with the name of the process 
pathToSave = path_folder
folderName = 'BROWN';

pathNewFolder = fullfile(pathToSave, folderName);

if ~exist(pathNewFolder, 'dir')
    mkdir(pathNewFolder);
    disp(['Folder "', folderName, '" has been created.']);
else
    disp(['Folder "', folderName, '" already exists.']);
end

for i=0:99
    
    filename = sprintf('%s_%03d.txt', folderName, i);
    filename_rev = sprintf('%s_reverse_%03d.txt', folderName, i);
    fullfilename = fullfile(pathNewFolder, filename);
    fullfilename_rev = fullfile(pathNewFolder, filename_rev);

    % Generate noise time series
    x = rednoise(m, n); 

    % Cut first idx0 part of the time series
    x_cut = x(idx0:end);

    % Transform in a coumn vector to save 
    x_noise = x_cut';
    x_reverse = flip(x_noise);

    writematrix(x_noise, fullfilename);
    writematrix(x_reverse, fullfilename_rev);
    
end

%%% Violet nosie

% Generate folder if it does not exist with the name of the process 
pathToSave = path_folder
folderName = 'VIOLET';

pathNewFolder = fullfile(pathToSave, folderName);

if ~exist(pathNewFolder, 'dir')
    mkdir(pathNewFolder);
    disp(['Folder "', folderName, '" has been created.']);
else
    disp(['Folder "', folderName, '" already exists.']);
end

for i=0:99
    
    filename = sprintf('%s_%03d.txt', folderName, i);
    filename_rev = sprintf('%s_reverse_%03d.txt', folderName, i);
    fullfilename = fullfile(pathNewFolder, filename);
    fullfilename_rev = fullfile(pathNewFolder, filename_rev);

    % Generate noise time series
    x = violetnoise(m, n); 

    % Cut first idx0 part of the time series
    x_cut = x(idx0:end);

    % Transform in a coumn vector to save 
    x_noise = x_cut';
    x_reverse = flip(x_noise);

    writematrix(x_noise, fullfilename);
    writematrix(x_reverse, fullfilename_rev);
    
end