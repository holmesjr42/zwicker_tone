import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))

import pandas as pd
import numpy as np
import scipy as scipy
import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
from tools import nn_tool as nt
from parameters import parameters as pm
from statsmodels.stats.anova import AnovaRM
import pingouin

# this is for lfp at 60 dB here

file = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
       "/dataset/nn_layer/nn_layer_nn_3_1.hdf5"

val = pm.Setup(cond2='lfp')

dbs, db, dcmap, names, legendl, ch_l, l_list, layer_name = val.nn31_plot()
legends = legendl[0]

g_st = {}

type1 = 'lfp'
level = '60'

with h5py.File(file, 'r') as h_5:
    data = h_5[type1][level]
    for n in names:
        g_st[n] = []

        for layer in l_list:
            t_ic, t_min, t_ind = nt.layer_average(data[n], layer, type='lfp')

            # wilcoxon ranksum
            wil = np.transpose(data[n][layer])
            g_st[n].append(np.array(wil[t_ind]))

for i in range(len(l_list)):
    animal1 = np.arange(len(g_st[names[0]][i]))
    animals = [str(np.int(k)) for k in animal1]

    data = np.vstack(
        [g_st[names[0]][i], g_st[names[1]][i],
         animals]
        ).transpose()

    df = pd.DataFrame(data, columns=['NN', 'WN', 'Animal'])
    tidy = pd.melt(
        df, id_vars='Animal', var_name='condition', value_name="types"
        )

    print(layer_name[i], AnovaRM(
        data=tidy, depvar="types",
        subject='Animal', within=['condition']).fit())

