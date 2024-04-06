import numpy as np
import math
from code.function import _readTxt
from code.function import _packmat
from code.function import _unpackmat


def convertStatistics(*, sourceT_Path, controlS_Path=None, patientS_Path=None, source_Atlas=None, target_Atlas=None, form=None):
    """
    Transform source atlas t-statistics to target atlas t-statistics.

    Parameters:
    - source_T: Source t-statistics.
    - control_S: Control group variance matrix, defaults to simulated variance matrix derived from the HCP dataset if not provided.
    - patient_S: Patient group variance matrix, defaults to simulated variance matrix derived from the HCP dataset not provided.
    - source_Atlas: Source atlas name, must be one of ['aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219','BN','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400'].
    - target_Atlas: Target atlas name, must be one of ['aal', 'DK114', 'Schaefer200', 'HCP_MMP'].
    - form: Specifies the transformation form, must be either 'functional' or 'structural'.

    Returns:
    Transformed t-statistics matrix in target atlas.
    """

    # Validate source_Atlas, target_Atlas, and form
    if source_Atlas not in ['aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219','BN','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400']:
        raise ValueError("source_Atlas must be either 'aal', 'DK114', 'Schaefer200', 'HCP_MMP', 'DK', 'DK219','BN','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400'.")
    if target_Atlas not in ['aal', 'DK114', 'Schaefer200', 'HCP_MMP']:
        raise ValueError("target_Atlas must be either 'aal', 'DK114', 'Schaefer200', 'HCP_MMP'.")
    if form not in ['functional', 'structural']:
        raise ValueError("form must be either 'functional' or 'structural'.")


    thresholdPath = '../resources/threshold/' + target_Atlas + '_threshold0.6.txt'
    brainCorresponding = '../resources/overlap/' +target_Atlas + '_to_' + source_Atlas + '.txt'
    brainGraph = _readTxt(brainCorresponding)
    target_Len = brainGraph.shape[0]
    source_Len = brainGraph.shape[1]

    if form == 'functional':
        threshold = np.zeros((target_Len,target_Len)) + 1
        coefficient = np.load('../resources/coefficient/F_' + target_Atlas + '_from_' + source_Atlas + '.npy',allow_pickle=True).item()

        # Set default values for control_S and patient_S if not provided
        if controlS_Path is None:
            controlS_Path = '../resources/default_variance/S_HCP_'+source_Atlas+'_FC.npy'  # Or any other default value
        if patientS_Path is None:
            patientS_Path = '../resources/default_variance/S_HCP_'+source_Atlas+'_FC.npy'  # Or any other default value

    if form == 'structural':
        threshold = _readTxt(thresholdPath)
        coefficient = np.load('../resources/coefficient/S_' + target_Atlas + '_from_' + source_Atlas + '.npy',allow_pickle=True).item()
        # Set default values for control_S and patient_S if not provided
        if controlS_Path is None:
            controlS_Path = '../resources/default_variance/S_HCP_' + source_Atlas + '_SC.npy'  # Or any other default value
        if patientS_Path is None:
            patientS_Path = '../resources/default_variance/S_HCP_' + source_Atlas + '_SC.npy'  # Or any other default value

    source_T = np.genfromtxt(sourceT_Path, delimiter='[,\s]+', dtype=float)
    control_S = np.genfromtxt(controlS_Path, delimiter='[,\s]+', dtype=float)
    patient_S = np.genfromtxt(patientS_Path, delimiter='[,\s]+', dtype=float)
    source_T = np.nan_to_num(source_T)
    control_S = np.nan_to_num(control_S)
    patient_S = np.nan_to_num(patient_S)

    transformed_T = np.zeros((target_Len,target_Len))
    source_T, control_S, patient_S = _packmat(source_Atlas,source_T,control_S,patient_S)

    for n in range(0, target_Len - 1):
        for m in range(n + 1, target_Len):
            composeA = np.squeeze(np.array(np.where(brainGraph[n] > 0.01)), axis=0)
            composeB = np.squeeze(np.array(np.where(brainGraph[m] > 0.01)), axis=0)
            k = np.zeros((source_Len, source_Len))
            denominator = 0
            for a in composeA:
                for b in composeB:
                    if a != b:
                        if (n, m, a, b) in coefficient.keys():
                            k[a][b] = coefficient[(n, m, a, b)]
                        else:
                            k[a][b] = coefficient[(n, m, b, a)]
                        if np.isnan(k[a][b]) or np.isinf(k[a][b]):
                            k[a][b] = 0
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
    transformed_T = transformed_T * threshold
    transformed_T = _unpackmat(target_Atlas,transformed_T)
    return transformed_T



