import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from tools import nnm_plot as nnp
from tools import nn_tool as nt
from parameter import parameters as pm
# import pylustrator
import matplotlib.pyplot as plt
# pylustrator.start()
sys.path.pop(1)

# file_spk = 'D:/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr79_200211_tsp.hdf5'
file_spk = snakemake.input
# file_lfp = 'D:/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr79_200211_lfp_fil.hdf5'

# condition setups
cond = [['nn_3_1', 'nn_wn_3_1'], ['nn_1_1', 'nn_wn_1_1']]  # conditions for offset response experiment
ind = [pm.Nn.nn_i['nn31'], pm.Nn.nn_i['nn11']]  # indices for each condition sessions
offset = [3000, 1000]  # offset start points for 3 / 1 and 1 / 1
trf = [150, 50]  # time points to calculate reference session range
lvs = ['70', '60']  # spl db you are going to use
group = {}


for file_input in file_spk:
    s_ref = [[] for _ in range(len(cond))]
    animal = nnp.animal_name(file_input)
    with h5py.File(file_input, 'r') as dat:
        for lv in range(len(lvs)):
            for j in range(len(cond)):  # choosing between 3 / 1 and 1 / 1
                if animal == 'cr103' and 'nn_1_1' in cond[j]:
                    s_ref[j] = np.zeros([2, 16, 2])
                else:
                    ti = ind[j][0]
                    tf = ind[j][1]
                    t_off = offset[j]
                    ths = [[] for _ in range(len(cond[j]))]
                    for k in range(len(cond[j])):  # choosing between notch and white noise
                        data = dat[cond[j][k]][lv]
                        mua = nt.index_spike(data)
                        ths[k].extend(nt.threshold_collect(mua, ti, tf, t_off))
                    bases = np.concatenate(ths, axis=1)
                    base = np.array([np.mean(bases, axis=1), np.std(bases, axis=1)])
                    s_ref[j].append(base.T)

        group[animal] = s_ref
# with h5py.File(file_lfp, 'r') as dat:
#     for j in range(len(cond)):  # choosing between 3 / 1 and 1 / 1
#         ti = ind[j][0]
#         tf = ind[j][1]
#         t_off = offset[j]
#         print('why')
#         for ch in range(16):  # channels
#             ths = []
#             print('you')
#             for k in range(len(cond[j])):  # choosing between notch and white noise
#                 print('do')
#                 for i in range(len(ti)):  # collecting offset-kinda reference session
#                     print('this', i)
#                     data = dat[cond[j][k]][0][ch]
#                     t_i = nt.lfp_index(ti[i] + t_off + trf[0])\
#
#                     t_f = nt.lfp_index(tf[i] - trf[1])
#                     ths.extend(data[t_i:t_f])

            # l_ref[j].append(ths)

with h5py.File(snakemake.output[0], 'w') as h:
    for t in list(group.keys()):
        d1 = h.create_dataset(t, data=group[t])
