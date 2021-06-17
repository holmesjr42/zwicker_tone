import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))

import h5py
from tools import nn_tool as nt
import pickle
import quantities as pq

sys.path.pop(1)

'''
This is creating average of spk/lfp for offset response in the three layers
'''

'''
setup
'''
# file_input = snakemake.input


'''
This is for a single animal data
plots psth and averaged raw lfp in the same figure
'''

d_lfp = snakemake.input.lfp
d_spk = snakemake.input.spk

# d_lfp = ["/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/nn_lfp_avg/cr92_201029_nn_lfp_a.pk",
#          "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/nn_lfp_avg/cr93_201110_nn_lfp_a.pk",
#          "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/nn_lfp_avg/cr95_201117_nn_lfp_a.pk"]
#
# d_spk = ["/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/tsp/cr92_201029_tsp.hdf5",
#          "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/tsp/cr93_201110_tsp.hdf5",
#          "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data"
#          "/dataset/tsp/cr95_201117_tsp.hdf5"]
#

# with open(d_lfp, 'rb') as dat:
#     a = pickle.load(dat)
# with h5py.File(d_spk, 'r') as h_5:

'''
setup
'''
dbs = ['70', '60']
# channels for layer: supra, granular, infra
ch_l = [0, 7, 11]
l_list = ['supr', 'gran', 'infr']  # list of layers
# names of the conditions
names = ['nn_1_1', 'nn_wn_1_1']
nn = names[0]
wn = names[1]

# spk
nrastor = {}
npsth = {}
nsmooth = {}
ntime = {}

'''
data retrieve
'''
# if animal == 'cr31' or animal == 'cr33':
#     plt.figure()
#     plt.savefig(snakemake.output[1], dpi=150)
#     db = [0]
# else:
#     db = [0, 1]

db = [0, 1]

g_sf = {}  # storing spk data
g_lf = {}  # storing lfp data

# lfp partition
for d in db:
    s = dbs[d]
    g_lf[s] = {}
    g_sf[s] = {}
    for n in names:
        g_lf[s][n] = {}
        g_sf[s][n] = {}
        for l in l_list:
            g_lf[s][n][l] = []
            g_sf[s][n][l] = []

for l_file in d_lfp:
    for n in names:
        for lv in db:
            d = dbs[lv]
            # lfp
            with open(l_file, 'rb') as datas:
                dat = pickle.load(datas)
                la = dat['la']
            # onset/offset points and change the unit
            la_n = la[n][d] * pq.microvolt
            la_n.units = pq.mV

            for i in range(len(ch_l)):
                g_lf[d][n][l_list[i]].append(la_n[ch_l[i]])

for s_file in d_spk:
    # spike
    with h5py.File(s_file, 'r') as h_5:
        for n in names:
            for lv in db:
                d = dbs[lv]
                mua = h_5[n][lv]
                nn = nt.index_spike(mua)
                nrastor[n], npsth[n], nsmooth[n], ntime[n] = nt.psth(nn, n)

                nsmooth[n] = nsmooth[n] * pq.ms**(-1)
                nsmooth[n].units = pq.s ** (-1)

                for i in range(len(ch_l)):
                    g_sf[d][n][l_list[i]].append(nsmooth[n][ch_l[i]])

names = ['spk', 'lfp']
groups = {'spk': g_sf, 'lfp': g_lf}

with h5py.File(snakemake.output[0], 'w') as hs:
# with h5py.File('test.hdf5', 'w') as hs:
    for data in list(groups.keys()):
        h1 = hs.create_group(data)
        for lv in list(groups[data].keys()):
            h2 = h1.create_group(lv)
            for cond in list(groups[data][lv].keys()):
                h3 = h2.create_group(cond)
                for layer in list(groups[data][lv][cond].keys()):
                    h4 = h3.create_dataset(
                        layer, data=groups[data][lv][cond][layer]
                        )
