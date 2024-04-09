import numpy as np
from scipy.stats import t
import matplotlib.pyplot as plt
from scipy import stats



def _readTxt(path):
    file = open(path)
    dataMat = []
    for line in file.readlines():
        curLine = line.strip().split(",")
        floatLine = list(map(float, curLine))
        dataMat.append(floatLine[:])
    dataMat = np.array(dataMat)
    dataMat[np.isnan(dataMat)] = 0
    return dataMat

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

def pearsonrImage_threshold(name,preds,lr,thresholdmat):

    upper_mat = np.triu(thresholdmat, k=1).astype(bool)
    upper_preds = np.triu(preds)
    preds_list = upper_preds[upper_mat]
    upper_lr = np.triu(lr)
    lr_list = upper_lr[upper_mat]
    # print('preds',len(preds_list)*2)
    # print('lr',len(lr_list)*2)
    plt.xticks(np.arange(-3, 3, 0.3))
    plt.yticks(np.arange(-3, 3, 0.3))
    plt.xlim((-3, 3))
    plt.ylim((-3, 3))
    plt.scatter(lr_list, preds_list, s=0.3)

    plt.xlabel('lr')
    plt.ylabel('preds')
    r, p = stats.pearsonr(lr_list, preds_list)
    plt.title('r = %6.3f，p = %6.6f' % (r, p))
    plt.savefig(name)
    plt.close()
    return r




# class struct:
#     def __init__(self,t_array,confidence_interval,standard_error,cohen_d,patient_num,normal_num):
#         self.t_array = t_array
#         self.confidence_interval = confidence_interval
#         self.standard_error = standard_error
#         self.cohen_d = cohen_d
#         self.patient_num = patient_num
#         self.normal_num = normal_num
#
# def _cal_effect_size(mat, upper_threshold, patient_num_mat, normal_num_mat):
#
#     upper_mat = np.triu(mat)
#
#     t_array = np.array(upper_mat[upper_threshold])
#
#
#     n1 = np.array(np.triu(patient_num_mat)[upper_threshold])
#     n2 = np.array(np.triu(normal_num_mat)[upper_threshold])
#
#
#     if t_array.shape != n1.shape or t_array.shape != n2.shape:
#         raise ValueError("Transformed arrays must have the same shape.")
#
#     cohen_d = np.zeros_like(t_array)
#     standard_error = np.zeros_like(t_array)
#     ci_lower_values = np.zeros_like(t_array)
#     ci_upper_values = np.zeros_like(t_array)
#
#     for idx in range(t_array.shape[0]):
#         n1_ij = n1[idx]
#         n2_ij = n2[idx]
#         n_ij = n1_ij + n2_ij
#
#         cohen_d[idx] = t_array[idx] * np.sqrt(1 / n1_ij + 1 / n2_ij)
#         # print(t_array[idx],np.sqrt(1 / n1_ij + 1 / n2_ij),cohen_d[idx])
#         standard_error[idx] = np.sqrt((n1_ij + n2_ij) / (n1_ij * n2_ij) + cohen_d[idx] ** 2 / (2 * n_ij))
#
#         alpha = 0.05
#         df = n1_ij + n2_ij - 2
#         ci_lower_values[idx] = cohen_d[idx] - t.ppf(1 - alpha / 2, df) * standard_error[idx]
#         ci_upper_values[idx] = cohen_d[idx] + t.ppf(1 - alpha / 2, df) * standard_error[idx]
#
#     confidence_interval = np.column_stack((ci_lower_values, ci_upper_values))
#
#
#     return t_array, confidence_interval, standard_error, cohen_d
#
# def _calculate_Q_for_position(sites, position):
#
#     d_values = np.array([site.cohen_d[position] for site in sites.values()])
#     se_values = np.array([site.standard_error[position] for site in sites.values()])
#
#     weights = 1 / (se_values ** 2)
#
#     d_bar = np.sum(weights * d_values) / np.sum(weights)
#
#     Q = np.sum(weights * (d_values - d_bar) ** 2)
#
#     return Q
#
#
# def _calculate_all_Q(sites):
#
#     array_length = len(next(iter(sites.values())).t_array)
#
#     Q_values = [_calculate_Q_for_position(sites, i) for i in range(array_length)]
#
#     return Q_values
# def _fixed_effects_meta_analysis(data_dict):
#
#     weights = np.array([1 / np.array(study.standard_error) ** 2 for study in data_dict.values()])
#
#     combined_effect_size = np.sum(np.array([weights[i] * np.array(study.cohen_d)
#                                            for i, study in enumerate(data_dict.values())]), axis=0) / np.sum(weights, axis=0)
#
#     se_combined = (1 / np.sum(weights, axis=0)) ** 0.5
#
#     z_value = 1.96  # 95% CI
#     lower_limit = combined_effect_size - z_value * se_combined
#     upper_limit = combined_effect_size + z_value * se_combined
#
#     # return combined_effect_size, se_combined, (lower_limit, upper_limit)
#     return combined_effect_size
#
# def _restore_effect_size_to_matrix(combined_effect_size, upper_threshold):
#
#     n = upper_threshold.shape[0]
#     restored_matrix = np.zeros((n, n))
#
#     # Iterator for combined_effect_size
#     effect_size_iter = iter(combined_effect_size)
#
#     # Fill the upper triangle based on upper_threshold
#     for i in range(n):
#         for j in range(i, n):
#             if upper_threshold[i, j]:
#                 restored_matrix[i, j] = next(effect_size_iter)
#
#     # Make the matrix symmetric
#     restored_matrix = restored_matrix + restored_matrix.T - np.diag(restored_matrix.diagonal())
#
#     return restored_matrix

