% Iterate over all files of interest
clear; close all;

studyinfolder = '__DATAIN__\data\EEG_MPILMBB_LEMON\preproc';
studydatasetname = 'lemonINDI_BIDS';
outfolder= fullfile('__DATAOUT__\brainnet', studydatasetname, 'eeg');
mkdir(outfolder);

% Get a list of all files and folders in this folder.
files = dir(studyinfolder);

% Get a logical vector that tells which is a directory.
dirFlags = [files.isdir];
% Extract only those that are directories.
subFolders = files(dirFlags); % A structure with extra info.

% Get only the folder names into a cell array.
subFolderNames = {subFolders(3:end).name}; % Start at 3 to skip . and ..

for k = 1 : length(subFolderNames)

    % process eyeclosed
    ecfile = fullfile(studyinfolder,subFolderNames{k},[subFolderNames{k} '_EC.set']);
    % fprintf('EC File #%d = %s\n', k, ecfile);
    if exist(ecfile, 'file')
        fprintf('EC File #%d = %s\n', k, ecfile);
        EEG = pop_loadset('filename',[subFolderNames{k} '_EC.set'],'filepath',fullfile(studyinfolder,subFolderNames{k}));
        % Export for non-matlab processing
        outsubfolder = fullfile(outfolder,[subFolderNames{k}]);
        mkdir(outsubfolder);

        pop_export(EEG,fullfile(outsubfolder,'EC.csv'), 'transpose','on','separator',',','precision',4);
        
        powerst = powers(EEG.nbchan,EEG.data, EEG.srate);
        writetable(powerst,fullfile(outsubfolder,'EC_powers.csv'));
        writestruct(EEG.chanlocs,fullfile(outsubfolder,'EC_channels.json'),FileType="json");
        
        % return
    end
    % process eyeopen
    eofile = fullfile(studyinfolder,subFolderNames{k},[subFolderNames{k} '_EO.set']);
    if exist(eofile, 'file')
        fprintf('EO File #%d = %s\n', k, eofile);
        EEG = pop_loadset('filename',[subFolderNames{k} '_EO.set'],'filepath',fullfile(studyinfolder,subFolderNames{k}));
        % Export for non-matlab processing
        outsubfolder = fullfile(outfolder,[subFolderNames{k}]);
        mkdir(outsubfolder);

        pop_export(EEG,fullfile(outsubfolder,'EO.csv'), 'transpose','on','separator',',','precision',4);
        powerst = powers(EEG.nbchan,EEG.data, EEG.srate);
        writetable(powerst,fullfile(outsubfolder,'EO_powers.csv'));
        writestruct(EEG.chanlocs,fullfile(outsubfolder,'EO_channels.json'),FileType="json");
        close all;
 %       return;
    end
end