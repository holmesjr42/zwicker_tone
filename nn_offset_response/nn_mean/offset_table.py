import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from tools import nn_tool as nt
from parameter import parameters as pm
import pickle
import quantities as pq
import pandas as pd
sys.path.pop(1)

'''
This is to create offset response table.
'''

'''
setup
'''

files = snakemake.input

# files = ["/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/nn_mean/cr31_190312_nn_mean.hdf5",
#          "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/nn_mean/cr33_190321_nn_mean.hdf5",
#          "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset"
#          "/nn_mean/cr50_190724_nn_mean.hdf5",
#          "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/nn_mean/cl116_210318_nn_mean.hdf5"]

sets = pm.Nn().setup()
types = ['lfp', 'spk']  # data type
names = sets[0][0:4]  # name of conditions
dbs = sets[1]  # SPL for nn_offset
dats = ['mean', 's_psth']  # lfp session mean/quantile
group = {'animal': [], 'data': [], 'condition': [], 'dB': [], 'Offset': []}
g_list = list(group.keys())
# 0.25/0.75, spk session rastor, psths, time
for ty in range(len(types)):
    t = types[ty]
    ds = dats[ty]
    for n in names:  # condition names
        if '1_1' in n:
            if t == 'lfp':
                ti = nt.lfp_index(1500)
                tf = nt.lfp_index(1990) + 1
                oi = nt.lfp_index(1000)
                of = nt.lfp_index(1100) + 1
            elif t == 'spk':
                ti = 1500
                tf = 1991
                oi = 1000
                of = 1101

        elif '3_1' in n:
            if t == 'lfp':
                ti = nt.lfp_index(3500)
                tf = nt.lfp_index(3990) + 1
                oi = nt.lfp_index(3000)
                of = nt.lfp_index(3100) + 1
            elif t == 'spk':
                ti = 3500
                tf = 3991
                oi = 3000
                of = 3101
        else:
            print('something is wrong with the condition name.')
            raise ValueError

        for db in range(len(dbs)):
            for file in files:
                with h5py.File(file, 'r') as dat:
                    if n in list(dat[t][ds].keys()) and db < len(
                            dat[t][ds][n]):
                        dat1 = dat[t][ds][n][db]
                        k = 0
                        for j in range(len(dat1)):
                            std = np.std(dat1[j][ti:tf])
                            mean = np.mean(dat1[j][ti:tf])
                            base = np.abs(mean) + 2 * np.abs(std)

                            if np.max(np.abs(dat1[j][oi:of])) > base:
                                k += 1
                            else:
                                answer = 'no'

                            # g = [
                            #     file.split('/')[-1].split('_')[0],
                            #     t, n, dbs[db], answer
                            #     ]
                        if (k / 16) > 0.7:
                            answer = 'yes'
                        else:
                            answer = 'no'

                        g = [
                            file.split('/')[-1].split('_')[0],
                            t, n, dbs[db], answer
                            ]
                        for i in range(len(g)):
                            group[g_list[i]].append(g[i])
                    else:
                        continue

df = pd.DataFrame(group, columns=g_list)
# df.to_csv(r'offset_table.csv')
df.to_csv(snakemake.output[0])
