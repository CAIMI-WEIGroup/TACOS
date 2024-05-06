import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pkg_resources
import scipy.io as io
import os
def _readTxt(path):

    absolute_path = pkg_resources.resource_filename('TACOS', path)

    dataMat = []
    with open(absolute_path, 'r') as file:
        for line in file.readlines():
            curLine = line.strip().split(",")
            floatLine = list(map(float, curLine))
            dataMat.append(floatLine)

    dataMat = np.array(dataMat)
    dataMat[np.isnan(dataMat)] = 0
    return dataMat

def _readTxtfromme(path):
    path = os.path.expanduser(path)
    dataMat = []
    with open(path, 'r') as file:
        for line in file.readlines():
            curLine = line.strip().split(",")
            floatLine = list(map(float, curLine))
            dataMat.append(floatLine)

    dataMat = np.array(dataMat)
    dataMat[np.isnan(dataMat)] = 0
    return dataMat


def _load_mat_file(relative_path):
    absolute_path = pkg_resources.resource_filename('TACOS', relative_path)
    coefficient = io.loadmat(absolute_path)
    return coefficient


def _packmat(source_Atlas,source_T,control_S,patient_S):
    if source_Atlas == 'DK':
        new_source_T = np.zeros((82, 82))
        new_source_T[14:, 14:] = source_T
        new_control_S = np.zeros((82, 82))
        new_control_S[14:, 14:] = control_S
        new_patient_S = np.zeros((82, 82))
        new_patient_S[14:, 14:] = patient_S
    elif source_Atlas == 'Schaefer200':
        new_source_T = np.insert(source_T, (0, 100), 0, axis=0)
        new_source_T = np.insert(new_source_T, (0, 100), 0, axis=1)
        new_control_S = np.insert(control_S, (0, 100), 0, axis=0)
        new_control_S = np.insert(new_control_S, (0, 100), 0, axis=1)
        new_patient_S = np.insert(patient_S, (0, 100), 0, axis=0)
        new_patient_S = np.insert(new_patient_S, (0, 100), 0, axis=1)
    elif source_Atlas == 'Brodmann':
        new_source_T = np.insert(source_T, (0, 39), 0, axis=0)
        new_source_T = np.insert(new_source_T, (0, 39), 0, axis=1)
        new_control_S = np.insert(control_S, (0, 39), 0, axis=0)
        new_control_S = np.insert(new_control_S, (0, 39), 0, axis=1)
        new_patient_S = np.insert(patient_S, (0, 39), 0, axis=0)
        new_patient_S = np.insert(new_patient_S, (0, 39), 0, axis=1)
    elif source_Atlas == 'economo':
        new_source_T = np.insert(source_T, 0, 0, axis=0)
        new_source_T = np.insert(new_source_T, 0, 0, axis=1)
        new_control_S = np.insert(control_S, 0, 0, axis=0)
        new_control_S = np.insert(new_control_S, 0, 0, axis=1)
        new_patient_S = np.insert(patient_S, 0, 0, axis=0)
        new_patient_S = np.insert(new_patient_S, 0, 0, axis=1)
    elif source_Atlas == 'nspn500':
        new_source_T = np.insert(source_T, (0, 152), 0, axis=0)
        new_source_T = np.insert(new_source_T, (0, 152), 0, axis=1)
        new_control_S = np.insert(control_S, (0, 152), 0, axis=0)
        new_control_S = np.insert(new_control_S, (0, 152), 0, axis=1)
        new_patient_S = np.insert(patient_S, (0, 152), 0, axis=0)
        new_patient_S = np.insert(new_patient_S, (0, 152), 0, axis=1)
    else:
        new_source_T = source_T
        new_control_S = control_S
        new_patient_S = patient_S
    return new_source_T,new_control_S,new_patient_S


def _unpackmat(target_Atlas,transformed_T):
    if target_Atlas == 'DK':
        new_transformed_T = transformed_T[14:,14:]
    elif target_Atlas == 'Schaefer200':
        new_transformed_T = np.delete(transformed_T, (0, 101), axis=0)
        new_transformed_T = np.delete(new_transformed_T, (0, 101), axis=1)
    elif target_Atlas == 'Brodmann':
        new_transformed_T = np.delete(transformed_T, (0, 40), axis=0)
        new_transformed_T = np.delete(new_transformed_T, (0, 40), axis=1)
    elif target_Atlas == 'economo':
        new_transformed_T = np.delete(transformed_T, 0, axis=0)
        new_transformed_T = np.delete(new_transformed_T, 0, axis=1)
    elif target_Atlas == 'nspn500':
        new_transformed_T = np.delete(transformed_T, (0, 153), axis=0)
        new_transformed_T = np.delete(new_transformed_T, (0, 153), axis=1)
    else:
        new_transformed_T = transformed_T
    return new_transformed_T

def _matShow(name,mat):
    colors = [(40/256, 116/256, 166/256), (1, 1, 1), (231/256, 76/256, 60/256)]
    max_abs_value = np.max(np.abs(mat))
    # norm = mcolors.TwoSlopeNorm(vmin=-max_abs_value, vcenter=0, vmax=max_abs_value)
    norm = mcolors.TwoSlopeNorm(vmin=-4, vcenter=0, vmax=4)

    cmap_name = 'custom_diverging'
    cm = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors)

    width_in_inches = 50 / 25.4
    plt.figure(figsize=(width_in_inches, width_in_inches * 5 / 5))
    plt.rcParams['font.size'] = 6
    im = plt.imshow(mat, cmap=cm, norm= norm)
    plt.xticks([])
    plt.yticks([])

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    cbar = plt.colorbar(im, orientation='vertical')
    cbar.set_label('Value', rotation=270, labelpad=20)

    plt.savefig(name+'.svg',format='svg')
    plt.colorbar()
    plt.close()



