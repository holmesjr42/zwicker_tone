import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import pickle
from parameter import parameters as pm
import h5py
import quantities as pq
from tools import spike_tools as st
import quantities as pq

sys.path.pop(1)

# file_input = ["/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr50_190724_spk_lfp_avg_nnm.hdf5",
#               "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm"
#               ".hdf5"
#               ]
#
file_input = snakemake.input

f31 = ['cr33', 'cr50', 'cr79', 'cr90', 'cr94']
group = {'lfp': {}, 'spk': {}}
g_t = list(group.keys())
types = ['lfp', 'tsp']
conds = ['nnm_3_0', 'nnm_3_0_strf']
conds2 = ['nnm_3_1', 'nnm_3_1', 'nnm_wn_3_1', 'nnm_wn_3_1', 'nnm_3_1_strf']
conds3 = ['nn', 'si', 'nn', 'si', 'blank']
cond2_k = [
    'nnm_3_1_on', 'nnm_3_1_off', 'nnm_wn_3_1_on',
    'nnm_wn_3_1_off', 'nnm_3_1_strf'
    ]
db = ['70', '60', '50', '40']
ch = 16
cf = 12

# continuous notched noise
for t in range(len(types)):
    for cond in conds:
        group[g_t[t]][cond] = {}
        for d in db:
            a_temp = []
            for file in file_input:
                f_temp = []
                with h5py.File(file, 'r') as dat:
                    d_type = dat[types[t]]
                    if np.any(d_type[cond][d]):
                        for c in range(16):
                            f_temp.append(d_type[cond][d][c][cf])
                    else:
                        continue
                if g_t[t] == 'lfp':
                    f_temp = f_temp * pq.microvolt
                    f_temp.units = pq.mV
                elif g_t[t] == 'spk':
                    f_temp = f_temp * pq.ms**(-1)
                    f_temp.units = pq.s**(-1)

                a_temp.append(f_temp)
            group[g_t[t]][cond][d] = a_temp


# nn-on/off

for t in range(len(types)):
    for cs in range(len(conds2)):
        con2 = conds2[cs]
        con3 = conds3[cs]
        conk = cond2_k[cs]
        group[g_t[t]][conk] = {}
        for d in db:
            a_temp = []
            for file in file_input:
                f_temp = []
                if file.split('/')[-1].split('_')[0] in f31:
                    if 'strf' in con2:
                        with h5py.File(file, 'r') as dat:
                            d_type = dat[types[t]]
                            for c in range(16):
                                f_temp.append(d_type[con2][d][c][cf])
                    else:
                        with h5py.File(file, 'r') as dat:
                            d_type = dat[types[t]]
                            for c in range(16):
                                f_temp.append(d_type[con2][con3][d][c][cf])
                else:
                    continue

                if g_t[t] == 'lfp':
                    f_temp = f_temp * pq.microvolt
                    f_temp.units = pq.mV
                elif g_t[t] == 'spk':
                    f_temp = f_temp * pq.ms**(-1)
                    f_temp.units = pq.s**(-1)

                a_temp.append(f_temp)
            group[g_t[t]][conk][d] = a_temp


with h5py.File(snakemake.output[0], 'w') as hs:
    for data in list(group.keys()):
        h1 = hs.create_group(data)
        for cond in list(group[data].keys()):
            h2 = h1.create_group(cond)
            for db in list(group[data][cond].keys()):
                h3 = h2.create_dataset(db, data=group[data][cond][db])
