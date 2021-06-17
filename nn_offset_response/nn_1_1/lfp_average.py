import os
import sys

sys.path.insert(1, os.path.dirname(os.getcwd()))

import numpy as np
import h5py
from parameters import parameters as pm
import matplotlib.pyplot as plt
import pylustrator
from tools import nn_tool as nt
from scipy import stats

pylustrator.start()
# I'm going to use only 60 dB here

file = "/home/bhc/OneDrive/Work/PhD/projects/zwicker_tone_2018_2021/data" \
       "/dataset/nn_layer/nn_layer_nn_1_1.hdf5"

val = pm.Setup(cond2='tsp')

dbs, db, dcmap, names, legendl, ch_l, l_list, layer_name = val.nn11_plot()
legends = legendl[0]

g_lf = {}  # dict to store lfp
g_sdf = {}  # dict for quartile
g_wf = {}  # for wilcoxon
tt= []
with h5py.File(file, 'r') as h_5:
    data = h_5['lfp']['60']

    for n in names:
        g_lf[n] = []
        g_sdf[n] = []
        g_wf[n] = []

        for layer in l_list:
            t_ic, t_min, t_ind = nt.layer_average(data[n], layer, type='lfp')

            # wilcoxon ranksum
            wil = np.transpose(data[n][layer])
            g_wf[n].append(np.array(wil[t_ind]))

            g_lf[n].append(abs(t_min))
            g_sdf[n].append(t_ic)

for i in range(len(l_list)):
    print(stats.wilcoxon(g_wf[names[0]][i], g_wf[names[1]][i]))

# plot
s_fig = plt.figure(figsize=(9, 9))
nx = np.arange(3)
width = 0.35

nn = plt.bar(
    nx - width / 2, g_lf[names[0]], width,
    label=legends[0], color=dcmap[0])
wn = plt.bar(
    nx + width / 2, g_lf[names[1]], width,
    label=legends[1], color=dcmap[1])

plt.legend(prop={'size': 15},
           loc='upper left',
           bbox_to_anchor=(0, 1))

# for SD in the figure
# for i in nx:
#
#     plt.plot([nx - width / 2, nx - width / 2], [g_sdf[names[0]][i][0],
#                                                 g_sdf[names[0]][i][1]], 'k')
#
#     plt.plot([nx + width / 2, nx + width / 2], [g_sdf[names[1]][i][0],
#                                                 g_sdf[names[1]][i][1]], 'k')

plt.xticks(nx, layer_name, size=15, weight='bold')
plt.yticks(size=15)
plt.text(0, 0, 'Field potential (mV)', size=20, weight='bold',
         horizontalalignment='center', verticalalignment='center',
         rotation='vertical')

#% start: automatic generated code from pylustrator
plt.figure(1).ax_dict = {ax.get_label(): ax for ax in plt.figure(1).axes}
import matplotlib as mpl
plt.figure(1).axes[0].set_position([0.190556, 0.110000, 0.775000, 0.770000])
plt.figure(1).axes[0].texts[0].set_position([-1.030452, 0.013499])
#% end: automatic generated code from pylustrator
plt.show()
