import numpy as np
from function import struct
from function import _readTxt,_cal_effect_size,_fixed_effects_meta_analysis



import numpy as np

def restore_effect_size_to_matrix(combined_effect_size, upper_threshold):
    """
    Restore the combined_effect_size array into a symmetric matrix where the upper triangle is defined by the upper_threshold.

    Parameters:
    combined_effect_size (np.array): 1D numpy array of size m.
    upper_threshold (np.array): 2D numpy array of shape n x n consisting of True/False values.

    Returns:
    np.array: Symmetric matrix with restored values from combined_effect_size.
    """
    n = upper_threshold.shape[0]
    restored_matrix = np.zeros((n, n))

    # Iterator for combined_effect_size
    effect_size_iter = iter(combined_effect_size)

    # Fill the upper triangle based on upper_threshold
    for i in range(n):
        for j in range(i, n):
            if upper_threshold[i, j]:
                restored_matrix[i, j] = next(effect_size_iter)

    # Make the matrix symmetric
    restored_matrix = restored_matrix + restored_matrix.T - np.diag(restored_matrix.diagonal())

    return restored_matrix

# Example usage

n = 5  # Example value for n, creating a 4x4 matrix


upper_threshold = np.triu(np.random.choice([True, False], size=(n, n)), 1)  # Example upper_threshold matrix
print(upper_threshold)

num_true_upper_triangle = np.sum(upper_threshold[np.triu_indices(n, 1)])

# Generating a combined_effect_size array with the same length as the number of True elements in the upper triangle
combined_effect_size = np.random.rand(num_true_upper_triangle)
print(combined_effect_size)
restored_matrix = restore_effect_size_to_matrix(combined_effect_size, upper_threshold)
print(restored_matrix)

exit()












file = ['aparc','lausanne250','BN_Atlas','HCP_MMP','Schaefer200']
for name in file:
    thresholdData = '/media/qingyuan/data/Statistics Convert Data/Parameter/threshold/HCP_'+name+'_threshold0.6.txt'
    thresholdMat = _readTxt(thresholdData)
    thresholdData_Cobre = '/media/qingyuan/data/Statistics Convert Data/Parameter/threshold/Cobre_'+name+'_threshold0.6.txt'
    thresholdMat_Cobre = _readTxt(thresholdData_Cobre)
    threshold = thresholdMat * thresholdMat_Cobre
    print(threshold.shape)
    np.savetxt(name+"_threshold0.6.txt",threshold,fmt='%d',delimiter=',')
