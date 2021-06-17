import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import h5py
import numpy as np
from parameter import parameters as pm
import pickle

sys.path.pop(1)

'''
This is creating average of spk/lfp for offset response.
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
names = sets[0]  # name of conditions
dbs = sets[1]  # SPL for nn_offset
dats = {'lfp': sets[2], 'spk': sets[3]}  # lfp session mean/quantile
f_group = {'lfp': {}, 'spk': {}}
# 0.25/0.75, spk session rastor, psths, time

'''
data retrieve
'''
for t in types:
    for ds in dats[t]:
        f_group[t][ds] = {}
        # ds is a key for different data analysis type e.g.:
        # quantile, mean , lfp; psth, rastor, smoothed psth, time, spk
        for n in names:  # condition names
            f_group[t][ds][n] = []
            for db in range(len(dbs)):
                m_temp = []  # temporary array to do mean over animals
                for file in files:
                    with h5py.File(file, 'r') as dat:
                        if n in list(dat[t][ds].keys()) and db < len(dat[t][ds][n]):
                            dat1 = dat[t][ds][n][db]
                            m_temp.append(dat1)
                        else:
                            continue
                f_group[t][ds][n].append(np.mean(m_temp, axis=0))

with h5py.File(snakemake.output[0], 'w') as h:
    for t in list(f_group.keys()):
        d1 = h.create_group(t)
        for ds in list(f_group[t].keys()):
            d2 = d1.create_group(ds)
            for n in list(f_group[t][ds].keys()):
                d3 = d2.create_dataset(
                    n, data=f_group[t][ds][n])
