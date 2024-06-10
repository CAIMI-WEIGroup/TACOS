
 function transformed_tval = convertStatistics(varargin)
    % Transform source atlas t-statistics to target atlas t-statistics.
    %
    % Parameters:
    % - source_tval (required): Path to source t-statistics.
    % - source_atlas (required): Source atlas name.
    % - target_atlas (required): Target atlas name.
    % - type (required): Specifies the transformation type, must be either 'functional' or 'structural'.
    % - variance_group1 (optional): Path to control group variance matrix.
    % - variance_group2 (optional): Path to patient group variance matrix.
    % - save_transformed_tval (optional): Whether to store the transformed tval as csv, acceptable value is true or false, defaults to false if not provided.
    % - display_transformed_tval (optional): Whether to display the transformed tval as svg, acceptable value is true or false, defaults to false if not provided.
    %
    % Returns:
    % The transformed t-statistics matrix in target atlas and will be saved as '.csv' in current directory.
    p = inputParser;

    addParameter(p, 'source_tval', '', @ischar);
    addParameter(p, 'variance_group1', '', @ischar);
    addParameter(p, 'variance_group2', '', @ischar);
    addParameter(p, 'source_atlas', '', @ischar);
    addParameter(p, 'target_atlas', '', @ischar);
    addParameter(p, 'type', '', @ischar);
    addParameter(p, 'save_transformed_tval', false, @(x) islogical(x) || isempty(x));
    addParameter(p, 'display_transformed_tval', false, @(x) islogical(x) || isempty(x));

    parse(p, varargin{:});

    required_params = {'source_tval', 'source_atlas', 'target_atlas', 'type'};
    for i = 1:length(required_params)
        if isempty(p.Results.(required_params{i}))
            error(['Missing required parameter: ', required_params{i}]);
        end
    end

    source_tval = p.Results.source_tval;
    variance_group1 = p.Results.variance_group1;
    variance_group2 = p.Results.variance_group2;
    source_atlas = p.Results.source_atlas;
    target_atlas = p.Results.target_atlas;
    type = p.Results.type;
    save_transformed_tval = p.Results.save_transformed_tval;
    display_transformed_tval = p.Results.display_transformed_tval;

    %% Validate inputs
    validSourceAtlases = {'aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219', 'BN', 'arslan', ...
                          'baldassano', 'Brodmann', 'economo', 'ica', 'nspn500', 'power', 'shen', ...
                          'Schaefer300', 'Schaefer400'};
    validTargetAtlases = {'aal', 'DK114', 'Schaefer200', 'HCP_MMP'};

    if ~ismember(source_atlas, validSourceAtlases)
        error('Invalid source_atlas');
    end
    if ~ismember(target_atlas, validTargetAtlases)
        error('Invalid target_atlas');
    end
    if ~ismember(type, {'functional', 'structural'})
        error('type must be either "functional" or "structural".');
    end
    if ~isempty(save_transformed_tval) && ~islogical(save_transformed_tval)
        error('save_transformed_tval must be either true, false, or not provided.');
    end
    if ~isempty(display_transformed_tval) && ~islogical(display_transformed_tval)
        error('display_transformed_tval must be either true, false, or not provided.');
    end

    %% Set up paths and defaults
    %path_to_resources = '../../Python/TACOS/resources';
    thresholdPath = fullfile([target_atlas, '_threshold0.6.txt']);
    brainCorresponding = fullfile([target_atlas, '_to_', source_atlas, '.txt']);
    brainGraph = readTxt(brainCorresponding);
    target_Len = size(brainGraph, 1);
    source_Len = size(brainGraph, 2);
    threshold = 1;
    coefficient = [];
    control_S = [];
    patient_S = [];

    %% Load data based on type
    if strcmp(type, 'functional')
        threshold = ones(target_Len, target_Len);
        if strcmp(target_atlas, 'Schaefer200')
            threshold = ones(200, 200);
        end
        coefficient = importdata(fullfile( ['F_', target_atlas, '_from_', source_atlas, '.mat']), ['F_', target_atlas, '_from_', source_atlas]);
       
        % Set default values for control_S and patient_S if not provided
        variance_group1 = setDefault(variance_group1, ['S_HCP_', source_atlas, '_FC.csv']);
        variance_group2 = setDefault(variance_group2, ['S_HCP_', source_atlas, '_FC.csv']);
        control_S = readTxt(variance_group1);
        patient_S = readTxt(variance_group2);
    elseif strcmp(type, 'structural')
        threshold = readTxt(thresholdPath);
        coefficient = importdata(fullfile( ['S_', target_atlas, '_from_', source_atlas, '.mat']), ['S_', target_atlas, '_from_', source_atlas]);

        % Set default values for control_S and patient_S if not provided
        variance_group1 = setDefault(variance_group1, ['S_HCP_', source_atlas, '_SC.csv']);
        variance_group2 = setDefault(variance_group2, ['S_HCP_', source_atlas, '_SC.csv']);
        control_S = readTxt(variance_group1);
        patient_S = readTxt(variance_group2);
    end

    %% Read and process source t-statistics
    source_T = readTxt(source_tval);  
    transformed_tval = zeros(target_Len, target_Len);
    [source_T, control_S,patient_S] = packmat(source_atlas, source_T, control_S, patient_S);
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
                transformed_tval(n, m) = 0;
                transformed_tval(m, n) = 0;
            else
                for a = composeA
                    for b = composeB
                        if a ~= b
                            result = result + source_T(a, b) * k(a, b) * sqrt((control_S(a, b) ^ 2 + patient_S(a, b) ^ 2) / denominator);
                        end
                    end
                end
                transformed_tval(n, m) = result;
                transformed_tval(m, n) = result;
            end
        end
    end

    %% Save and display results
    transformed_tval = unpackmat(target_atlas, transformed_tval);

    transformed_tval = transformed_tval .* threshold;

    if save_transformed_tval
        filename = sprintf('transformed_%s_%s.csv', target_atlas, source_atlas);
        csvwrite(['transformed_', target_atlas, '_', source_atlas, '.csv'], transformed_tval);
        fprintf('The transformed t-statistics have been saved as %s in the current directory.\n', filename);
    end

    if display_transformed_tval
        matShow(['transformed_' target_atlas], transformed_tval);
        matShow(['source_' source_atlas], source_T);
        fprintf('The transformed t-statistics have been saved as transformed_%s.svg and source_%s.svg in the current directory.\n', target_atlas, source_atlas);
    end

    fprintf('The t-statistics from %s have been transformed into %s successfully.\n', source_atlas, target_atlas);
end

function outPath = setDefault(inPath,defaultFile)
    if isempty(inPath)
        outPath = fullfile(defaultFile);
    else
        outPath = inPath;
    end
end

function [new_source_T, new_control_S, new_patient_S] = packmat(source_atlas, source_T, control_S, patient_S)
    % Packs matrices by inserting zeros according to the atlas configuration.

    switch source_atlas
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

function new_transformed_T = unpackmat(target_atlas, transformed_T)
    % Unpacks matrices by trimming padded zeros according to the atlas configuration.

    switch target_atlas
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
    figure('Units', 'inches', 'Position', [1, 1, widthInInches, widthInInches], 'Name', name);
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