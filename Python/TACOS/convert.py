import numpy as np
import math
import os
from .function import _readTxt
from .function import _packmat
from .function import _unpackmat
from .function import _matShow
from .function import _load_mat_file
from .function import _readTxtfromme
def convertStatistics(*, source_tval, variance_group1=None, variance_group2=None, source_atlas=None, target_atlas=None, type=None, save_transformed_tval=None, display_transformed_tval=None):
    """
    Transform source atlas t-statistics to target atlas t-statistics.

    Parameters:
    - source_tval (required): Source t-statistics.
    - source_atlas (required): Source atlas name, must be one of ['aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219','BN','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400'].
    - target_atlas (required): Target atlas name, must be one of ['aal', 'DK114', 'Schaefer200', 'HCP_MMP'].
    - type (required): Specifies the transformation type, must be either 'functional' or 'structural'.
    - variance_group1 (optional): Variance_group1 variance matrix, defaults to simulated variance matrix derived from the HCP dataset if not provided.
    - variance_group2 (optional): Variance_group2 variance matrix, defaults to simulated variance matrix derived from the HCP dataset not provided.
    - save_transformed_tval (optional): Whether to store the transformed tval as csv, acceptable value is True or False, defaults to False if not provided.
    - display_transformed_tval (optional): Whether to display the transformed tval as svg, acceptable value is True or False, defaults to False if not provided.

    Returns:
    The transformed t-statistics matrix in target atlas and will be saved as '.csv' in current directory.
    """

    if source_atlas not in ['aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219', 'BN', 'arslan', 'baldassano', 'Brodmann', 'economo', 'ica', 'nspn500', 'power', 'shen', 'Schaefer300', 'Schaefer400']:
        raise ValueError("source_atlas must be either 'aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219','BN','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400'.")
    if target_atlas not in ['aal', 'DK114', 'Schaefer200', 'HCP_MMP']:
        raise ValueError("target_atlas must be either 'aal', 'DK114', 'Schaefer200', 'HCP_MMP'.")
    if type not in ['functional', 'structural']:
        raise ValueError("type must be either 'functional' or 'structural'.")
    if save_transformed_tval not in [True, False, None]:
        raise ValueError("save_transformed_tval must be either True, False, or not provided.")
    if display_transformed_tval not in [True, False, None]:
        raise ValueError("display_transformed_tval must be either True, False, or not provided.")

    thresholdPath = os.path.join('resources', 'threshold', f'{target_atlas}' + '_threshold0.6.txt')
    brainCorresponding = os.path.join('resources', 'overlap', f'{target_atlas}_to_{source_atlas}.txt')
    brainGraph = _readTxt(brainCorresponding)
    target_Len = brainGraph.shape[0]
    source_Len = brainGraph.shape[1]
    threshold  = 1
    coefficient = []
    control_S = []
    patient_S = []
    if type == 'functional':
        threshold = np.zeros((target_Len,target_Len)) + 1
        if target_atlas == 'Schaefer200':
            threshold = np.zeros((200, 200)) + 1
        coefficient = _load_mat_file(os.path.join('resources', 'coefficient', f'F_{target_atlas}_from_{source_atlas}.mat'))['F_' + target_atlas + '_from_' + source_atlas][0]

        if variance_group1 is None:
            variance_group1 = os.path.join('resources', 'default_variance', f'S_HCP_{source_atlas}_FC.csv')
            control_S = _readTxt(variance_group1)
        else:
            control_S = _readTxtfromme(variance_group1)
        if variance_group2 is None:
            variance_group2 = os.path.join('resources', 'default_variance', f'S_HCP_{source_atlas}_FC.csv')
            patient_S = _readTxt(variance_group2)
        else:
            patient_S = _readTxtfromme(variance_group2)
    if type == 'structural':
        threshold = _readTxt(thresholdPath)
        coefficient = _load_mat_file(os.path.join('resources', 'coefficient', f'S_{target_atlas}_from_{source_atlas}.mat'))['S_' + target_atlas + '_from_' + source_atlas][0]

        if variance_group1 is None:
            variance_group1 = os.path.join('resources', 'default_variance', f'S_HCP_{source_atlas}_SC.csv')
            control_S = _readTxt(variance_group1)
        else:
            control_S = _readTxtfromme(variance_group1)
        if variance_group2 is None:
            variance_group2 = os.path.join('resources', 'default_variance', f'S_HCP_{source_atlas}_SC.csv')
            patient_S = _readTxt(variance_group2)
        else:
            patient_S = _readTxtfromme(variance_group2)
    source_T = _readTxtfromme(source_tval)

    source_T = np.nan_to_num(source_T)
    control_S = np.nan_to_num(control_S)
    patient_S = np.nan_to_num(patient_S)

    transformed_T = np.zeros((target_Len,target_Len))
    source_T, control_S, patient_S = _packmat(source_atlas, source_T, control_S, patient_S)

    cofnum = 0
    for n in range(0, target_Len - 1):
        for m in range(n + 1, target_Len):
            composeA = np.squeeze(np.array(np.where(brainGraph[n] > 0.01)), axis=0)
            composeB = np.squeeze(np.array(np.where(brainGraph[m] > 0.01)), axis=0)
            k = np.zeros((source_Len, source_Len))
            denominator = 0
            for a in composeA:
                for b in composeB:
                    if a != b:
                        k[a][b] = coefficient[cofnum]
                        cofnum = cofnum + 1
                        denominator = denominator + k[a][b] ** 2 * (control_S[a][b] ** 2 + patient_S[a][b] ** 2)
            result = 0
            if denominator == 0:
                transformed_T[n][m] = 0
                transformed_T[m][n] = 0
                continue
            else:
                for a in composeA:
                    for b in composeB:
                        if a != b:
                            result = result + source_T[a][b] * k[a][b] * math.sqrt((control_S[a][b] ** 2 + patient_S[a][b] ** 2) / denominator)
                transformed_T[n][m] = result
                transformed_T[m][n] = transformed_T[n][m]
    transformed_T = _unpackmat(target_atlas, transformed_T)
    transformed_T = transformed_T * threshold

    if save_transformed_tval:
        np.savetxt('transformed_{}_{}.csv'.format(target_atlas, source_atlas), transformed_T, delimiter=',')
        print("The transformed t-statistics have been saved as " + 'transformed_{}_{}.csv'.format(target_atlas, source_atlas) + " in the current directory.")

    if display_transformed_tval:
        _matShow('transformed_' + target_atlas, transformed_T)
        _matShow('source_' + source_atlas, source_T)
        print("The transformed t-statistics have been saved as " + 'transformed_{}.svg'.format(target_atlas) + " and " + 'source_{}.svg'.format(source_atlas) + " in the current directory.")

    print("The t-statistics from {}".format(source_atlas) + " have been transformed into {}".format(target_atlas) + "successfully.")
    return transformed_T
