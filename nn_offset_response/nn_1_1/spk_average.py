import os
import sys

sys.path.insert(1, os.path.dirname(os.path.dirname(os.getcwd())) + "/nn_tool")

import numpy as np
import h5py
from tools import nn_tool as nt
from parameter import parameters as pm
import matplotlib.pyplot as plt
import pickle
import quantities as pq
import pylustrator
import statsmodels.stats.api as sms

pylustrator.start()
# I'm going to use only 70 dB here

file = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
       "/dataset/nn_layer/nn_layer_nn_1_1.hdf5"

dbs = ['70', '60']
db = [0, 1]
val = pm.Setup(cond2='tsp')
cb = val.values()[-2]
dcmap = val.values()[7]
names = ['nn_1_1', 'nn_wn_1_1']
legends = ['NN', 'WN']
ch_l = [0, 8, 12]  # channel number
depth = [100, 800, 1200]
l_list = ['supr', 'gran', 'infr']  # list of layers
layer_name = ['Supragranular\nLayer', 'Granular\nLayer',
              'Infragranular\nLayer']
g_sf = {}  # dict to store spk
g_cf = {}  # dict for quartile

with h5py.File(file, 'r') as h_5:
    data = h_5['spk']['60']
    for n in names:
        g_sf[n] = []
        g_cf[n] = []
        for layer in l_list:
            tems = np.median(data[n][layer], axis=0)  # average spk
            temc2 = np.percentile(data[n][layer], 25, axis=0)
            temc7 = np.percentile(data[n][layer], 75, axis=0)
            t_max = np.max(tems[1000:1101])  # peak value

            # ind of offset peak
            t_ind = [
                x for x in np.where(tems == t_max)[0] if 1000 < x < 1101
                ][0]

            t_ic = [temc2[t_ind], temc7[t_ind]]

            g_sf[n].append(t_max)
            g_cf[n].append(t_ic)

# plot
s_fig = plt.figure(figsize=(9, 9))
nx = np.arange(3)
width = 0.35

nn = plt.bar(
    nx - width / 2, g_sf[names[0]], width,
    label=names[0], color=dcmap[0])
wn = plt.bar(
    nx + width / 2, g_sf[names[1]], width,
    label=names[1], color=dcmap[1])



for i in nx:

    plt.plot([nx - width / 2, nx - width / 2], [g_cf[names[0]][i][0],
                                                g_cf[names[0]][i][1]], 'k')

    plt.plot([nx + width / 2, nx + width / 2], [g_cf[names[1]][i][0],
                                                g_cf[names[1]][i][1]], 'k')

plt.xticks(nx, layer_name)
plt.show()
