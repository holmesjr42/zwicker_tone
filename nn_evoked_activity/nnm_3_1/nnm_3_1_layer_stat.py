import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import matplotlib.pyplot as plt
from parameter import parameters as pm
import h5py
from matplotlib.colors import ListedColormap
from tools import nnm_plot as nnmp
import pylustrator
import quantities as pq
from tools import nn_tool as nt
import pandas as pd
from scipy import stats

pylustrator.start()
sys.path.pop(1)

'''
Create heatmap for firing rate
'''

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some setups for plotting e.g. color scheme
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
sets = val.extra_setup()
lvl = com.db['lv']  # SPLdB list

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_1.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
cc = sets[-2][0]
cnn = sets[-5][0]
cnf = sets[-4][0]
cwf = sets[-3][0]
conds = [cc, cnn, cnf, cwf]

# control, nn-on, nn-off, wn-off
paradigm = sets[6]
l_n = sets[1]
l_list = sets[2]
octs = com.octaves  # list of octaves
# list of layer names
layer_name = sets[0]
d_type = ['spk', 'lfp']

# indice of edge frequencies in octaves
find = [sets[3][1], sets[3][-2]]
# dic for dataframe
dataf = {
    'data': [], 'level': [], 'cond': [], 'statistic': [], 'pvalue': []
    }
c_list = list(dataf.keys())

# load file
with h5py.File(file_input, 'r') as dat:
    lp = [dat['fpl'][cc], dat['fpl'][cnn],
          dat['fpl'][cnf], dat['fpl'][cwf]]  # spk
    sk = [dat['fps'][cc], dat['fps'][cnn],
          dat['fps'][cnf], dat['fps'][cwf]]

    s_data = [sk, lp]
    for d in range(len(d_type)):
        stype = s_data[d]
        for lv in lvl:
            for k in range(len(s_data[d])):
                temp = [[] for _ in range(3)]
                for l in range(len(l_list)):
                    ly = l_list[l]

                    # list of the max/min spk/lfp frequency in nn band
                    fm = []
                    dt = stype[1][ly][lv]
                    for a in range(len(dt)):
                        fm = nt.freq_find(dt[a], find, type=d_type[d])
                        temp[l].append(s_data[d][k][ly][lv][a][fm])

                test = stats.friedmanchisquare(temp[0], temp[1], temp[2])
                stemp = [d_type[d], lv, conds[k], test[0], test[1]]
                for j in range(len(c_list)):
                    dataf[c_list[j]].append(stemp[j])

df = pd.DataFrame(dataf, columns=c_list)
df.to_csv(r'fp_layer_stat2.csv')
