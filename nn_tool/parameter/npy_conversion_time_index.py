import glob
import os.path as opath
import scipy.io as spio
import numpy as np


f_path = '/home/bhc/OneDrive/Work/PhD/zwicker_tone/data/code_matlab/'
f_path_n = '/home/bhc/codes/spikes_classics/'
t_index_3_0 = 'time_index_multi_tones_500ms_180sec.mat'
t_index_3_1 = 'time_index_multi_tones_500ms_180sec_nn_3_1.mat'

'''time index for notched noise 3 s 0 s STRF'''
data_r = spio.loadmat(f_path + t_index_3_0)['time_index']
data_n = []

for i in range(49):
    a = np.concatenate(data_r[0][i])
    data_n.append(a)

o_file = t_index_3_0.replace('mat', 'npy')
print(f_path_n + o_file)
np.save(f_path_n + o_file, data_n)

'''time index for notched noise 3 s 1 s STRF'''

dataa_r = spio.loadmat(f_path + t_index_3_1)['time_index_nn_3_1']
dataa_n = [[] for i in range(2)]

for k in range(2):
    for i in range(49):
        a = np.concatenate(dataa_r[k][i])
        dataa_n[k].append(a)


p_file = t_index_3_1.replace('mat', 'npy')
print(f_path_n + p_file)
np.save(f_path_n + p_file, dataa_n)
