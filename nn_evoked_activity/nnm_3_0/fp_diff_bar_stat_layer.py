import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
from parameter import parameters as pm
import h5py
from tools import nn_tool as nt
from scipy import stats
import pandas as pd

sys.path.pop(1)

'''
spk/lfp difference rate comparison between NN and control with edge and band 
min/max 
freq.
'''

# import features
nnc = pm.Nnmcontfeat
nns = pm.Nnsifeat
com = pm.Commonfeat

# some setups for plotting e.g. color scheme
val = pm.Setup(cond='nnm_3_0', cond2='tsp', mode=1)
mode, ylc, condc, condt, nb, ch, depth, dcmap, ws, hs, rt, cct, cb, ccmap = \
    val.values()
lvl = com.db['lv']  # SPLdB list
sets = val.extra_setup()

file_input = '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
             '/data/dataset/fp_layer/fp_layer_nnm_3_0.hdf5'
# file_input = snakemake.input[0]

# stimulus conditions for this script
cn = sets[7][0]
cs = sets[8][0]

# layer keys for dataset
l_list = sets[2]

# dic for difference ratio and quartile 25/75


ratio = {'data': [], 'SPL dB': [], 'p-value': []}
r_list = list(ratio.keys())
d_type = ['spk', 'lfp']
r_name = ['SPK', 'LFP']
# load file
with h5py.File(file_input, 'r') as dat:
    # spk, lfp, baseline data
    data = [dat['fps'], dat['fpl'], dat['base']]
    for d in range(len(d_type)):
        for lv in lvl:
            temp2 = []
            for layer in l_list:

                temp = nt.diff(
                    data[d], layer, lv, cn, cs,
                    bdata=data[2], types=d_type[d], fqtype='center'
                    )

                temp2.append(temp[3])
            pval = stats.friedmanchisquare(temp2[0], temp2[1], temp2[2])

            temp3 = [d_type[d], lv, pval[1]]

            for i in range(len(temp3)):
                ratio[r_list[i]].append(temp3[i])

df = pd.DataFrame(ratio, columns=r_list)
df.to_csv(r'fp_diff_bar_stat.csv')
