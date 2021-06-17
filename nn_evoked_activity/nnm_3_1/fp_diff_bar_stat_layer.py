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

file_input = ['/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
              '/data/dataset/fp_layer/fp_layer_nnm_3_1.hdf5',
              '/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021' \
              '/data/dataset/fp_layer/fp_layer_nnm_wn_3_1.hdf5'
              ]
# file_input = snakemake.input[0]

# stimulus conditions for this script: 0, NN; 1, WN
conds = [
    [sets[-2][0], sets[-5][0], sets[-4][0]],
    [sets[-1][0], sets[-5][0], sets[-3][0]]
    ]

l_list = sets[2]


# index list of low edge, high edge
finx = [sets[3][1], sets[3][3]]
paradigm = [sets[6][1:3], [sets[6][-1]]]

# coordination of cond sublist and paired test execution
k_list = [[1, 2], [2]]


d_list = [paradigm[0][0], paradigm[0][1], paradigm[1][0]]
d_type = ['spk', 'lfp']

ratio = {'data': [], 'condition': [], 'SPL dB': [], 'p-value': []}
r_list = list(ratio.keys())

# load file
for f in range(len(file_input)):
    file = file_input[f]
    kl = k_list[f]
    pdm = paradigm[f]
    cond = conds[f]
    with h5py.File(file, 'r') as dat:
        dats = [dat['fps'], dat['fpl']]
        base = dat['base']

        for d in range(len(d_type)):
            for lv in lvl:
                for k in range(len(kl)):
                    k1 = kl[k]
                    pdm1 = pdm[k]
                    # getting coord of nn condition. check cn for details
                    ctrl = cond[0]
                    cn = cond[k1]  # condition which you want to calculate
                    # difference
                    cnn = cond[1]  # nn-on to find frequency indice for each animal
                    # storing level-wise data temporarily.
                    # 3 indicates: median and 2 quartiles
                    temp1 = []
                    for ln in range(len(l_list)):
                        layer = l_list[ln]

                        teemp = nt.diff_on_off(
                            dats[d], layer, lv, cn, ctrl, cnn,
                            bdata=base, types=d_type[d]
                            )

                        temp1.append(teemp[4])

                    pval = stats.friedmanchisquare(temp1[0], temp1[1], temp1[2])

                    temp3 = [d_type[d], cn, lv, pval[1]]

                    for i in range(len(temp3)):
                        ratio[r_list[i]].append(temp3[i])

df = pd.DataFrame(ratio, columns=r_list)
df.to_csv(r'fp_diff_bar_stat_3_1.csv')

