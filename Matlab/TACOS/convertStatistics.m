
 function transformed_T = convertStatistics(varargin)
    % Transform source atlas t-statistics to target atlas t-statistics.
    %
    % Parameters:
    % - sourceT_Path (required): Path to source t-statistics.
    % - controlS_Path (optional): Path to control group variance matrix.
    % - patientS_Path (optional): Path to patient group variance matrix.
    % - source_Atlas (required): Source atlas name.
    % - target_Atlas (required): Target atlas name.
    % - form (required): Specifies the transformation form, must be either 'functional' or 'structural'.
    %
    % Returns:
    % The transformed t-statistics matrix in target atlas and will be saved as '.csv' in current directory.
    p = inputParser;

    addParameter(p, 'sourceT_Path', '', @ischar);
    addParameter(p, 'controlS_Path', '', @ischar);
    addParameter(p, 'patientS_Path', '', @ischar);
    addParameter(p, 'source_Atlas', '', @ischar);
    addParameter(p, 'target_Atlas', '', @ischar);
    addParameter(p, 'form', '', @ischar);

    
    parse(p, varargin{:});

    required_params = {'sourceT_Path', 'source_Atlas', 'target_Atlas', 'form'};
    for i = 1:length(required_params)
        if isempty(p.Results.(required_params{i}))
            error(['Missing required parameter: ', required_params{i}]);
        end
    end

    sourceT_Path = p.Results.sourceT_Path;
    controlS_Path = p.Results.controlS_Path;
    patientS_Path = p.Results.patientS_Path;
    source_Atlas = p.Results.source_Atlas;
    target_Atlas = p.Results.target_Atlas;
    form = p.Results.form;


    if ~isempty(controlS_Path)
        disp(['Control Sample: ', controlS_Path]);
    end
    if ~isempty(patientS_Path)
        disp(['Patient Sample: ', patientS_Path]);
    end

    %% Validate inputs
    validSourceAtlases = {'aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219', 'BN', 'arslan', ...
                          'baldassano', 'Brodmann', 'economo', 'ica', 'nspn500', 'power', 'shen', ...
                          'Schaefer300', 'Schaefer400'};
    validTargetAtlases = {'aal', 'DK114', 'Schaefer200', 'HCP_MMP'};

    if ~ismember(source_Atlas, validSourceAtlases)
        error('Invalid source_Atlas');
    end
    if ~ismember(target_Atlas, validTargetAtlases)
        error('Invalid target_Atlas');
    end
    if ~ismember(form, {'functional', 'structural'})
        error('form must be either "functional" or "structural".');
    end

    %% Set up paths and defaults
    path_to_resources = '../../Python/TACOS/resources';
    thresholdPath = fullfile(path_to_resources, 'threshold', [target_Atlas, '_threshold0.6.txt']);
    brainCorresponding = fullfile(path_to_resources, 'overlap', [target_Atlas, '_to_', source_Atlas, '.txt']);
    brainGraph = readTxt(brainCorresponding);
    target_Len = size(brainGraph, 1);
    source_Len = size(brainGraph, 2);
    threshold = 1;
    coefficient = [];
    control_S = [];
    patient_S = [];

    %% Load data based on form
    if strcmp(form, 'functional')
        threshold = ones(target_Len, target_Len);
        if strcmp(target_Atlas, 'Schaefer200')
            threshold = ones(200, 200);
        end
        coefficient = importdata(fullfile(path_to_resources, 'coefficient', ['F_', target_Atlas, '_from_', source_Atlas, '.mat']), ['F_', target_Atlas, '_from_', source_Atlas]);
       
        % Set default values for control_S and patient_S if not provided
        controlS_Path = setDefault(controlS_Path, 'default_variance', ['S_HCP_', source_Atlas, '_FC.csv']);
        patientS_Path = setDefault(patientS_Path, 'default_variance', ['S_HCP_', source_Atlas, '_FC.csv']);
        control_S = readTxt(controlS_Path);
        patient_S = readTxt(patientS_Path);
    elseif strcmp(form, 'structural')
        threshold = readTxt(thresholdPath);
        coefficient = importdata(fullfile(path_to_resources, 'coefficient', ['S_', target_Atlas, '_from_', source_Atlas, '.mat']), ['S_', target_Atlas, '_from_', source_Atlas]);

        % Set default values for control_S and patient_S if not provided
        controlS_Path = setDefault(controlS_Path, 'default_variance', ['S_HCP_', source_Atlas, '_SC.csv']);
        patientS_Path = setDefault(patientS_Path, 'default_variance', ['S_HCP_', source_Atlas, '_SC.csv']);
        control_S = readTxt(controlS_Path);
        patient_S = readTxt(patientS_Path);
    end

    %% Read and process source t-statistics
    source_T = readTxt(sourceT_Path);  
    transformed_T = zeros(target_Len, target_Len);
    [source_T, control_S,patient_S] = packmat(source_Atlas, source_T, control_S, patient_S);
    %% Compute transformation
    cofnum = 1;
    for n = 1:target_Len-1
        for m = n+1:target_Len
            composeA = find(brainGraph(n, :) > 0.01);
            composeB = find(brainGraph(m, :) > 0.01);
            k = zeros(source_Len,source_Len);
            denominator = 0;
            for a = composeA
                for b = composeB
                    if a ~= b
                        k(a,b) = coefficient(cofnum);                     
                        cofnum = cofnum + 1;
                        denominator = denominator + k(a, b) ^ 2 * (control_S(a, b) ^ 2 + patient_S(a, b) ^ 2);
                    end
                end
            end
            result = 0;
            if denominator == 0
                transformed_T(n, m) = 0;
                transformed_T(m, n) = 0;
            else
                for a = composeA
                    for b = composeB
                        if a ~= b
                            result = result + source_T(a, b) * k(a, b) * sqrt((control_S(a, b) ^ 2 + patient_S(a, b) ^ 2) / denominator);
                        end
                    end
                end
                transformed_T(n, m) = result;
                transformed_T(m, n) = result;
            end
        end
    end

    %% Save and display results
    transformed_T = unpackmat(target_Atlas, transformed_T);

    transformed_T = transformed_T .* threshold;

    csvwrite(['transformed_', target_Atlas, '_', source_Atlas, '.csv'], transformed_T);
    matShow(['transformed_' target_Atlas], transformed_T);
    matShow(['source_' source_Atlas], source_T);
end

function outPath = setDefault(inPath, folder, defaultFile)
    if isempty(inPath)
        outPath = fullfile('../../Python/TACOS/resources', folder, defaultFile);
    else
        outPath = inPath;
    end
end

function [new_source_T, new_control_S, new_patient_S] = packmat(source_Atlas, source_T, control_S, patient_S)
    % Packs matrices by inserting zeros according to the atlas configuration.

    switch source_Atlas
        case 'DK'
            new_source_T = zeros(82, 82);
            new_source_T(15:end, 15:end) = source_T;
            new_control_S = zeros(82, 82);
            new_control_S(15:end, 15:end) = control_S;
            new_patient_S = zeros(82, 82);
            new_patient_S(15:end, 15:end) = patient_S;
        case 'Schaefer200'
            new_source_T = insert_zeros(source_T, 101);
            new_source_T = insert_zeros(new_source_T, 1);
            new_control_S = insert_zeros(control_S, 101);
            new_control_S = insert_zeros(new_control_S, 1);
            new_patient_S = insert_zeros(patient_S, 101);
            new_patient_S = insert_zeros(new_patient_S, 1);

        case 'Brodmann'
            new_source_T = insert_zeros(source_T, 40);
            new_source_T = insert_zeros(new_source_T, 1);
            new_control_S = insert_zeros(control_S, 40);
            new_control_S = insert_zeros(new_control_S, 1);
            new_patient_S = insert_zeros(patient_S, 40);
            new_patient_S = insert_zeros(new_patient_S, 1);
        case 'economo'
            new_source_T = insert_zeros(source_T, 1);
            new_control_S = insert_zeros(control_S, 1);
            new_patient_S = insert_zeros(patient_S, 1);
        case 'nspn500'
            new_source_T = insert_zeros(source_T, 153);
            new_source_T = insert_zeros(new_source_T, 1);
            new_control_S = insert_zeros(control_S, 153);
            new_control_S = insert_zeros(new_control_S, 1);
            new_patient_S = insert_zeros(patient_S, 153);
            new_patient_S = insert_zeros(new_patient_S, 1);
        otherwise
            new_source_T = source_T;
            new_control_S = control_S;
            new_patient_S = patient_S;
    end
end

function new_transformed_T = unpackmat(target_Atlas, transformed_T)
    % Unpacks matrices by trimming padded zeros according to the atlas configuration.

    switch target_Atlas
        case 'DK'
            new_transformed_T = transformed_T(15:end, 15:end);
        case 'Schaefer200'
            new_transformed_T = remove_row_col(transformed_T, 102);
            new_transformed_T = remove_row_col(new_transformed_T, 1);
        case 'Brodmann'
            new_transformed_T = remove_row_col(transformed_T, 41);
            new_transformed_T = remove_row_col(new_transformed_T, 1);
        case 'economo'
            new_transformed_T = remove_row_col(transformed_T, 1);
        case 'nspn500'
           new_transformed_T = remove_row_col(transformed_T, 154);
            new_transformed_T = remove_row_col(new_transformed_T, 1);
        otherwise
            new_transformed_T = transformed_T;
    end
end

function matShow(name, mat)
    colors = [40/256, 116/256, 166/256; 1, 1, 1; 231/256, 76/256, 60/256];
    cmap = customColormap(colors);
    widthInInches = 50 / 25.4;
    figure('Units', 'inches', 'Position', [1, 1, widthInInches, widthInInches]);
    ax = axes('Position', [0.1 0.1 0.8 0.8], 'Visible', 'off');
    imagesc(mat, 'Parent', ax, [-4 4]); 
    colormap(ax, cmap);
    colorbar('eastoutside', 'AxisLocation', 'out');
    caxis([-4 4]);
    saveas(gcf, [name, '.svg'], 'svg');
end

function cmap = customColormap(colors)
    cmapSize = 256; 
    cmap = interp1(linspace(0, 1, size(colors, 1)), colors, linspace(0, 1, cmapSize));
end

function dataMat = readTxt(path)
    dataMat = readmatrix(path);
    dataMat(isnan(dataMat)) = 0;
end

function updated_matrix = insert_zeros(matrix, index)
    [rows, cols] = size(matrix);

    if index == 1
        updated_matrix = [zeros(1, cols); matrix];
    elseif index > rows
        updated_matrix = [matrix; zeros(1, cols)];
    else
        updated_matrix = [matrix(1:index-1, :); zeros(1, cols); matrix(index:end, :)];
    end

    if index == 1
        updated_matrix = [zeros(rows + 1, 1), updated_matrix];
    elseif index > cols
        updated_matrix = [updated_matrix, zeros(rows + 1, 1)];
    else
        updated_matrix = [updated_matrix(:, 1:index-1), zeros(rows + 1, 1), updated_matrix(:, index:end)];
    end
end

function updated_matrix = remove_row_col(matrix, index)
    matrix(index, :) = [];  
    matrix(:, index) = [];  
    updated_matrix = matrix;
end