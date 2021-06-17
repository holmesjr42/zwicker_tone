import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import h5py
from parameter import parameters as pm
from tools import spike_tools as st
from tools import nn_tool as nt
import quantities as pq
import pandas as pd

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
#               "/data/dataset/nnm_spk_lfp_avg/cr31_190312_spk_lfp_avg_nnm.hdf5",
#               "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr50_190724_spk_lfp_avg_nnm.hdf5",
#               "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021"
#               "/data/dataset/nnm_spk_lfp_avg/cr79_200211_spk_lfp_avg_nnm"
#               ".hdf5"
#               ]


com = pm.Commonfeat  # common features
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
sets = val.extra_setup()
# animal/data folder name
animals = []

for i in range(len(file_input)):
    animals = np.append(animals, file_input[i].split('/')[-1].split('_')[0])

# data coordination of each animal
db = com.db

# for details, check data_list.ods
lvs = db['lv']  # SPLdB list

# condition keys
nc = ['nnm_3_1_strf', 'nnm_3_1', 'nnm_wn_3_1']

l_list = ['supr', 'gran', 'infr']  # list of layers

g_list = ['mfpt', 'mfpl']  # list of the data types
g_list2 = ['spk', 'lfp']

types = ['control', 'nn_on', 'nn_off', 'wn_off']

g_s = {
    'firing_rate': [], 'channel': [], 'dB': [], 'layer': [],
    'condition': [], 'sample': []
    }

g_l = {
    'amplitude': [], 'channel': [], 'dB': [], 'layer': [],
    'condition': [], 'sample': []
    }
groups = [g_s, g_l]
c_list = list(g_s.keys())
# indice list of low edge, center, high edge, 0.5 oct above/below  of notch gap
find = [sets[3][1], sets[3][-2]]

for g in range(len(g_list)):
    g_key = g_list[g]
    g_name = g_list2[g]
    group = groups[g]
    c_list = list(group.keys())
    for lv in lvs:
        for file in range(len(file_input)):
            with h5py.File(file_input[file], 'r') as dat:
                f_name = file_input[file].split('/')[-1].split('_')[0]
                '''nnm chunk spikes & LFP'''

                fp = [
                    dat[g_key][nc[0]][lv], dat[g_key][nc[1]]['nn'][lv],
                    dat[g_key][nc[1]]['si'][lv], dat[g_key][nc[2]]['si'][lv]
                    ]
                for t in range(len(types)):
                    cond = types[t]
                    data = nt.dat_unit(fp[t], types=g_name)
                    for ch in range(len(data)):
                        if ch < 4:
                            layer = 'supra'
                        elif 3 < ch < 8:
                            layer = 'granular'
                        elif 7 < ch:
                            layer = 'infra'
                        else:
                            print('channel number is weird')
                            raise ValueError

                        max_f = nt.freq_find(data[ch], find, type=g_name)
                        mx = data[ch][max_f].magnitude

                        temps = [mx, ch, lv, layer, cond, f_name]

                        for j in range(len(c_list)):
                            group[c_list[j]].append(temps[j])

s_list = list(g_s.keys())
l_list = list(g_l.keys())
ds = pd.DataFrame(g_s, columns=s_list)
dl = pd.DataFrame(g_l, columns=l_list)

# ds.to_csv(r'3_1_spk.csv')
# dl.to_csv(r'3_1_lfp.csv')
ds.to_csv(snakemake.output.spk)
dl.to_csv(snakemake.output.lfp)