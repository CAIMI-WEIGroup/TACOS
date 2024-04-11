import numpy as np
import math
import os
from .function import _readTxt
from .function import _packmat
from .function import _unpackmat
from .function import _matShow
from .function import _load_mat_file
from .function import _readTxtfromme
def convertStatistics(*, sourceT_Path, controlS_Path=None, patientS_Path=None, source_Atlas=None, target_Atlas=None, form=None):
    """
    Transform source atlas t-statistics to target atlas t-statistics.

    Parameters:
    - source_T (required): Source t-statistics.
    - source_Atlas (required): Source atlas name, must be one of ['aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219','BN','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400'].
    - target_Atlas (required): Target atlas name, must be one of ['aal', 'DK114', 'Schaefer200', 'HCP_MMP'].
    - form (required): Specifies the transformation form, must be either 'functional' or 'structural'.
    - control_S (optional): Control group variance matrix, defaults to simulated variance matrix derived from the HCP dataset if not provided.
    - patient_S (optional): Patient group variance matrix, defaults to simulated variance matrix derived from the HCP dataset not provided.

    Returns:
    The transformed t-statistics matrix in target atlas and will be saved as '.csv' in current directory.
    """

    # Validate source_Atlas, target_Atlas, and form
    if source_Atlas not in ['aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219','BN','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400']:
        raise ValueError("source_Atlas must be either 'aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219','BN','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400'.")
    if target_Atlas not in ['aal', 'DK114', 'Schaefer200', 'HCP_MMP']:
        raise ValueError("target_Atlas must be either 'aal', 'DK114', 'Schaefer200', 'HCP_MMP'.")
    if form not in ['functional', 'structural']:
        raise ValueError("form must be either 'functional' or 'structural'.")

    thresholdPath = os.path.join('resources', 'threshold', f'{target_Atlas}' + '_threshold0.6.txt')
    brainCorresponding = os.path.join('resources', 'overlap', f'{target_Atlas}_to_{source_Atlas}.txt')
    brainGraph = _readTxt(brainCorresponding)
    target_Len = brainGraph.shape[0]
    source_Len = brainGraph.shape[1]
    threshold  = 1
    coefficient = []
    control_S = []
    patient_S = []
    if form == 'functional':
        threshold = np.zeros((target_Len,target_Len)) + 1
        if target_Atlas == 'Schaefer200':
            threshold = np.zeros((200, 200)) + 1
        coefficient = _load_mat_file(os.path.join('resources', 'coefficient', f'F_{target_Atlas}_from_{source_Atlas}.mat'))['F_'+target_Atlas+'_from_'+source_Atlas][0]

        # Set default values for control_S and patient_S if not provided
        if controlS_Path is None:
            controlS_Path = os.path.join('resources', 'default_variance', f'S_HCP_{source_Atlas}_FC.csv')
            control_S = _readTxt(controlS_Path)
        else:
            control_S = _readTxtfromme(controlS_Path)
        if patientS_Path is None:
            patientS_Path = os.path.join('resources', 'default_variance', f'S_HCP_{source_Atlas}_FC.csv')
            patient_S = _readTxt(patientS_Path)
        else:
            patient_S = _readTxtfromme(patientS_Path)
    if form == 'structural':
        threshold = _readTxt(thresholdPath)
        coefficient = _load_mat_file(os.path.join('resources', 'coefficient', f'S_{target_Atlas}_from_{source_Atlas}.mat'))['S_'+target_Atlas+'_from_'+source_Atlas][0]
        # Set default values for control_S and patient_S if not provided
        if controlS_Path is None:
            controlS_Path = os.path.join('resources', 'default_variance', f'S_HCP_{source_Atlas}_SC.csv')
            control_S = _readTxt(controlS_Path)
        else:
            control_S = _readTxtfromme(controlS_Path)
        if patientS_Path is None:
            patientS_Path = os.path.join('resources', 'default_variance', f'S_HCP_{source_Atlas}_SC.csv')
            patient_S = _readTxt(patientS_Path)
        else:
            patient_S = _readTxtfromme(patientS_Path)
    source_T = _readTxtfromme(sourceT_Path)

    source_T = np.nan_to_num(source_T)
    control_S = np.nan_to_num(control_S)
    patient_S = np.nan_to_num(patient_S)

    transformed_T = np.zeros((target_Len,target_Len))
    source_T, control_S, patient_S = _packmat(source_Atlas,source_T,control_S,patient_S)

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
    transformed_T = _unpackmat(target_Atlas,transformed_T)
    transformed_T = transformed_T * threshold

    np.savetxt('transformed_{}_{}.csv'.format(target_Atlas, source_Atlas), transformed_T, delimiter=',')
    _matShow('transformed_' + target_Atlas, transformed_T)
    _matShow('source_' + source_Atlas, source_T)

    return transformed_T



