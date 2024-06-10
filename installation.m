function installation()
scriptDir = fileparts(mfilename("fullpath"));
addpath(fullfile(scriptDir,'Matlab','TACOS'));
addpath(fullfile(scriptDir,'Python','TACOS','resources','coefficient'));
addpath(fullfile(scriptDir,'Python','TACOS','resources','default_variance'));
addpath(fullfile(scriptDir,'Python','TACOS','resources','overlap'));
addpath(fullfile(scriptDir,'Python','TACOS','resources','region_order'));
addpath(fullfile(scriptDir,'Python','TACOS','resources','threshold'));
savepath;
disp('Toolbox installation is complete');
end

