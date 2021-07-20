import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from tools import nnm_plot as nnp
from tools import nn_tool as nt
from parameter import parameters as pm
import scipy.io
# import pylustrator
import matplotlib.pyplot as plt
# pylustrator.start()
sys.path.pop(1)

# file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr31_190312_tsp.hdf5',
#             '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr50_190724_tsp.hdf5']
# file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr31_190312_lfp_fil.hdf5',
#             '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr50_190724_lfp_fil.hdf5']
# file_spk = [
#             '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr50_190724_tsp.hdf5']
# file_lfp = [
#             '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr50_190724_lfp_fil.hdf5']

file_path_s = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/'
file_path_l = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/'

file_spk = sorted([file_path_s + i for i in os.listdir(file_path_s)])
file_lfp = sorted([file_path_l + i for i in os.listdir(file_path_l)])

# condition setups
cond = ['nn_3_1', 'nn_wn_3_1', 'nn_1_1', 'nn_wn_1_1']  # conditions for offset response experiment

lfp_70 = [[] for _ in range(len(cond))]
lfp_60 = [[] for _ in range(len(cond))]

spk_70 = [[] for _ in range(len(cond))]
spk_60 = [[] for _ in range(len(cond))]
# cond = ['nn_1_1']

for dat_index in range(len(file_spk)):

    for c in range(len(cond)):
        condition = cond[c]
        d_spk = file_spk[dat_index]
        d_lfp = file_lfp[dat_index]
        animal = d_spk.split('/')[-1].split('_')[0]

        if condition in cond[2:4] and animal == 'cr103':
            continue
        else:
            data = nt.OffsetPrepare(d_spk, d_lfp, condition)
            spk = data.spk_psth()[1]
            lfp = data.lfp_seg()[1]
            spk_70[c].append(spk[0])
            lfp_70[c].append(lfp[0])

            if len(lfp) > 1:
                spk_60[c].append(spk[1])
                lfp_60[c].append(lfp[1])

                if condition == cond[2] or condition == cond[3]:
                    print(condition, animal, '60')


scipy.io.savemat('nn_3_1_70.mat', {'psth': spk_70[0], 'lfp': lfp_70[0]})
scipy.io.savemat('wn_3_1_70.mat', {'psth': spk_70[1], 'lfp': lfp_70[1]})
scipy.io.savemat('nn_3_1_60.mat', {'psth': spk_60[0], 'lfp': lfp_60[0]})
scipy.io.savemat('wn_3_1_60.mat', {'psth': spk_60[1], 'lfp': lfp_60[1]})

scipy.io.savemat('nn_1_1_70.mat', {'psth': spk_70[2], 'lfp': lfp_70[2]})
scipy.io.savemat('wn_1_1_70.mat', {'psth': spk_70[3], 'lfp': lfp_70[3]})
scipy.io.savemat('nn_1_1_60.mat', {'psth': spk_60[2], 'lfp': lfp_60[2]})
scipy.io.savemat('wn_1_1_60.mat', {'psth': spk_60[3], 'lfp': lfp_60[3]})
