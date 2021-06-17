import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import h5py
import json
from parameter import parameters as pm
from tools import spike_tools as st
import quantities as pq
sys.path.pop(1)

'''
This is creating average of spk/lfp ratio change with confidential interval
09/03/2021 change: instead of layerwise mean, I choose one channel which 
represents each layer
'''

'''
setup
'''
file_input = snakemake.input
# file_input = ["/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr29_190228_spk_lfp_avg_nnm.hdf5",
#               "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr50_190724_spk_lfp_avg_nnm.hdf5",
#               "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm"
#               ".hdf5"
#               ]

com = pm.Commonfeat  # common features

# animal/data folder name
animals = []
for i in range(len(file_input)):
    animals = np.append(animals, file_input[i].split('/')[-1].split('_')[0])

# data coordination of each animal
db = com.db

# for details, check data_list.ods
lvs = db['lv']  # SPLdB list

# channels for layer: supra, granular, infra
ch_l = com.ch_l

nc = ['nnm_3_0_strf', 'nnm_3_0']

l_list = ['supr', 'gran', 'infr']  # list of layers

g_list = ['fps', 'fpl', 'base']  # list of the data types
finx = [4, 12, 20]  # index of lower edge, center, higher edge freq

g_sf = {}
g_lf = {}
g_bs = {}
group2 = [g_sf, g_lf, g_bs]

for group in [g_sf, g_lf, g_bs]:
    for cond in nc:
        group[cond] = {}
        for ls in l_list:
            group[cond][ls] = {}
            for lv in lvs:
                group[cond][ls][lv] = []

                # sms.DescrStatsW(a_f2[p][q]).tconfint_mean()

for lv in lvs:
    levels = []
    for file in range(len(file_input)):
        with h5py.File(file_input[file], 'r') as dat:

            '''nnm continuous spikes & LFP'''
            #
            fps = [dat['mfpt'][nc[0]][lv], dat['mfpt'][nc[1]][lv]]
            fpl = [dat['mfpl'][nc[0]][lv], dat['mfpl'][nc[1]][lv]]
            base = [dat['base'][nc[0]][lv], dat['base'][nc[1]][lv]]

            group1 = [fps, fpl, base]

            if not np.any(fps[1]):
                continue
            else:
                for g in range(len(group1)):
                    g1 = np.array(st.unit_trans(group1[g], g_list[g]))
                    g2 = group2[g]
                    for ls in range(len(l_list)):

                        lc = g1[0][ch_l[ls]]
                        ln = g1[1][ch_l[ls]]

                        g2[nc[0]][l_list[ls]][lv].append(lc)
                        g2[nc[1]][l_list[ls]][lv].append(ln)

names = ['fps', 'fpl']
groups = {'fps': g_sf, 'fpl': g_lf, 'base': g_bs}

with h5py.File(snakemake.output[0], 'w') as hs:
    for data in list(groups.keys()):
        h1 = hs.create_group(data)
        for cond in list(g_lf.keys()):
            h2 = h1.create_group(cond)
            for layer in list(g_lf[cond].keys()):
                h3 = h2.create_group(layer)
                for lv in list(g_lf[cond][layer].keys()):
                    h4 = h3.create_dataset(
                        lv, data=groups[data][cond][layer][lv]
                        )


