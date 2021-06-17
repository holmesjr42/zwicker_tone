import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))
import numpy as np
import h5py
import json
from parameters import parameters as pm
import statsmodels.stats.api as sms
import quantities as pq
import neo.core
from tools import icsd
from tools import spike_tools as spt

sys.path.pop(1)

'''
This is creating average of spk/lfp ratio change with confidential interval
'''

'''
setup
'''
# file_input = snakemake.input
file_input = ["/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
              "/data/dataset/nnm_spk_lfp_avg/cr29_190228_spk_lfp_avg_nnm.hdf5",
              "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
              "/data/dataset/nnm_spk_lfp_avg/cr50_190724_spk_lfp_avg_nnm.hdf5",
              "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
              "/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm"
              ".hdf5"
              ]

com = pm.Commonfeat  # common features

# animal/data folder name
animals = []
for i in range(len(file_input)):
    animals = np.append(animals, file_input[i].split('/')[-1].split('_')[0])

# data coordination of each animal
db = com.db

# for details, check data_list.ods
acor = db['animal']  # animal coordination
lvs = db['lv']  # SPLdB list

# channels for layer: supra, granular, infra
ch_l = [[0, 6], [6, 9], [9, 16]]

ns = [['nnm_3_1_strf', 'nnm_3_1'], ['nnm_3_1_strf', 'nnm_wn_3_1']]

nc = [
    ['nnm_3_1_strf', 'nnm_3_1_on', 'nnm_3_1_off'],
    ['nnm_3_1_wn_strf', 'nnm_wn_3_1_on', 'nnm_wn_3_1_off']
    ]

l_list = ['supr', 'gran', 'infr']  # list of layers

g_sf = {}
g_lf = {}
g_bs = {}


for cond1 in nc:
    for cond in cond1:
        for group in [g_sf, g_lf, g_bs]:
            group[cond] = {}
            for ls in l_list:
                group[cond][ls] = {}
                for lv in lvs:
                    group[cond][ls][lv] = []


group2 = [g_sf, g_lf, g_bs]

for lv in lvs:
    levels = []
    for file in range(len(file_input)):
        with h5py.File(file_input[file], 'r') as dat:
            for i in range(len(nc)):
                ns1 = ns[i]
                nc1 = nc[i]

                '''ON-OFF spikes & LFP'''

                fps = [
                    dat['fpt'][ns1[0]][lv],
                    dat['fpt'][ns1[1]]['nn'][lv],
                    dat['fpt'][ns1[1]]['si'][lv]
                       ]
                fpl = [
                    dat['fpl'][ns1[0]][lv],
                    dat['fpl'][ns1[1]]['nn'][lv],
                    dat['fpl'][ns1[1]]['si'][lv]
                       ]

                base = [
                    dat['base'][ns1[0]][lv],
                    dat['base'][ns1[1]]['nn'][lv],
                    dat['base'][ns1[1]]['si'][lv]
                       ]

                group1 = [fps, fpl, base]

                if not np.any(fps[1]):
                    continue
                else:
                    for g in range(len(group1)):
                        for ls in range(len(l_list)):

                            g1 = np.array(group1[g])
                            g2 = group2[g]

                            lc = np.mean(
                                g1[0][ch_l[ls][0]:ch_l[ls][1]], axis=0
                                )
                            ln_on = np.mean(
                                g1[1][ch_l[ls][0]:ch_l[ls][1]], axis=0
                                )
                            ln_off = np.mean(
                                g1[2][ch_l[ls][0]:ch_l[ls][1]], axis=0
                                )

                            g2[nc1[0]][l_list[ls]][lv].append(lc)
                            g2[nc1[1]][l_list[ls]][lv].append(ln_on)
                            g2[nc1[2]][l_list[ls]][lv].append(ln_off)


names = ['fps', 'fpl', 'base']
groups = {'fps': g_sf, 'fpl': g_lf, 'base': g_bs}

# with h5py.File(snakemake.output[0], 'w') as hs:
#     for data in list(groups.keys()):
#         h1 = hs.create_group(data)
#         for cond in list(groups[data].keys()):
#             h2 = h1.create_group(cond)
#             for layer in list(groups[data][cond].keys()):
#                 h3 = h2.create_group(layer)
#                 for lv in list(groups[data][cond][layer].keys()):
#                     h4 = h3.create_dataset(
#                         lv, data=groups[data][cond][layer][lv]
#                         )
#
