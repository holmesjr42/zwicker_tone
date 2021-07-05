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

# file_spk = snakemake.input.spk
# file_lfp = snakemake.input.lfp
# file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr31_190312_tsp.hdf5']
# file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr31_190312_lfp_fil.hdf5']
file_spk = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/tsp/cr50_190724_tsp.hdf5']
file_lfp = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data/dataset/lfp_fil/cr50_190724_lfp_fil.hdf5']
# condition setups
cond = [['nn_3_1', 'nn_wn_3_1'], ['nn_1_1', 'nn_wn_1_1']]  # conditions for offset response experiment
t_ind = [pm.Nn.nn_i['nn31'], pm.Nn.nn_i['nn11']]  # indices for each condition sessions
offset = [3000, 1000]  # offset start points for 3 / 1 and 1 / 1
lvs = ['70', '60']  # spl db you are going to use
group = {}
types = ['spk', 'lfp']

for f in range(len(file_spk)):
    s_input = file_spk[f]
    l_input = file_lfp[f]
    s_ref = [[] for _ in range(len(cond))]
    l_ref = [[] for _ in range(len(cond))]
    animal = nnp.animal_name(s_input)
    group[animal] = {}
    with h5py.File(s_input, 'r') as s_dat:
        with h5py.File(l_input, 'r') as l_dat:
            for lv in range(len(lvs)):
                for j in range(len(cond)):  # choosing between 3 / 1 and 1 / 1
                    if animal == 'cr103' and 'nn_1_1' in cond[j]:
                        s_ref[j] = np.zeros([2, 16, 2])
                        l_ref[j] = np.zeros([2, 16, 2])
                    else:
                        ti = ind[j][0]
                        tf = ind[j][1]
                        t_off = offset[j]
                        s_ths = [[] for _ in range(len(cond[j]))]
                        l_ths = [[] for _ in range(len(cond[j]))]
                        for k in range(len(cond[j])):  # choosing between notch and white noise
                            s_data = s_dat[cond[j][k]]
                            l_data = l_dat[cond[j][k]]

                            if lv <= len(s_data) - 1:
                                # spk
                                mua = nt.index_spike(s_data[lv])
                                s_ths[k].extend(nt.threshold_collect(mua, ti, tf, t_off, type='spk'))

                                # lfp
                                lfp = []
                                for g in range(len(l_data[lv])):
                                    lfp.append(l_data[lv][g])
                                lfp = np.array(lfp)
                                l_ths[k].extend(nt.threshold_collect(lfp, ti, tf, t_off, type='lfp'))
                            else:
                                continue
                        if np.shape(s_ths)[1] != 0:
                            s_bases = np.concatenate(s_ths, axis=1)
                            l_bases = np.concatenate(l_ths, axis=1)
                        else:
                            continue

                        s_base = np.array([np.mean(s_bases, axis=1), np.std(s_bases, axis=1)])
                        l_base = np.array([np.mean(l_bases, axis=1), np.std(l_bases, axis=1)])

                        s_ref[j].append(s_base.T)
                        l_ref[j].append(l_base.T)

            group[animal]['spk'] = s_ref
            group[animal]['lfp'] = l_ref

    # l_ref = [[] for _ in range(len(cond))]
    # with h5py.File(l_input, 'r') as dat:
    #     for lv in range(len(lvs)):
    #         for j in range(len(cond)):  # choosing between 3 / 1 and 1 / 1
    #             if animal == 'cr103' and 'nn_1_1' in cond[j]:
    #                 s_ref[j] = np.zeros([2, 16, 2])
    #             else:
    #                 ti = ind[j][0]
    #                 tf = ind[j][1]
    #                 t_off = offset[j]
    #                 ths = [[] for _ in range(len(cond[j]))]
    #                 for k in range(len(cond[j])):  # choosing between notch and white noise
    #                     data = dat[cond[j][k]]
    #                     if lv <= len(data) - 1:
    #                         mua = nt.index_spike(data[lv])
    #                         ths[k].extend(nt.threshold_collect(mua, ti, tf, t_off))
    #                     else:
    #                         continue
    #                 if np.shape(ths)[1] != 0:
    #                     bases = np.concatenate(ths, axis=1)
    #                     base = np.array([np.mean(bases, axis=1), np.std(bases, axis=1)])
    #                     s_ref[j].append(base.T)
    #                 else:
    #                     continue

with h5py.File(snakemake.output[0], 'w') as h:
    for t0 in list(group.keys()):
        d1 = h.create_group(t0)
        for t1 in types:
            d2 = d1.create_dataset(t1, data=group[t0][t1])
