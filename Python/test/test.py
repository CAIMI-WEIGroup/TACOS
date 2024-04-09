# from code.convert import convertStatistics
#
# import numpy as np
# from scipy import io
#
# from code.function import pearsonrImage_threshold
# from code.function import _readTxt
import requests
import os
import subprocess




url = 'https://www.dropbox.com/scl/fi/68777a2jn85mh1t4ppy6h/test.txt?rlkey=qyytuqnw91bpenawz710d5vy7&dl=1'
target_folder = "../code/"
file_path = os.path.join(target_folder, "funtest.txt")

# 使用 wget 下载文件
try:
    result = subprocess.run(['wget', '-O', file_path, url], check=True)
    print(f"Downloaded resource successfully to '{file_path}'.")
except subprocess.CalledProcessError as e:
    print(f"Failed to download the resource: {e}")
exit()




# https://www.dropbox.com/t/GyqSxgUORFwM5Xaw
url = 'https://www.dropbox.com/scl/fi/68777a2jn85mh1t4ppy6h/test.txt?rlkey=qyytuqnw91bpenawz710d5vy7&dl=1'
# url = 'https://www.dropbox.com/home/TACOS/test.txt'
# url = 'https://www.dropbox.com/preview/TACOS/test.txt?context=content_suggestions&role=personal'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

print('waitresponse')
try:
    response = requests.get(url, headers=headers, timeout=20)
    print('Response obtained')
    print('responseget')
    target_folder = "../code/"
    if response.status_code == 200:
        # 构建目标文件的完整路径
        file_path = os.path.join(target_folder, "funtest.txt")

        # 写入文件
        with open(file_path, "wb") as file:
            print('start')
            file.write(response.content)
        print(f"Downloaded resource successfully to '{file_path}'.")
    else:
        print("Failed to download the resource. Please check the source and target names.")
except Exception as e:
    print(f"Error: {e}")


exit()







# new_matrix = np.zeros((202,202))+1
# new_matrix = np.delete(new_matrix, (0,100), axis=0)
# new_matrix = np.delete(new_matrix, (0,100), axis=1)
#
# print(new_matrix.shape)
# print(new_matrix)
# print(new_matrix[100,:])
# exit()



# # namelist = ['Cobre','CUI_GE']
# namelist = ['Cobre','CUI_GE','CUI_SIEMENS','UCLA_UNP','MCICShare']
# # atlaslist = ['aparc','lausanne250','HCP_MMP','BN_Atlas','Schaefer200','lausanne120']
# atlaslist = ['lausanne250']
# weightlist = ['1']
#
#
# #cobre patient:58,normal:73
# #CUI_GE:144,141
# #CUI_SIEMENS:57,87
# #UCLA_UNP:49,123
# #MCICShare:31,24
# thresholdPath = '../resources/threshold/' + 'DK114' + '_threshold0.6.txt'
# threshold = _readTxt(thresholdPath)
# print(threshold.shape)
# allpreds_list = []
# true_list = []
# for weight in weightlist:
#     for atlas in atlaslist:
#         # print(atlas)
#         preds_dict = {}
#         true_dict = {}
#         for name in namelist:
#             print(atlas,name)
#             mat_path = '/media/qingyuan/data/Statistics Convert Data/Dataset/' + name + '/math_predict_only/math_predict_only_TSmat_lausanne120_'+atlas+'_weight'+weight+'_'+name+'.mat'
#             mat_preds = io.loadmat(mat_path)['preds'][0]
#             mat_true = io.loadmat(mat_path)['true'][0]
#             print(mat_preds.shape)
#             print(mat_true.shape)
#             num_path = '/media/qingyuan/data/Statistics Convert Data/Dataset/' + name + '/'+name + '_TSmat_only/TSmat_lausanne120_'+atlas+'_weight'+weight+'_'+name+'.mat'
#             patient_nonzero = io.loadmat(num_path)['patient_nonzero']
#             normal_nonzero = io.loadmat(num_path)['normal_nonzero']
#             # np.savetxt(atlas+"patient_num.txt", patient_nonzero, fmt='%d', delimiter=',')
#             # np.savetxt(atlas+"control_num.txt", normal_nonzero, fmt='%d', delimiter=',')
#             print(patient_nonzero.shape)
#             preds_dict[name] = mat_preds
#             true_dict[name] = mat_true
#
#
# combined_true = meta_Simple(true_dict['Cobre'],true_dict['CUI_GE'],atlas='DK114',form='structural')
# combined_preds = meta_Simple(preds_dict['Cobre'],preds_dict['CUI_GE'],atlas='DK114',form='structural')
# pearsonrImage_threshold('conbined',combined_preds,combined_true,threshold)
# exit()









mat_path = '/media/qingyuan/data/Statistics Convert Data/Dataset/HCP/HCP_TSmat_FC/' + 'lausanne120' + '/true/TSmat_' + 'lausanne120' + '_' + 'BN_Atlas' + '_HCP_FC.mat'
print(mat_path)


subjectsLr = np.squeeze(io.loadmat(mat_path)['connectivity_lr'][:,:,:1])
print(subjectsLr.shape)
subjectsHr = np.squeeze(io.loadmat(mat_path)['connectivity_hr'][:,:,:1])
print(subjectsHr.shape)
normalS = np.squeeze(io.loadmat(mat_path)['normal'][:,:,:1])
patientS = np.squeeze(io.loadmat(mat_path)['patient'][:,:,:1])

thresholdPath = '../resources/threshold/' + 'DK114' + '_threshold0.6.txt'
threshold = _readTxt(thresholdPath)
# threshold = np.zeros((114,114))+1
# 'structural'
preds = convertStatistics(subjectsHr,normalS,patientS,'BN','DK114','structural')
# for i in preds:
#     print(i)
print('hi')
pearsonrImage_threshold('BN2121'+'_weight',preds,subjectsLr,threshold)