import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
from parameter import parameters as pm
import h5py
from tools import nn_tool as nt
import pandas as pd
from scipy import stats

'''
This is a script to produce p value data set for nnm_3_0: both frequency 
profile and difference ratio.
'''
# file I'm going to use
file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_0.hdf5'

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some features for name/condition to retrieve data from the dataset
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

# stimulus conditions for this script
cn = sets[7][0]
cs = sets[8][0]
cond = ['control', 'nn']
# layer name list and dic key list of layers
layer_name = sets[0]
l_list = sets[2]

# indice of edge frequencies in octaves
find = [sets[3][1], sets[3][-2]]
f_name = [sets[5][0], sets[5][2]]
# dissertation

#  loading data

dataf = {
    'data': [], 'cond': [], 'level': [], 'statistic': [], 'pvalue': []
    }
c_list = list(dataf.keys())
d_list = ['fps', 'fpl']
t_list = ['spk', 'lfp']

with h5py.File(file_input, 'r') as dat:
    fps = dat['fps']
    fpl = dat['fpl']
    base = dat['base']
    ds = [fps, fpl]
    t = ['spk', 'lfp']
    for d in range(len(ds)):
        dats = ds[d]
        d_n = d_list[d]
        for lv in lvl:
            fm = []
            dt = dats[cn][l_list[1]][lv]
            for a in range(len(dt)):
                fm.append(nt.freq_find(dt[a], find, type=t[d]))
            for c in [cs, cn]:
                d_layer = [[] for _ in range(3)]
                for layer in range(len(l_list)):
                    dls = d_layer[layer]
                    ly = l_list[layer]

                    dt2 = dats[c][ly][lv]

                    for i in range(len(dt2)):
                        d_layer[layer] = np.append(d_layer[layer], dt2[i][fm[i]])

                testc = stats.friedmanchisquare(
                    d_layer[0], d_layer[1], d_layer[2]
                    )
                testf = [d_list[d], c, lv, testc[0], testc[1]]

                for j in range(len(c_list)):
                    dataf[c_list[j]].append(testf[j])


    df = pd.DataFrame(dataf, columns=c_list)
    print(df)
    df.to_csv(r'fp_layer.csv')
