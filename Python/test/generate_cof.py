# from testConvert import convertStatistics

import numpy as np
from scipy import io

# from code.function import pearsonrImage_threshold
from code.function import _readTxt
import requests
import os
import subprocess


target = 'Schaefer200'
sourceAtlas = ['aal','DK219','BN','DK','DK114','HCP_MMP','Schaefer200','arslan','baldassano','Brodmann','economo','ica','nspn500','power','shen','Schaefer300','Schaefer400']
# sourceAtlas = ['aal','lausanne250','BN_Atlas','aparc']
for source in sourceAtlas:
    if target==source:
        continue
    res = []
    single_S = np.load('../resources/default_variance/S_HCP_'+source+'_SC.npy')
    np.savetxt('../resources/default_variance/S_HCP_'+source+'_SC.csv', single_S, delimiter=',')

    continue
    coefficient = np.load('../resources/coefficient/F_' + target + '_from_' + source + '.npy',allow_pickle=True).item()
    brainCorresponding = '../resources/overlap/' + target + '_to_' + source + '.txt'
    brainGraph = _readTxt(brainCorresponding)
    target_Len = brainGraph.shape[0]
    source_Len = brainGraph.shape[1]
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
                        res.append(k[a][b])
    data = {'F_' + target + '_from_' + source: res}
    io.savemat('../resources/co/F_' + target + '_from_' + source+'.mat', data)