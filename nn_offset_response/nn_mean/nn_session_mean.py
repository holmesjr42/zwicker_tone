import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

from tools import spike_tools as st
import h5py
from tools import nn_tool as nt
from parameter import parameters as pm
import numpy as np
import statsmodels.stats.api as sms

sys.path.pop(1)

'''
This is for having averaged LFP signal for a single animal data with 3 s/ 1 
s 1 s/ 1 s NN/WN condition in hdf5. spk/lfp unit is updated in this script as 
1/s or mV by function.
'''

# d_lfp = snakemake.input.lfp
# d_spk = snakemake.input.spk
d_lfp = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
        "/dataset/lfp_fil/cr90_201023_lfp_fil.hdf5"

d_spk = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
        "/dataset/tsp/cr90_201023_tsp.hdf5"

animal = d_lfp.split('/')[-1].split('_')[0]
sets = pm.Nn().setup()

'''
setup
'''
data = [d_lfp, d_spk]
# lfp session mean, quantile 25%, all the sweep data before mean
lfp = {'mean': {}, 'q27': {}, 'sweep': {}}
spk = {'rastor': {}, 'psth': {}, 's_psth': {}, 'time': {}}
s_list = list(spk.keys())
# spke rastor, psth, smoothed psth, time
types = ['lfp', 'spk']
names = sets[0]
db = sets[1]

'''
data retrieve
'''
# lfp
for t in range(len(types)):
    d_file = data[t]
    dt = types[t]

    with h5py.File(d_file, 'r') as f:
        for n in names:
            if n in list(f.keys()):
                # lfp
                if dt == 'lfp':
                    lfp['mean'][n] = []
                    lfp['q27'][n] = []
                    for i in range(len(f[n])):
                        dat = f[n][i]
                        lst = nt.lfp_seg(dat, n)
                        l_temp = []  # dissertation storage for lfp mean
                        c_temp = []  # dissertation storage for lfp quantile 0.25/0.75
                        for j in range(len(lst)):  # number of channels

                            # processing session mean
                            l_temp.append(
                                np.mean(lst[j][:-1], axis=0)
                                )
                            # processing session quantile
                            lst2 = np.transpose(lst[j])
                            lcs = []
                            for j2 in range(len(lst2)):
                                lcs.append(
                                    np.array(
                                        [np.quantile(lst2[j2], 0.25),
                                         np.quantile(lst2[j2], 0.75)]
                                        )
                                    )
                            c_temp.append(lcs)
                        lfp['mean'][n].append(l_temp)
                        lfp['q27'][n].append(c_temp)
                        lfp['sweep'][n] = lst
                        print(f'{animal}, {dt}: {n} at {db[i]} is done')
                # spk
                elif dt == 'spk':
                    for subs in s_list:
                        spk[subs][n] = []
                    for i in range(len(f[n])):
                        mua = f[n][i]
                        nn = nt.index_spike(mua)
                        s_temp = nt.psth(nn, n)
                        for j in range(len(s_list)):
                            sub = s_list[j]
                            spk[sub][n].append(s_temp[j])
                        print(f'{animal}, {dt}: {n} at {db[i]} is done')

group = {'lfp': lfp, 'spk': spk}

with h5py.File(snakemake.output[0], 'w') as h:
# with h5py.File('test_01.hdf5', 'w') as h:
    for t in list(group.keys()):
        d1 = h.create_group(t)
        for n in list(group[t].keys()):
            d2 = d1.create_group(n)
            for l in list(group[t][n].keys()):
                d3 = d2.create_dataset(
                    l, data=group[t][n][l])
