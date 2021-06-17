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

# stimulus conditions for this script
nconds = [sets[-5][0], sets[-4][0], sets[-3][0]]
cconds = [sets[-2][0], sets[-2][0], sets[-2][0]]

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
    'data': [], 'layer': [], 'cond': [], 'pvalue': []
    }
c_list = list(dataf.keys())

# load file
with h5py.File(file_input, 'r') as dat:
    lp = dat['fpl']
    sk = dat['fps']
    base = dat['base']
    s_data = [sk, lp]
    for d in range(len(d_type)):
        stype = s_data[d]
        dtype = d_type[d]
        for l in range(len(l_list)):
            ly = l_list[l]
            for c in range(len(nconds)):
                cn = nconds[c]
                cs = cconds[c]
                templv = []
                for lvn in range(len(lvl)):
                    lv = lvl[lvn]

                    teemp = nt.diff_on_off(stype, ly, lv, cn, cs,
                                           nconds[0], bdata=base, types=dtype
                        )
                    templv.append(teemp[3])
                test = stats.friedmanchisquare(
                    templv[0], templv[1], templv[2], templv[3]
                    )

                s_df = [dtype, l_list[l], nconds[c], test[1]]

                for z in range(len(c_list)):
                    dataf[c_list[z]].append(s_df[z])

df = pd.DataFrame(dataf, columns=c_list)
df.to_csv(r'fp_diff_stat2.csv')